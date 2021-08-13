"""The application/controller class for ABQ Data Entry"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import platform

from . import views as v
from . import models as m
from .mainmenu import get_main_menu_for_os
from . import images
from . import network as n


class Application(tk.Tk):
  """Application root window"""


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # move here for ch12 because we need some settings data to authenticate
    self.settings_model = m.SettingsModel()
    self._load_settings()

    # Hide window while GUI is built
    self.withdraw()

    # Authenticate
    if not self._show_login():
      self.destroy()
      return

    # show the window
    self.deiconify()

   # Create model
   # remove for ch12
   # self.model = m.CSVModel()

    self.inserted_rows = []
    self.updated_rows = []

    # Begin building GUI
    self.title("ABQ Data Entry Application")
    self.columnconfigure(0, weight=1)

    # Set taskbar icon
    self.taskbar_icon = tk.PhotoImage(file=images.ABQ_LOGO_64)
    self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

    # Create the menu
    #menu = MainMenu(self, self.settings)
    menu_class = get_main_menu_for_os(platform.system())
    menu = menu_class(self, self.settings)

    self.config(menu=menu)
    event_callbacks = {
      '<<FileQuit>>': lambda _: self.quit(),
      '<<ShowRecordlist>>': self._show_recordlist,
      '<<NewRecord>>': self._new_record,
      '<<UpdateWeatherData>>': self._update_weather_data,
      '<<UploadToCorporateREST>>': self._upload_to_corporate_rest,
      '<<UploadToCorporateFTP>>': self._upload_to_corporate_ftp,
     }
    for sequence, callback in event_callbacks.items():
      self.bind(sequence, callback)

    # new for ch9
    self.logo = tk.PhotoImage(file=images.ABQ_LOGO_32)
    ttk.Label(
      self,
      text="ABQ Data Entry Application",
      font=("TkDefaultFont", 16),
      image=self.logo,
      compound=tk.LEFT
    ).grid(row=0)

    # The notebook
    self.notebook = ttk.Notebook(self)
    self.notebook.enable_traversal()
    self.notebook.grid(row=1, padx=10, sticky='NSEW')

    # The data record form
    self.recordform_icon = tk.PhotoImage(file=images.FORM_ICON)
    self.recordform = v.DataRecordForm(self, self.model, self.settings)
    self.notebook.add(
        self.recordform, text='Entry Form',
        image=self.recordform_icon, compound=tk.LEFT
    )
    self.recordform.bind('<<SaveRecord>>', self._on_save)


    # The data record list
    self.recordlist_icon = tk.PhotoImage(file=images.LIST_ICON)
    self.recordlist = v.RecordList(
      self, self.inserted_rows, self.updated_rows
    )
    self.notebook.insert(
        0, self.recordlist, text='Records',
        image=self.recordlist_icon, compound=tk.LEFT
    )
    self._populate_recordlist()
    self.recordlist.bind('<<OpenRecord>>', self._open_record)


    self._show_recordlist()

    # status bar
    self.status = tk.StringVar()
    self.statusbar = ttk.Label(self, textvariable=self.status)
    self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)


    self.records_saved = 0


  def _on_save(self, *_):
    """Handles file-save requests"""

    # Check for errors first

    errors = self.recordform.get_errors()
    if errors:
      self.status.set(
        "Cannot save, error in fields: {}"
        .format(', '.join(errors.keys()))
      )
      message = "Cannot save record"
      detail = "The following fields have errors: \n  * {}".format(
        '\n  * '.join(errors.keys())
      )
      messagebox.showerror(
        title='Error',
        message=message,
        detail=detail
      )
      return False

    data = self.recordform.get()
    rowkey = self.recordform.current_record
    self.model.save_record(data, rowkey)
    if rowkey is not None:
      self.updated_rows.append(rowkey)
    else:
      rowkey = (data['Date'], data['Time'], data['Lab'], data['Plot'])
      self.inserted_rows.append(rowkey)
    self.records_saved += 1
    self.status.set(
      "{} records saved this session".format(self.records_saved)
    )
    self.recordform.reset()
    self._populate_recordlist()

# Remove for ch12
#  def _on_file_select(self, *_):
#    """Handle the file->select action"""
#
#    filename = filedialog.asksaveasfilename(
#      title='Select the target file for saving records',
#      defaultextension='.csv',
#      filetypes=[('CSV', '*.csv *.CSV')]
#    )
#    if filename:
#      self.model = m.CSVModel(filename=filename)
#      self.inserted_rows.clear()
#      self.updated_rows.clear()
#      self._populate_recordlist()

  @staticmethod
  def _simple_login(username, password):
    """A basic authentication backend with a hardcoded user and password"""
    return username == 'abq' and password == 'Flowers'

  # new ch12
  def _database_login(self, username, password):
    """Try to login to the database and create self.data_model"""
    db_host = self.settings['db_host'].get()
    db_name = self.settings['db_name'].get()
    try:
      self.model = m.SQLModel(
        db_host, db_name, username, password)
    except m.pg.OperationalError as e:
      print(e)
      return False
    return True

  def _show_login(self):
    """Show login dialog and attempt to login"""
    error = ''
    title = "Login to ABQ Data Entry"
    while True:
      login = v.LoginDialog(self, title, error)
      if not login.result:  # User canceled
        return False
      username, password = login.result
      if self._database_login(username, password):
        return True
      error = 'Login Failed' # loop and redisplay

  def _load_settings(self):
    """Load settings into our self.settings dict."""

    vartypes = {
      'bool': tk.BooleanVar,
      'str': tk.StringVar,
      'int': tk.IntVar,
      'float': tk.DoubleVar
    }

    # create our dict of settings variables from the model's settings.
    self.settings = dict()
    for key, data in self.settings_model.fields.items():
      vartype = vartypes.get(data['type'], tk.StringVar)
      self.settings[key] = vartype(value=data['value'])

    # put a trace on the variables so they get stored when changed.
    for var in self.settings.values():
      var.trace_add('write', self._save_settings)

    # update font settings after loading them
    self._set_font()
    self.settings['font size'].trace_add('write', self._set_font)
    self.settings['font family'].trace_add('write', self._set_font)

    # process theme
    style = ttk.Style()
    theme = self.settings.get('theme').get()
    if theme in style.theme_names():
      style.theme_use(theme)

  def _save_settings(self, *_):
    """Save the current settings to a preferences file"""

    for key, variable in self.settings.items():
      self.settings_model.set(key, variable.get())
    self.settings_model.save()

  def _show_recordlist(self, *_):
    """Show the recordform"""
    self.notebook.select(self.recordlist)

  def _populate_recordlist(self):
    try:
      rows = self.model.get_all_records()
    except Exception as e:
      messagebox.showerror(
        title='Error',
        message='Problem reading file',
        detail=str(e)
      )
    else:
      self.recordlist.populate(rows)

  def _new_record(self, *_):
    """Open the record form with a blank record"""
    self.recordform.load_record(None, None)
    self.notebook.select(self.recordform)


  def _open_record(self, *_):
    """Open the Record selected recordlist id in the recordform"""
    rowkey = self.recordlist.selected_id
    try:
      record = self.model.get_record(rowkey)
    except Exception as e:
      messagebox.showerror(
        title='Error', message='Problem reading file', detail=str(e)
      )
      return
    self.recordform.load_record(rowkey, record)
    self.notebook.select(self.recordform)

  # new chapter 9
  def _set_font(self, *_):
    """Set the application's font"""
    font_size = self.settings['font size'].get()
    font_family = self.settings['font family'].get()
    font_names = ('TkDefaultFont', 'TkMenuFont', 'TkTextFont')
    for font_name in font_names:
      tk_font = font.nametofont(font_name)
      tk_font.config(size=font_size, family=font_family)

  # new chapter 13
  def _update_weather_data(self, *_):
    """Initiate retrieval and storage of weather data"""
    try:
      weather_data = n.get_local_weather(
        self.settings['weather_station'].get()
      )
    except Exception as e:
      messagebox.showerror(
        title='Error',
        message='Problem retrieving weather data',
        detail=str(e)
      )
      self.status.set('Problem retrieving weather data')
    else:
      self.model.add_weather_data(weather_data)
      time = weather_data['observation_time_rfc822']
      self.status.set(f"Weather data recorded for {time}")

  def _create_csv_extract(self):
    csvmodel = m.CSVModel()
    records = self.model.get_all_records()
    if not records:
      return None
    for record in records:
      csvmodel.save_record(record)
    return csvmodel.file

  def _upload_to_corporate_ftp(self, *_):

    csvfile = self._create_csv_extract()
    d = v.LoginDialog(self, 'Login to ABQ Corporate FTP')
    if d.result is None:
      return
    username, password = d.result
    host = self.settings['abq_ftp_host'].get()
    port = self.settings['abq_ftp_port'].get()
    try:
      n.upload_to_corporate_ftp(
        csvfile, host, port, username, password
      )
    except n.ftp.all_errors as e:
      messagebox.showerror('Error Uploading File.', str(e))
      return
    try:
      files = n.get_corporate_ftp_files(
        host, port, username, password
      )
    except n.ftp.all_errors as e:
      messagebox.showerror(
        'Error listing Files (file uploaded OK)',
        str(e)
      )
      return
    filestring = '\n'.join(f'* {f}' for f in files)
    messagebox.showinfo(
      'Success', f'{csvfile} successfully uploaded to FTP \n\n'
      f'Current files on the server are: \n\n {filestring}'
    )

  def _upload_to_corporate_rest(self, *_):
    csvfile = self._create_csv_extract()
    if csvfile is None:
      messagebox.showwarning(
        title='No records',
        message='There are no records to upload'
      )
      return
    d = v.LoginDialog(
      self, 'Login to ABQ Corporate REST API'
    )
    if d.result is not None:
      username, password = d.result
    else:
      return
    try:
      n.upload_to_corporate_rest(
        csvfile,
        self.settings['abq_upload_url'].get(),
        self.settings['abq_auth_url'].get(),
        username,
        password
      )
    except n.requests.ConnectionError as e:
      messagebox.showerror('Error connecting', str(e))
    except Exception as e:
      messagebox.showerror('General Exception', str(e))
    else:
      messagebox.showinfo(
        'Success',
        f'{csvfile} successfully uploaded to REST API.'
      )
