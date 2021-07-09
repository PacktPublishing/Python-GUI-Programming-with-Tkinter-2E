"""The Main Menu class for ABQ Data Entry"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

from . import images

class MainMenu(tk.Menu):
  """The Application's main menu"""

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
      'file_open': tk.PhotoImage(file=images.SAVE_ICON),
      'record_list': tk.PhotoImage(file=images.LIST_ICON),
      'new_record': tk.PhotoImage(file=images.FORM_ICON),
      'quit': tk.BitmapImage(file=images.QUIT_BMP, foreground='red'),
      'about': tk.BitmapImage(
          file=images.ABOUT_BMP, foreground='#CC0', background='#A09'
       ),
    }

  def __init__(self, parent, settings, **kwargs):
    """Constructor for MainMenu

    arguments:
      parent - The parent widget
      settings - a dict containing Tkinter variables
    """
    super().__init__(parent, **kwargs)
    self.settings = settings
    self._create_icons()

    # Styles
    self.styles = {
      'background': '#333',
      'foreground': 'white',
      'activebackground': '#777',
      'activeforeground': 'white',
      'relief': tk.GROOVE
    }
    self.configure(**self.styles)

    # The help menu
    help_menu = tk.Menu(self, tearoff=False, **self.styles)
    help_menu.add_command(
      label='About…',
      command=self.show_about,
      image=self.icons['about'],
      compound=tk.LEFT
    )

    # The file menu
    file_menu = tk.Menu(self, tearoff=False, **self.styles)
    file_menu.add_command(
      label="Select file…",
      command=self._event('<<FileSelect>>'),
      image=self.icons['file_open'],
      compound=tk.LEFT
    )

    file_menu.add_separator()
    file_menu.add_command(
      label="Quit",
      command=self._event('<<FileQuit>>'),
      image=self.icons['quit'],
      compound=tk.LEFT
    )

    # The options menu
    options_menu = tk.Menu(self, tearoff=False, **self.styles)
    options_menu.add_checkbutton(
      label='Autofill Date',
      variable=self.settings['autofill date']
    )
    options_menu.add_checkbutton(
      label='Autofill Sheet data',
      variable=self.settings['autofill sheet data']
    )

    size_menu = tk.Menu(options_menu, tearoff=False, **self.styles)
    options_menu.add_cascade(label='Font Size', menu=size_menu)
    for size in range(6, 17, 1):
      size_menu.add_radiobutton(
        label=size, value=size,
        variable=self.settings['font size']
      )
    family_menu = tk.Menu(options_menu, tearoff=False, **self.styles)
    options_menu.add_cascade(label='Font Family', menu=family_menu)
    for family in font.families():
      family_menu.add_radiobutton(
        label=family, value=family,
        variable=self.settings['font family']
      )

    style = ttk.Style()
    themes_menu = tk.Menu(self, tearoff=False, **self.styles)
    for theme in style.theme_names():
      themes_menu.add_radiobutton(
        label=theme, value=theme,
        variable=self.settings['theme']
      )
    options_menu.add_cascade(label='Theme', menu=themes_menu)
    self.settings['theme'].trace_add('write', self._on_theme_change)


    # switch from recordlist to recordform
    go_menu = tk.Menu(self, tearoff=False, **self.styles)
    go_menu.add_command(
      label="Record List",
      command=self._event('<<ShowRecordlist>>'),
      image=self.icons['record_list'],
      compound=tk.LEFT
    )
    go_menu.add_command(
      label="New Record",
      command=self._event('<<NewRecord>>'),
      image=self.icons['new_record'],
      compound=tk.LEFT
    )

    # add the menus in order to the main menu
    self.add_cascade(label='File', menu=file_menu)
    self.add_cascade(label='Go', menu=go_menu)
    self.add_cascade(label='Options', menu=options_menu)
    self.add_cascade(label='Help', menu=help_menu)

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
