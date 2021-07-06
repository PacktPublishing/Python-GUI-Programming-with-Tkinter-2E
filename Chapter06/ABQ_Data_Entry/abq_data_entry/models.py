import csv
from pathlib import Path
import os
from .constants import FieldTypes as FT
from decimal import Decimal
from datetime import datetime

class CSVModel:
  """CSV file storage"""

  fields = {
    "Date": {'req': True, 'type': FT.iso_date_string},
    "Time": {
      'req': True, 'type': FT.string_list,
      'values': ['8:00', '12:00', '16:00', '20:00']
    },
    "Technician": {'req': True, 'type':  FT.string},
    "Lab": {
      'req': True, 'type': FT.short_string_list,
      'values': ['A', 'B', 'C']
    },
    "Plot": {
      'req': True, 'type': FT.string_list,
      'values': [str(x) for x in range(1, 21)]
    },
    "Seed Sample":  {'req': True, 'type': FT.string},
    "Humidity": {
      'req': True, 'type': FT.decimal,
      'min': 0.5, 'max': 52.0, 'inc': .01
    },
    "Light": {
      'req': True, 'type': FT.decimal,
      'min': 0, 'max': 100.0, 'inc': .01
    },
    "Temperature": {
      'req': True, 'type': FT.decimal,
      'min': 4, 'max': 40, 'inc': .01
    },
    "Equipment Fault": {'req': False, 'type': FT.boolean},
    "Plants": {'req': True, 'type': FT.integer, 'min': 0, 'max': 20},
    "Blossoms": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Fruit": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Min Height": {
      'req': True, 'type': FT.decimal,
      'min': 0, 'max': 1000, 'inc': .01
    },
    "Max Height": {
      'req': True, 'type': FT.decimal,
      'min': 0, 'max': 1000, 'inc': .01
    },
    "Med Height": {
      'req': True, 'type': FT.decimal,
      'min': 0, 'max': 1000, 'inc': .01
    },
    "Notes": {'req': False, 'type': FT.long_string}
  }


  def __init__(self):

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


  def save_record(self, data):
    """Save a dict of data to the CSV file"""
    newfile = not self.file.exists()

    with open(self.file, 'a', newline='') as fh:
      csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
      if newfile:
        csvwriter.writeheader()

      csvwriter.writerow(data)
