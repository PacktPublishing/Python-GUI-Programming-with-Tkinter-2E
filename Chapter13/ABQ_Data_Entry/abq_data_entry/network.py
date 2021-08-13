from urllib.request import urlopen
from xml.etree import ElementTree
import requests
import ftplib as ftp
from os import path

def get_local_weather(station):
  """Retrieve local weather data from the web

  Returns a dictionary containing:
    - observation_time_rfc822: timestamp of observation in rfc822 format
    - temp_c: The temperature in degrees C
    - relative_humidity: Relative Humidity percentage
    - pressure_mb: Air pressure in mb
    - weather: A string describing weather conditions
  """
  url = f'http://w1.weather.gov/xml/current_obs/{station}.xml'
  response = urlopen(url)

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


def upload_to_corporate_rest(
    filepath, upload_url, auth_url,
    username, password):
  """Upload a file to the corporate server using REST"""

  session = requests.session()

  response = session.post(
    auth_url,
    data={'username': username, 'password': password}
  )
  response.raise_for_status()

  files = {'file': open(filepath, 'rb')}
  response = session.put(
    upload_url,
    files=files
  )
  files['file'].close()
  response.raise_for_status()


def upload_to_corporate_ftp(
    filepath, ftp_host,
    ftp_port, ftp_user, ftp_pass):
  """Upload a file to the corporate server using FTP"""

  with ftp.FTP() as ftp_cx:
    # connect and login
    ftp_cx.connect(ftp_host, ftp_port)
    ftp_cx.login(ftp_user, ftp_pass)

    # upload file
    filename = path.basename(filepath)

    with open(filepath, 'rb') as fh:
      ftp_cx.storbinary('STOR {}'.format(filename), fh)

def get_corporate_ftp_files(ftp_host, ftp_port, ftp_user, ftp_pass):
  """Get a list of the files on the FTP host"""
  with ftp.FTP() as ftp_cx:
    ftp_cx.connect(ftp_host, ftp_port)
    ftp_cx.login(ftp_user, ftp_pass)
    files = ftp_cx.nlst()

  return files
