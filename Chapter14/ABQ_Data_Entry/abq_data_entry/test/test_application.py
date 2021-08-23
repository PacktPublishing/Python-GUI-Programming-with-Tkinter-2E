from unittest import TestCase
from unittest.mock import patch
from .. import application


class TestApplication(TestCase):
  records = [
    {'Date': '2018-06-01', 'Time': '8:00', 'Technician': 'J Simms',
     'Lab': 'A', 'Plot': '1', 'Seed Sample': 'AX477',
     'Humidity': '24.09', 'Light': '1.03', 'Temperature': '22.01',
     'Equipment Fault': False,  'Plants': '9', 'Blossoms': '21',
     'Fruit': '3', 'Max Height': '8.7', 'Med Height': '2.73',
     'Min Height': '1.67', 'Notes': '\n\n',
    },
    {'Date': '2018-06-01', 'Time': '8:00', 'Technician': 'J Simms',
     'Lab': 'A', 'Plot': '2', 'Seed Sample': 'AX478',
     'Humidity': '24.47', 'Light': '1.01', 'Temperature': '21.44',
     'Equipment Fault': False, 'Plants': '14', 'Blossoms': '27',
     'Fruit': '1', 'Max Height': '9.2', 'Med Height': '5.09',
     'Min Height': '2.35', 'Notes': ''
     }
  ]

  settings = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True},
        'font size': {'type': 'int', 'value': 9},
        'font family': {'type': 'str', 'value': ''},
        'theme': {'type': 'str', 'value': 'default'}
      }

  def setUp(self):
    # can be parenthesized in python 3.10+
    with \
      patch('abq_data_entry.application.m.CSVModel') as csvmodel,\
      patch('abq_data_entry.application.m.SettingsModel') as settingsmodel,\
      patch('abq_data_entry.application.Application._show_login') as show_login,\
      patch('abq_data_entry.application.v.DataRecordForm'),\
      patch('abq_data_entry.application.v.RecordList'),\
      patch('abq_data_entry.application.ttk.Notebook'),\
      patch('abq_data_entry.application.get_main_menu_for_os')\
    :

      settingsmodel().fields = self.settings
      csvmodel().get_all_records.return_value = self.records
      show_login.return_value = True
      self.app = application.Application()

  def tearDown(self):
    self.app.update()
    self.app.destroy()

  def test_show_recordlist(self):
    self.app._show_recordlist()
    self.app.update()
    self.app.notebook.select.assert_called_with(self.app.recordlist)

  def test_populate_recordlist(self):
    # test correct functions
    self.app._populate_recordlist()
    self.app.model.get_all_records.assert_called()
    self.app.recordlist.populate.assert_called_with(self.records)

    # test exceptions

    self.app.model.get_all_records.side_effect = Exception('Test message')
    with patch('abq_data_entry.application.messagebox'):
      self.app._populate_recordlist()
      application.messagebox.showerror.assert_called_with(
        title='Error', message='Problem reading file',
        detail='Test message'
      )
