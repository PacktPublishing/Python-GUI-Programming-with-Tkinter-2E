import csv
from pathlib import Path
import os
import json
import platform
from datetime import datetime
from urllib.request import urlopen
from xml.etree import ElementTree
import requests
import paramiko
from threading import Thread, Lock
from queue import Queue
from collections import namedtuple

import psycopg2 as pg
from psycopg2.extras import DictCursor

from .constants import FieldTypes as FT

Message = namedtuple('Message', ['status', 'subject', 'body'])

class SQLModel:
  """Data Model for SQL data storage"""

  fields = {
    "Date": {'req': True, 'type': FT.iso_date_string},
    "Time": {'req': True, 'type': FT.string_list,
         'values': ['8:00', '12:00', '16:00', '20:00']},
    "Technician": {'req': True, 'type':  FT.string_list,
             'values': []},
    "Lab": {'req': True, 'type': FT.short_string_list,
        'values': []},
    "Plot": {'req': True, 'type': FT.string_list,
         'values': []},
    "Seed Sample":  {'req': True, 'type': FT.string},
    "Humidity": {'req': True, 'type': FT.decimal,
           'min': 0.5, 'max': 52.0, 'inc': .01},
    "Light": {'req': True, 'type': FT.decimal,
          'min': 0, 'max': 100.0, 'inc': .01},
    "Temperature": {'req': True, 'type': FT.decimal,
            'min': 4, 'max': 40, 'inc': .01},
    "Equipment Fault": {'req': False, 'type': FT.boolean},
    "Plants": {'req': True, 'type': FT.integer,
           'min': 0, 'max': 20},
    "Blossoms": {'req': True, 'type': FT.integer,
           'min': 0, 'max': 1000},
    "Fruit": {'req': True, 'type': FT.integer,
          'min': 0, 'max': 1000},
    "Min Height": {'req': True, 'type': FT.decimal,
             'min': 0, 'max': 1000, 'inc': .01},
    "Max Height": {'req': True, 'type': FT.decimal,
             'min': 0, 'max': 1000, 'inc': .01},
    "Med Height": {'req': True, 'type': FT.decimal,
              'min': 0, 'max': 1000, 'inc': .01},
    "Notes": {'req': False, 'type': FT.long_string}
  }
  lc_update_query = (
    'UPDATE lab_checks SET lab_tech_id = '
    '(SELECT id FROM lab_techs WHERE name = %(Technician)s) '
    'WHERE date=%(Date)s AND time=%(Time)s AND lab_id=%(Lab)s'
  )

  lc_insert_query = (
    'INSERT INTO lab_checks VALUES (%(Date)s, %(Time)s, %(Lab)s, '
    '(SELECT id FROM lab_techs WHERE name LIKE %(Technician)s))'
  )

  pc_update_query = (
    'UPDATE plot_checks SET date=%(Date)s, time=%(Time)s, '
    'lab_id=%(Lab)s, plot=%(Plot)s,  seed_sample = %(Seed Sample)s, '
    'humidity = %(Humidity)s, light = %(Light)s, '
    'temperature = %(Temperature)s, '
    'equipment_fault = %(Equipment Fault)s, '
    'blossoms = %(Blossoms)s, plants = %(Plants)s, '
    'fruit = %(Fruit)s, max_height = %(Max Height)s, '
    'min_height = %(Min Height)s, median_height = %(Med Height)s, '
    'notes = %(Notes)s WHERE date=%(key_date)s AND time=%(key_time)s '
    'AND lab_id=%(key_lab)s AND plot=%(key_plot)s')

  pc_insert_query = (
    'INSERT INTO plot_checks VALUES (%(Date)s, %(Time)s, %(Lab)s,'
    ' %(Plot)s, %(Seed Sample)s, %(Humidity)s, %(Light)s,'
    ' %(Temperature)s, %(Equipment Fault)s, %(Blossoms)s, %(Plants)s,'
    ' %(Fruit)s, %(Max Height)s, %(Min Height)s,'
    ' %(Med Height)s, %(Notes)s)')

  def __init__(self, host, database, user, password):
    self.connection = pg.connect(host=host, database=database,
      user=user, password=password, cursor_factory=DictCursor)

    techs = self.query("SELECT name FROM lab_techs ORDER BY name")
    labs = self.query("SELECT id FROM labs ORDER BY id")
    plots = self.query("SELECT DISTINCT plot FROM plots ORDER BY plot")
    self.fields['Technician']['values'] = [x['name'] for x in techs]
    self.fields['Lab']['values'] = [x['id'] for x in labs]
    self.fields['Plot']['values'] = [str(x['plot']) for x in plots]

  def query(self, query, parameters=None):
    with self.connection:
      with self.connection.cursor() as cursor:
        cursor.execute(query, parameters)
      # cursor.description is None when
      # no rows are returned
        if cursor.description is not None:
          return cursor.fetchall()

  def get_all_records(self, all_dates=False):
    """Return all records.

    By default, only return today's records, unless
    all_dates is True.
    """
    query = ('SELECT * FROM data_record_view '
      'WHERE %(all_dates)s OR "Date" = CURRENT_DATE '
      'ORDER BY "Date" DESC, "Time", "Lab", "Plot"')
    return self.query(query, {'all_dates': all_dates})

  def get_record(self, rowkey):
    """Return a single record

    rowkey must be a tuple of date, time, lab, and plot
    """
    date, time, lab, plot = rowkey
    query = (
      'SELECT * FROM data_record_view '
      'WHERE "Date" = %(date)s AND "Time" = %(time)s '
      'AND "Lab" = %(lab)s AND "Plot" = %(plot)s')
    result = self.query(
      query,
      {"date": date, "time": time, "lab": lab, "plot": plot}
    )
    return result[0] if result else dict()

  def save_record(self, record, rowkey):
    """Save a record to the database

    rowkey must be a tuple of date, time, lab, and plot.
      Or None if this is a new record.
    """
    if rowkey:
      key_date, key_time, key_lab, key_plot = rowkey
      record.update({
        "key_date": key_date,
        "key_time": key_time,
        "key_lab": key_lab,
        "key_plot": key_plot
      })

    # Lab check is based on the entered date/time/lab
    if self.get_lab_check(
      record['Date'], record['Time'], record['Lab']
    ):
      lc_query = self.lc_update_query
    else:
      lc_query = self.lc_insert_query
    # Plot check is based on the key values
    if rowkey:
      pc_query = self.pc_update_query
    else:
      pc_query = self.pc_insert_query

    self.query(lc_query, record)
    self.query(pc_query, record)

  def get_lab_check(self, date, time, lab):
    """Retrieve the lab check record for the given date, time, and lab"""
    query = ('SELECT date, time, lab_id, lab_tech_id, '
      'lt.name as lab_tech FROM lab_checks JOIN lab_techs lt '
      'ON lab_checks.lab_tech_id = lt.id WHERE '
      'lab_id = %(lab)s AND date = %(date)s AND time = %(time)s')
    results = self.query(
      query, {'date': date, 'time': time, 'lab': lab})
    return results[0] if results else dict()

  def get_current_seed_sample(self, lab, plot):
    """Get the seed sample currently planted in the given lab and plot"""
    result = self.query('SELECT current_seed_sample FROM plots '
      'WHERE lab_id=%(lab)s AND plot=%(plot)s',
      {'lab': lab, 'plot': plot})
    return result[0]['current_seed_sample'] if result else ''

  def add_weather_data(self, data):
    query = (
      'INSERT INTO local_weather VALUES '
      '(%(observation_time_rfc822)s, %(temp_c)s, '
      '%(relative_humidity)s, %(pressure_mb)s, '
      '%(weather)s)'
    )
    try:
      self.query(query, data)
    except pg.IntegrityError:
      # already have weather for this datetime
      pass

class CSVModel:
  """CSV file storage"""

  fields = {
    "Date": {'req': True, 'type': FT.iso_date_string},
    "Time": {'req': True, 'type': FT.string_list,
             'values': ['8:00', '12:00', '16:00', '20:00']},
    "Technician": {'req': True, 'type':  FT.string},
    "Lab": {'req': True, 'type': FT.short_string_list,
            'values': ['A', 'B', 'C']},
    "Plot": {'req': True, 'type': FT.string_list,
             'values': [str(x) for x in range(1, 21)]},
    "Seed Sample":  {'req': True, 'type': FT.string},
    "Humidity": {'req': True, 'type': FT.decimal,
                 'min': 0.5, 'max': 52.0, 'inc': .01},
    "Light": {'req': True, 'type': FT.decimal,
              'min': 0, 'max': 100.0, 'inc': .01},
    "Temperature": {'req': True, 'type': FT.decimal,
                    'min': 4, 'max': 40, 'inc': .01},
    "Equipment Fault": {'req': False, 'type': FT.boolean},
    "Plants": {'req': True, 'type': FT.integer, 'min': 0, 'max': 20},
    "Blossoms": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Fruit": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Min Height": {'req': True, 'type': FT.decimal,
                   'min': 0, 'max': 1000, 'inc': .01},
    "Max Height": {'req': True, 'type': FT.decimal,
                   'min': 0, 'max': 1000, 'inc': .01},
    "Med Height": {'req': True, 'type': FT.decimal,
                   'min': 0, 'max': 1000, 'inc': .01},
    "Notes": {'req': False, 'type': FT.long_string}
  }


  def __init__(self, filename=None):

    if not filename:
      datestring = datetime.today().strftime("%Y-%m-%d")
      filename = "abq_data_record_{}.csv".format(datestring)
    self.file = Path(filename)

    # Check for append permissions:
    file_exists = os.access(self.file, os.F_OK)
    parent_writeable = os.access(self.file.parent, os.W_OK)
    file_writeable = os.access(self.file, os.W_OK)
    if (
      (not file_exists and not parent_writeable) or
      (file_exists and not file_writeable)
    ):
      msg = f'Permission denied accessing file: {filename}'
      raise PermissionError(msg)


  def save_record(self, data, rownum=None):
    """Save a dict of data to the CSV file"""

    if rownum is None:
      # This is a new record
      newfile = not self.file.exists()

      with open(self.file, 'a', newline='') as fh:
        csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
        if newfile:
          csvwriter.writeheader()
        csvwriter.writerow(data)
    else:
      # This is an update
      records = self.get_all_records()
      records[rownum] = data
      with open(self.file, 'w', encoding='utf-8', newline='') as fh:
        csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
        csvwriter.writeheader()
        csvwriter.writerows(records)

  def get_all_records(self):
    """Read in all records from the CSV and return a list"""
    if not self.file.exists():
      return []

    with open(self.file, 'r', encoding='utf-8') as fh:
      # Casting to list is necessary for unit tests to work
      csvreader = csv.DictReader(fh)
      missing_fields = set(self.fields.keys()) - set(csvreader.fieldnames)
      if len(missing_fields) > 0:
        fields_string = ', '.join(missing_fields)
        raise Exception(
          f"File is missing fields: {fields_string}"
        )
      records = list(csvreader)

    # Correct issue with boolean fields
    trues = ('true', 'yes', '1')
    bool_fields = [
      key for key, meta
      in self.fields.items()
      if meta['type'] == FT.boolean
    ]
    for record in records:
      for key in bool_fields:
        record[key] = record[key].lower() in trues
    return records

  def get_record(self, rownum):
    """Get a single record by row number

    Callling code should catch IndexError
      in case of a bad rownum.
    """

    return self.get_all_records()[rownum]


class SettingsModel:
  """A model for saving settings"""

  fields = {
    'autofill date': {'type': 'bool', 'value': True},
    'autofill sheet data': {'type': 'bool', 'value': True},
    'font size': {'type': 'int', 'value': 9},
    'font family': {'type': 'str', 'value': ''},
    'theme': {'type': 'str', 'value': 'default'},
    'db_host': {'type': 'str', 'value': 'localhost'},
    'db_name': {'type': 'str', 'value': 'abq'},
    'weather_station': {'type': 'str', 'value': 'KBMG'},
    'abq_rest_url': {
      'type': 'str',
      'value': 'http://localhost:8000'
      },
    'abq_sftp_host': {'type': 'str', 'value': 'localhost'},
    'abq_sftp_port': {'type': 'int', 'value': 22},
    'abq_sftp_path': {'type': 'str', 'value': 'ABQ/BLTN_IN'}
  }

  config_dirs = {
    "Linux": Path(os.environ.get('$XDG_CONFIG_HOME', Path.home() / '.config')),
    "freebsd7": Path(os.environ.get('$XDG_CONFIG_HOME', Path.home() / '.config')),
    'Darwin': Path.home() / 'Library' / 'Application Support',
    'Windows': Path.home() / 'AppData' / 'Local'
  }

  def __init__(self):
    # determine the file path
    filename = 'abq_settings.json'
    filedir = self.config_dirs.get(platform.system(), Path.home())
    self.filepath = filedir / filename

    # load in saved values
    self.load()

  def set(self, key, value):
    """Set a variable value"""
    if (
      key in self.fields and
      type(value).__name__ == self.fields[key]['type']
    ):
      self.fields[key]['value'] = value
    else:
      raise ValueError("Bad key or wrong variable type")

  def save(self):
    """Save the current settings to the file"""
    json_string = json.dumps(self.fields)
    with open(self.filepath, 'w', encoding='utf-8') as fh:
      fh.write(json_string)

  def load(self):
    """Load the settings from the file"""

    # if the file doesn't exist, return
    if not self.filepath.exists():
      return

    # open the file and read in the raw values
    with open(self.filepath, 'r') as fh:
      raw_values = json.loads(fh.read())

    # don't implicitly trust the raw values, but only get known keys
    for key in self.fields:
      if key in raw_values and 'value' in raw_values[key]:
        raw_value = raw_values[key]['value']
        self.fields[key]['value'] = raw_value

class WeatherDataModel:

  base_url = 'http://w1.weather.gov/xml/current_obs/{}.xml'

  def __init__(self, station):
    self.url = self.base_url.format(station)


  def get_weather_data(self):
    response = urlopen(self.url)

    xmlroot = ElementTree.fromstring(response.read())
    weatherdata = {
      'observation_time_rfc822': None,
      'temp_c': None,
      'relative_humidity': None,
      'pressure_mb': None,
      'weather': None
    }

    for tag in weatherdata:
      element = xmlroot.find(tag)
      if element is not None:
        weatherdata[tag] = element.text

    return weatherdata



class ThreadedUploader(Thread):

  upload_lock = Lock()

  def __init__(self, session_cookie, files_url, filepath, queue):
    super().__init__()
    self.files_url = files_url
    self.filepath = filepath
    self.session = requests.Session()
    self.session.cookies['session'] = session_cookie
    self.queue = queue


  def run(self, *args, **kwargs):
    self.queue.put(
      Message(
        'info', 'Upload Started',
        f'Begin upload of {self.filepath}'
      )
    )

    with self.upload_lock:
      with open(self.filepath, 'rb') as fh:
        files = {'file': fh}
        response = self.session.put(
          self.files_url, files=files
        )
      try:
        response.raise_for_status()
      except Exception as e:
        self.queue.put(Message('error', 'Upload Error', str(e)))
      else:
        self.queue.put(
          Message(
            'done',
            'Upload Succeeded',
            f'Upload of {self.filepath} to REST succeeded'
          )
        )


class CorporateRestModel:

  def __init__(self, base_url):

    self.auth_url = f'{base_url}/auth'
    self.files_url = f'{base_url}/files'
    self.session = requests.session()
    self.queue = Queue()

  @staticmethod
  def _raise_for_status(response):
    try:
      response.raise_for_status()
    except requests.HTTPError:
      raise Exception(response.json().get('message'))

  def authenticate(self, username, password):
    """Authenticate to the server"""
    response = self.session.post(
      self.auth_url,
      data={'username': username, 'password': password}
    )
    self._raise_for_status(response)

  def check_file(self, filename):
    """See if a file exists on the server"""
    url = f"{self.files_url}/{filename}"
    response = self.session.head(url)
    if response.status_code == 200:
      return True
    elif response.status_code == 404:
      return False
    self._raise_for_status(response)

  def get_file(self, filename):
    """Download a file from the server"""
    url = f"{self.files_url}/{filename}"
    response = self.session.get(url)
    self._raise_for_status(response)
    return response.text

  def upload_file(self, filepath):
    """PUT a file on the server"""
    cookie = self.session.cookies.get('session')
    uploader = ThreadedUploader(
      cookie, self.files_url, filepath, self.queue
    )
    uploader.start()

class SFTPModel:

  def __init__(self, host, port=22):
    self.host = host
    self.port = port

    # setup SSHClient
    self._client = paramiko.SSHClient()
    self._client.set_missing_host_key_policy(
      paramiko.AutoAddPolicy()
    )
    self._client.load_system_host_keys()


  def authenticate(self, username, password):
    try:
      self._client.connect(
        self.host, username=username,
        password=password, port=self.port
      )
    except paramiko.AuthenticationException:
      raise Exception(
        'The username and password were not accepted by the server.'
      )

  def _check_auth(self):
    transport = self._client.get_transport()
    if not transport.is_active() and transport.is_authenticated():
      raise Exception('Not connected to a server.')


  def check_file(self, remote_path):
    """Check if the file at remote_path exists"""
    self._check_auth()
    sftp = self._client.open_sftp()
    try:
      sftp.stat(remote_path)
    except FileNotFoundError:
      return False
    return True

  def upload_file(self, local_path, remote_path):
    """Upload file at local_path to remote_path

    Both paths must include a filename
    """
    self._check_auth()
    sftp = self._client.open_sftp()

    # Create the dstination path if it doesn't exist
    remote_path = Path(remote_path)
    for directory in remote_path.parent.parts:
      if directory not in sftp.listdir():
        sftp.mkdir(directory)
      sftp.chdir(directory)
    # copy the file
    # just use filename because our CWD should
    # be the full path without the name
    sftp.put(local_path, remote_path.name)

  def get_file(self, remote_path, local_path):
    self._check_auth()
    sftp = self._client.open_sftp()
    sftp.get(remote_path, local_path)
