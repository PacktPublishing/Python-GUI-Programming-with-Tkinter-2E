import csv
from pathlib import Path
import os
import json

from .constants import FieldTypes as FT
from decimal import Decimal
from datetime import datetime

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
      csvreader = csv.DictReader(fh.readlines())
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
    'autofill sheet data': {'type': 'bool', 'value': True}
  }

  def __init__(self):
    # determine the file path
    filename = 'abq_settings.json'
    self.filepath = Path.home() / filename

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
    with open(self.filepath, 'w') as fh:
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
