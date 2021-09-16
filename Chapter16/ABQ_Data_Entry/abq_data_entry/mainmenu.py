"""The Main Menu class for ABQ Data Entry"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

from . import images

class GenericMainMenu(tk.Menu):
  """The Application's main menu"""

  accelerators = {
    'file_open': 'Ctrl+O',
    'quit': 'Ctrl+Q',
    'record_list': 'Ctrl+L',
    'new_record': 'Ctrl+R',
  }

  keybinds = {
    '<Control-o>': '<<FileSelect>>',
    '<Control-q>': '<<FileQuit>>',
    '<Control-n>': '<<NewRecord>>',
    '<Control-l>': '<<ShowRecordlist>>'
  }

  styles = {}

  def _event(self, sequence):
    """Return a callback function that generates the sequence"""
    def callback(*_):
      root = self.master.winfo_toplevel()
      root.event_generate(sequence)

    return callback

  def _create_icons(self):

    # must be done in a method because PhotoImage can't be created
    # until there is a Tk instance.
    # There isn't one when the class is defined, but there is when
    # the instance is created.
    self.icons = {
    #  'file_open': tk.PhotoImage(file=images.SAVE_ICON),
      'record_list': tk.PhotoImage(file=images.LIST_ICON),
      'new_record': tk.PhotoImage(file=images.FORM_ICON),
      'quit': tk.BitmapImage(file=images.QUIT_BMP, foreground='red'),
      'about': tk.BitmapImage(
          file=images.ABOUT_BMP, foreground='#CC0', background='#A09'
       ),
    }

  def _add_file_open(self, menu):

    menu.add_command(
      label='Select file…', command=self._event('<<FileSelect>>'),
      image=self.icons.get('file'), compound=tk.LEFT
  )

  def _add_quit(self, menu):
    menu.add_command(
      label='Quit', command=self._event('<<FileQuit>>'),
      image=self.icons.get('quit'), compound=tk.LEFT
    )

  def _add_weather_download(self, menu):
    menu.add_command(
      label="Update Weather Data",
      command=self._event('<<UpdateWeatherData>>'),
    )

  def _add_rest_upload(self, menu):
    menu.add_command(
      label="Upload CSV to corporate REST",
      command=self._event('<<UploadToCorporateREST>>'),
    )

  def _add_sftp_upload(self, menu):
    menu.add_command(
      label="Upload CSV to corporate SFTP",
      command=self._event('<<UploadToCorporateSFTP>>'),
    )

  def _add_autofill_date(self, menu):
    menu.add_checkbutton(
      label='Autofill Date', variable=self.settings['autofill date']
    )

  def _add_autofill_sheet(self, menu):
    menu.add_checkbutton(
      label='Autofill Sheet data',
      variable=self.settings['autofill sheet data']
    )

  def _add_font_size_menu(self, menu):
    font_size_menu = tk.Menu(self, tearoff=False, **self.styles)
    for size in range(6, 17, 1):
      font_size_menu.add_radiobutton(
        label=size, value=size,
        variable=self.settings['font size']
      )
    menu.add_cascade(label='Font size', menu=font_size_menu)

  def _add_font_family_menu(self, menu):
    font_family_menu = tk.Menu(self, tearoff=False, **self.styles)
    for family in font.families():
      font_family_menu.add_radiobutton(
        label=family, value=family,
        variable=self.settings['font family']
    )
    menu.add_cascade(label='Font family', menu=font_family_menu)

  def _add_themes_menu(self, menu):
    style = ttk.Style()
    themes_menu = tk.Menu(self, tearoff=False, **self.styles)
    for theme in style.theme_names():
      themes_menu.add_radiobutton(
        label=theme, value=theme,
        variable=self.settings['theme']
      )
    menu.add_cascade(label='Theme', menu=themes_menu)
    self.settings['theme'].trace_add('write', self._on_theme_change)

  def _add_go_record_list(self, menu):
    menu.add_command(
      label="Record List", command=self._event('<<ShowRecordlist>>'),
      image=self.icons.get('record_list'), compound=tk.LEFT
    )

  def _add_go_new_record(self, menu):
    menu.add_command(
      label="New Record", command=self._event('<<NewRecord>>'),
      image=self.icons.get('new_record'), compound=tk.LEFT
    )

  def _add_about(self, menu):
    menu.add_command(
      label='About…', command=self.show_about,
      image=self.icons.get('about'), compound=tk.LEFT
    )

  def _add_growth_chart(self, menu):
    menu.add_command(
      label='Show Growth Chart', command=self._event('<<ShowGrowthChart>>')
    )

  def _add_yield_chart(self, menu):
    menu.add_command(
      label='Show Yield Chart', command=self._event('<<ShowYieldChart>>')
    )

  def _build_menu(self):
    # The file menu
    self._menus['File'] = tk.Menu(self, tearoff=False, **self.styles)
    #self._add_file_open(self._menus['File'])
    self._menus['File'].add_separator()
    self._add_quit(self._menus['File'])

    #Tools menu
    self._menus['Tools'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_weather_download(self._menus['Tools'])
    self._add_rest_upload(self._menus['Tools'])
    self._add_sftp_upload(self._menus['Tools'])
    self._add_growth_chart(self._menus['Tools'])
    self._add_yield_chart(self._menus['Tools'])

    # The options menu
    self._menus['Options'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_autofill_date(self._menus['Options'])
    self._add_autofill_sheet(self._menus['Options'])
    self._add_font_size_menu(self._menus['Options'])
    self._add_font_family_menu(self._menus['Options'])
    self._add_themes_menu(self._menus['Options'])

    # switch from recordlist to recordform
    self._menus['Go'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_go_record_list(self._menus['Go'])
    self._add_go_new_record(self._menus['Go'])

    # The help menu
    self._menus['Help'] = tk.Menu(self, tearoff=False, **self.styles)
    self.add_cascade(label='Help', menu=self._menus['Help'])
    self._add_about(self._menus['Help'])

    for label, menu in self._menus.items():
      self.add_cascade(label=label, menu=menu)
    self.configure(**self.styles)

  def __init__(self, parent, settings, **kwargs):
    super().__init__(parent, **kwargs)
    self.settings = settings
    self._create_icons()
    self._menus = dict()
    self._build_menu()
    self._bind_accelerators()
    self.configure(**self.styles)

  def show_about(self):
    """Show the about dialog"""

    about_message = 'ABQ Data Entry'
    about_detail = (
      'by Alan D Moore\n'
      'For assistance please contact the author.'
    )

    messagebox.showinfo(
      title='About', message=about_message, detail=about_detail
    )
  @staticmethod
  def _on_theme_change(*_):
    """Popup a message about theme changes"""
    message = "Change requires restart"
    detail = (
      "Theme changes do not take effect"
      " until application restart"
    )
    messagebox.showwarning(
      title='Warning',
      message=message,
      detail=detail
    )

  def _bind_accelerators(self):

    for key, sequence in self.keybinds.items():
      self.bind_all(key, self._event(sequence))

class WindowsMainMenu(GenericMainMenu):
  """
  Changes:
   - Windows uses file->exit instead of file->quit,
     and no accelerator is used.
   - Windows can handle commands on the menubar, so
     put 'Record List' / 'New Record' on the bar
   - Windows can't handle icons on the menu bar, though
   - Put 'options' under 'Tools' with separator
  """

  def _create_icons(self):
    super()._create_icons()
    del(self.icons['new_record'])
    del(self.icons['record_list'])

  def __init__(self, *args, **kwargs):
    del(self.keybinds['<Control-q>'])
    super().__init__(*args, **kwargs)

  def _add_quit(self, menu):
    menu.add_command(
      label='Exit',
      command=self._event('<<FileQuit>>'),
      image=self.icons.get('quit'),
      compound=tk.LEFT
    )

  def _build_menu(self):
    # File Menu
    self._menus['File'] = tk.Menu(self, tearoff=False)
#    self._add_file_open(self._menus['File'])
    self._menus['File'].add_separator()
    self._add_quit(self._menus['File'])

    #Tools menu
    self._menus['Tools'] = tk.Menu(self, tearoff=False)
    self._add_autofill_date(self._menus['Tools'])
    self._add_autofill_sheet(self._menus['Tools'])
    self._add_font_size_menu(self._menus['Tools'])
    self._add_font_family_menu(self._menus['Tools'])
    self._add_themes_menu(self._menus['Tools'])
    self._add_weather_download(self._menus['Tools'])
    self._add_rest_upload(self._menus['Tools'])
    self._add_sftp_upload(self._menus['Tools'])
    self._add_growth_chart(self._menus['Tools'])
    self._add_yield_chart(self._menus['Tools'])

    # The help menu
    self._menus['Help'] = tk.Menu(self, tearoff=False)
    self._add_about(self._menus['Help'])

    # Build main menu
    self.add_cascade(label='File', menu=self._menus['File'])
    self.add_cascade(label='Tools', menu=self._menus['Tools'])
    self._add_go_record_list(self)
    self._add_go_new_record(self)
    self.add_cascade(label='Help', menu=self._menus['Help'])


class LinuxMainMenu(GenericMainMenu):
  """Differences for Linux:

    - Edit menu for autofill options
    - View menu for font & theme options
    - Use color theme for menu
  """
  styles = {
    'background': '#333',
    'foreground': 'white',
    'activebackground': '#777',
    'activeforeground': 'white',
    'relief': tk.GROOVE
  }


  def _build_menu(self):
    self._menus['File'] = tk.Menu(self, tearoff=False, **self.styles)
#    self._add_file_open(self._menus['File'])
    self._menus['File'].add_separator()
    self._add_quit(self._menus['File'])

    # The edit menu
    self._menus['Edit'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_autofill_date(self._menus['Edit'])
    self._add_autofill_sheet(self._menus['Edit'])

    #Tools menu
    self._menus['Tools'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_weather_download(self._menus['Tools'])
    self._add_rest_upload(self._menus['Tools'])
    self._add_sftp_upload(self._menus['Tools'])
    self._add_growth_chart(self._menus['Tools'])
    self._add_yield_chart(self._menus['Tools'])


    # The View menu
    self._menus['View'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_font_size_menu(self._menus['View'])
    self._add_font_family_menu(self._menus['View'])
    self._add_themes_menu(self._menus['View'])

    # switch from recordlist to recordform
    self._menus['Go'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_go_record_list(self._menus['Go'])
    self._add_go_new_record(self._menus['Go'])

    # The help menu
    self._menus['Help'] = tk.Menu(self, tearoff=False, **self.styles)
    self._add_about(self._menus['Help'])

    for label, menu in self._menus.items():
      self.add_cascade(label=label, menu=menu)


class MacOsMainMenu(GenericMainMenu):
  """
  Differences for MacOS:

    - Create App Menu
    - Move about to app menu, remove 'help'
    - Remove redundant quit command
    - Change accelerators to Command-[]
    - Add View menu for font & theme options
    - Add Edit menu for autofill options
    - Add Window menu for navigation commands
  """
  keybinds = {
      '<Command-o>': '<<FileSelect>>',
      '<Command-n>': '<<NewRecord>>',
      '<Command-l>': '<<ShowRecordlist>>'
    }
  accelerators = {
    'file_open': 'Cmd-O',
    'record_list': 'Cmd-L',
    'new_record': 'Cmd-R',
    }

  def _add_about(self, menu):
    menu.add_command(
      label='About ABQ Data Entry', command=self.show_about,
      image=self.icons.get('about'), compound=tk.LEFT
    )

  def _build_menu(self):
    self._menus['ABQ Data Entry'] = tk.Menu(
      self, tearoff=False,
      name='apple'
    )
    self._add_about(self._menus['ABQ Data Entry'])
    self._menus['ABQ Data Entry'].add_separator()

    self._menus['File'] = tk.Menu(self, tearoff=False)
#    self._add_file_open(self._menus['File'])

    self._menus['Edit'] = tk.Menu(self, tearoff=False)
    self._add_autofill_date(self._menus['Edit'])
    self._add_autofill_sheet(self._menus['Edit'])

    #Tools menu
    self._menus['Tools'] = tk.Menu(self, tearoff=False)
    self._add_weather_download(self._menus['Tools'])
    self._add_rest_upload(self._menus['Tools'])
    self._add_sftp_upload(self._menus['Tools'])
    self._add_growth_chart(self._menus['Tools'])
    self._add_yield_chart(self._menus['Tools'])

    # View menu
    self._menus['View'] = tk.Menu(self, tearoff=False)
    self._add_font_size_menu(self._menus['View'])
    self._add_font_family_menu(self._menus['View'])
    self._add_themes_menu(self._menus['View'])

    # Window Menu
    self._menus['Window'] = tk.Menu(self, name='window', tearoff=False)
    self._add_go_record_list(self._menus['Window'])
    self._add_go_new_record(self._menus['Window'])

    for label, menu in self._menus.items():
      self.add_cascade(label=label, menu=menu)


def get_main_menu_for_os(os_name):
  """Return the menu class appropriate to the given OS"""
  menus = {
    'Linux': LinuxMainMenu,
    'Darwin': MacOsMainMenu,
    'freebsd7': LinuxMainMenu,
    'Windows': WindowsMainMenu
  }

  return menus.get(os_name, GenericMainMenu)
