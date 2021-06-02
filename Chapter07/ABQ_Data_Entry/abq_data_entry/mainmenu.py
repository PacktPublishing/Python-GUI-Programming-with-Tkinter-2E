"""The Main Menu class for ABQ Data Entry"""

import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
  """The Application's main menu"""

  def _event(self, sequence):
    """Return a callback function that generates the sequence"""
    def callback(*_):
      root = self.master.winfo_toplevel()
      root.event_generate(sequence)

    return callback

  def __init__(self, parent, settings, **kwargs):
    """Constructor for MainMenu

    arguments:
      parent - The parent widget
      settings - a dict containing Tkinter variables
    """
    super().__init__(parent, **kwargs)
    self.settings = settings

    # The help menu
    help_menu = tk.Menu(self, tearoff=False)
    help_menu.add_command(label='About…', command=self.show_about)

    # The file menu
    file_menu = tk.Menu(self, tearoff=False)
    file_menu.add_command(
      label="Select file…",
      command=self._event('<<FileSelect>>')
    )

    file_menu.add_separator()
    file_menu.add_command(
      label="Quit",
      command=self._event('<<FileQuit>>')
    )

    # The options menu
    options_menu = tk.Menu(self, tearoff=False)
    options_menu.add_checkbutton(
      label='Autofill Date',
      variable=self.settings['autofill date']
    )
    options_menu.add_checkbutton(
      label='Autofill Sheet data',
      variable=self.settings['autofill sheet data']
    )

    # add the menus in order to the main menu
    self.add_cascade(label='File', menu=file_menu)
    self.add_cascade(label='Options', menu=options_menu)
    self.add_cascade(label='Help', menu=help_menu)


  def show_about(self):
    """Show the about dialog"""

    about_message = 'ABQ Data Entry'
    about_detail = (
      'by Alan D Moore\n'
      'For assistance please contact the author.'
    )

    messagebox.showinfo(title='About', message=about_message, detail=about_detail)
