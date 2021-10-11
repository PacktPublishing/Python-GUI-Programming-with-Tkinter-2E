"""The application/controller class for ABQ Data Entry"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from . import views as v
from . import models as m
from .mainmenu import MainMenu

class Application(tk.Tk):
  """Application root window"""


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Hide window while GUI is built
    self.withdraw()

    # Authenticate
    if not self._show_login():
      self.destroy()
      return

    # show the window
    self.deiconify()

   # Create model
    self.model = m.CSVModel()

    # Load settings
    # self.settings = {
    #   'autofill date': tk.BooleanVar(),
    #   'autofill sheet data': tk.BoleanVar()
    # }
    self.settings_model = m.SettingsModel()
    self._load_settings()

    # Begin building GUI
    self.title("ABQ Data Entry Application")
    self.columnconfigure(0, weight=1)

    # Create the menu
    menu = MainMenu(self, self.settings)
    self.config(menu=menu)
    event_callbacks = {
      '<<FileSelect>>': self._on_file_select,
      '<<FileQuit>>': lambda _: self.quit(),
    }
    for sequence, callback in event_callbacks.items():
      self.bind(sequence, callback)


    ttk.Label(
      self,
      text="ABQ Data Entry Application",
      font=("TkDefaultFont", 16)
    ).grid(row=0)

    self.recordform = v.DataRecordForm(self, self.model, self.settings)
    self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
    self.recordform.bind('<<SaveRecord>>', self._on_save)

    # status bar
    self.status = tk.StringVar()
    self.statusbar = ttk.Label(self, textvariable=self.status)
    self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)


    self._records_saved = 0


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
    self.model.save_record(data)
    self._records_saved += 1
    self.status.set(
      "{} records saved this session".format(self._records_saved)
    )
    self.recordform.reset()

  def _on_file_select(self, *_):
    """Handle the file->select action"""

    filename = filedialog.asksaveasfilename(
      title='Select the target file for saving records',
      defaultextension='.csv',
      filetypes=[('CSV', '*.csv *.CSV')]
    )
    if filename:
      self.model = m.CSVModel(filename=filename)

  @staticmethod
  def _simple_login(username, password):
    """A basic authentication backend with a hardcoded user and password"""
    return username == 'abq' and password == 'Flowers'

  def _show_login(self):
    """Show login dialog and attempt to login"""
    error = ''
    title = "Login to ABQ Data Entry"
    while True:
      login = v.LoginDialog(self, title, error)
      if not login.result:  # User canceled
        return False
      username, password = login.result
      if self._simple_login(username, password):
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

  def _save_settings(self, *_):
    """Save the current settings to a preferences file"""

    for key, variable in self.settings.items():
      self.settings_model.set(key, variable.get())
    self.settings_model.save()
