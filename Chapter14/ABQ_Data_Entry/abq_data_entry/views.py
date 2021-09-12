import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from datetime import datetime
from . import widgets as w
from .constants import FieldTypes as FT
from . import images

class DataRecordForm(tk.Frame):
  """The input form for our widgets"""

  var_types = {
    FT.string: tk.StringVar,
    FT.string_list: tk.StringVar,
    FT.short_string_list: tk.StringVar,
    FT.iso_date_string: tk.StringVar,
    FT.long_string: tk.StringVar,
    FT.decimal: tk.DoubleVar,
    FT.integer: tk.IntVar,
    FT.boolean: tk.BooleanVar
  }

  def _add_frame(self, label, style='', cols=3):
    """Add a labelframe to the form"""

    frame = ttk.LabelFrame(self, text=label)
    if style:
      frame.configure(style=style)
    frame.grid(sticky=tk.W + tk.E)
    for i in range(cols):
      frame.columnconfigure(i, weight=1)
    return frame

  def __init__(self, parent, model, settings, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.model= model
    self.settings = settings
    fields = self.model.fields

    # new for ch9
    style = ttk.Style()

    # Frame styles
    style.configure(
      'RecordInfo.TLabelframe',
      background='khaki', padx=10, pady=10
    )
    style.configure(
      'EnvironmentInfo.TLabelframe', background='lightblue',
      padx=10, pady=10
    )
    style.configure(
      'PlantInfo.TLabelframe',
      background='lightgreen', padx=10, pady=10
    )
    # Style the label Element as well
    style.configure(
      'RecordInfo.TLabelframe.Label', background='khaki',
      padx=10, pady=10
    )
    style.configure(
      'EnvironmentInfo.TLabelframe.Label',
      background='lightblue', padx=10, pady=10
    )
    style.configure(
      'PlantInfo.TLabelframe.Label',
      background='lightgreen', padx=10, pady=10
    )

    # Style for the form labels and buttons
    style.configure('RecordInfo.TLabel', background='khaki')
    style.configure('RecordInfo.TRadiobutton', background='khaki')
    style.configure('EnvironmentInfo.TLabel', background='lightblue')
    style.configure(
      'EnvironmentInfo.TCheckbutton',
      background='lightblue'
    )
    style.configure('PlantInfo.TLabel', background='lightgreen')


    # Create a dict to keep track of input widgets
    self._vars = {
      key: self.var_types[spec['type']]()
      for key, spec in fields.items()
    }

    # Build the form
    self.columnconfigure(0, weight=1)

    # new chapter 8
    # variable to track current record id
    self.current_record = None

    # Label for displaying what record we're editing
    self.record_label = ttk.Label(self)
    self.record_label.grid(row=0, column=0)

    # Record info section
    r_info = self._add_frame(
      "Record Information", 'RecordInfo.TLabelframe'
    )

    # line 1
    w.LabelInput(
      r_info, "Date",
      field_spec=fields['Date'],
      var=self._vars['Date'],
      label_args={'style': 'RecordInfo.TLabel'}
    ).grid(row=0, column=0)
    w.LabelInput(
      r_info, "Time",
      field_spec=fields['Time'],
      var=self._vars['Time'],
      label_args={'style': 'RecordInfo.TLabel'}
    ).grid(row=0, column=1)
    # swap order for chapter 12
    w.LabelInput(
      r_info, "Lab",
      field_spec=fields['Lab'],
      var=self._vars['Lab'],
      label_args={'style': 'RecordInfo.TLabel'},
      input_args={'style': 'RecordInfo.TRadiobutton'}
    ).grid(row=0, column=2)
    # line 2
    w.LabelInput(
      r_info, "Plot",
      field_spec=fields['Plot'],
      var=self._vars['Plot'],
      label_args={'style': 'RecordInfo.TLabel'}
    ).grid(row=1, column=0)
    w.LabelInput(
      r_info, "Technician",
      field_spec=fields['Technician'],
      var=self._vars['Technician'],
      label_args={'style': 'RecordInfo.TLabel'}
    ).grid(row=1, column=1)
    w.LabelInput(
      r_info, "Seed Sample",
      field_spec=fields['Seed Sample'],
      var=self._vars['Seed Sample'],
      label_args={'style': 'RecordInfo.TLabel'}
    ).grid(row=1, column=2)


    # Environment Data
    e_info = self._add_frame(
      "Environment Data", 'EnvironmentInfo.TLabelframe'
    )

    e_info = ttk.LabelFrame(
      self,
      text="Environment Data",
      style='EnvironmentInfo.TLabelframe'
      )
    e_info.grid(row=2, column=0, sticky="we")
    w.LabelInput(
      e_info, "Humidity (g/m³)",
      field_spec=fields['Humidity'],
      var=self._vars['Humidity'],
      disable_var=self._vars['Equipment Fault'],
      label_args={'style': 'EnvironmentInfo.TLabel'}
    ).grid(row=0, column=0)
    w.LabelInput(
      e_info, "Light (klx)",
      field_spec=fields['Light'],
      var=self._vars['Light'],
      disable_var=self._vars['Equipment Fault'],
      label_args={'style': 'EnvironmentInfo.TLabel'}
    ).grid(row=0, column=1)
    w.LabelInput(
      e_info, "Temperature (°C)",
      field_spec=fields['Temperature'],
      disable_var=self._vars['Equipment Fault'],
      var=self._vars['Temperature'],
      label_args={'style': 'EnvironmentInfo.TLabel'}
    ).grid(row=0, column=2)
    w.LabelInput(
      e_info, "Equipment Fault",
      field_spec=fields['Equipment Fault'],
      var=self._vars['Equipment Fault'],
      label_args={'style': 'EnvironmentInfo.TLabel'},
      input_args={'style': 'EnvironmentInfo.TCheckbutton'}
    ).grid(row=1, column=0, columnspan=3)

    # Plant Data section
    p_info = self._add_frame("Plant Data", 'PlantInfo.TLabelframe')

    w.LabelInput(
      p_info, "Plants",
      field_spec=fields['Plants'],
      var=self._vars['Plants'],
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=0, column=0)
    w.LabelInput(
      p_info, "Blossoms",
      field_spec=fields['Blossoms'],
      var=self._vars['Blossoms'],
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=0, column=1)
    w.LabelInput(
      p_info, "Fruit",
      field_spec=fields['Fruit'],
      var=self._vars['Fruit'],
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=0, column=2)
    # Height data
    # create variables to be updated for min/max height
    # they can be referenced for min/max variables
    min_height_var = tk.DoubleVar(value='-infinity')
    max_height_var = tk.DoubleVar(value='infinity')

    w.LabelInput(
      p_info, "Min Height (cm)",
      field_spec=fields['Min Height'],
      var=self._vars['Min Height'],
      input_args={"max_var": max_height_var,
            "focus_update_var": min_height_var},
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=1, column=0)
    w.LabelInput(
      p_info, "Max Height (cm)",
      field_spec=fields['Max Height'],
      var=self._vars['Max Height'],
      input_args={"min_var": min_height_var,
            "focus_update_var": max_height_var},
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=1, column=1)
    w.LabelInput(
      p_info, "Median Height (cm)",
      field_spec=fields['Med Height'],
      var=self._vars['Med Height'],
      input_args={"min_var": min_height_var,
            "max_var": max_height_var},
      label_args={'style': 'PlantInfo.TLabel'}
    ).grid(row=1, column=2)


    # Notes section  -- Update grid row value for ch8
    w.LabelInput(
      self, "Notes", field_spec=fields['Notes'],
      var=self._vars['Notes'], input_args={"width": 85, "height": 10}
    ).grid(sticky="nsew", row=4, column=0, padx=10, pady=10)

    # buttons
    buttons = tk.Frame(self)
    buttons.grid(sticky=tk.W + tk.E, row=5)
    self.save_button_logo = tk.PhotoImage(file=images.SAVE_ICON)
    self.savebutton = ttk.Button(
      buttons, text="Save", command=self._on_save,
      image=self.save_button_logo, compound=tk.LEFT
    )
    self.savebutton.pack(side=tk.RIGHT)

    self.reset_button_logo = tk.PhotoImage(file=images.RESET_ICON)
    self.resetbutton = ttk.Button(
      buttons, text="Reset", command=self.reset,
      image=self.reset_button_logo, compound=tk.LEFT
    )
    self.resetbutton.pack(side=tk.RIGHT)

    # new for ch12
    # Triggers
    for field in ('Lab', 'Plot'):
      self._vars[field].trace_add(
        'write', self._populate_current_seed_sample)

    for field in ('Date', 'Time', 'Lab'):
      self._vars[field].trace_add(
        'write', self._populate_tech_for_lab_check)

    # default the form
    self.reset()

  def _on_save(self):
    self.event_generate('<<SaveRecord>>')

  @staticmethod
  def tclerror_is_blank_value(exception):
    blank_value_errors = (
      'expected integer but got ""',
      'expected floating-point number but got ""',
      'expected boolean value but got ""'
    )
    is_bve = str(exception).strip() in blank_value_errors
    return is_bve

  def get(self):
    """Retrieve data from form as a dict"""

    # We need to retrieve the data from Tkinter variables
    # and place it in regular Python objects
    data = dict()
    for key, var in self._vars.items():
      try:
        data[key] = var.get()
      except tk.TclError as e:
        if self.tclerror_is_blank_value(e):
          data[key] = None
        else:
          raise e
    return data

  def reset(self):
    """Resets the form entries"""

    lab = self._vars['Lab'].get()
    time = self._vars['Time'].get()
    technician = self._vars['Technician'].get()
    try:
      plot = self._vars['Plot'].get()
    except tk.TclError:
      plot = ''
    plot_values = self._vars['Plot'].label_widget.input.cget('values')

    # clear all values
    for var in self._vars.values():
      if isinstance(var, tk.BooleanVar):
        var.set(False)
      else:
        var.set('')

    # Autofill Date
    if self.settings['autofill date'].get():
      current_date = datetime.today().strftime('%Y-%m-%d')
      self._vars['Date'].set(current_date)
      self._vars['Time'].label_widget.input.focus()

    # check if we need to put our values back, then do it.
    if (
      self.settings['autofill sheet data'].get() and
      plot not in ('', 0, plot_values[-1])
    ):
      self._vars['Lab'].set(lab)
      self._vars['Time'].set(time)
      self._vars['Technician'].set(technician)
      next_plot_index = plot_values.index(plot) + 1
      self._vars['Plot'].set(plot_values[next_plot_index])
      self._vars['Seed Sample'].label_widget.input.focus()

  def get_errors(self):
    """Get a list of field errors in the form"""

    errors = dict()
    for key, var in self._vars.items():
      inp = var.label_widget.input
      error = var.label_widget.error

      if hasattr(inp, 'trigger_focusout_validation'):
        inp.trigger_focusout_validation()
      if error.get():
        errors[key] = error.get()

    return errors

  # rewrite for ch12
  def load_record(self, rowkey, data=None):
    """Load a record's data into the form"""
    self.current_record = rowkey
    if rowkey is None:
      self.reset()
      self.record_label.config(text='New Record')
    else:
      date, time, lab, plot = rowkey
      title = f'Record for Lab {lab}, Plot {plot} at {date} {time}'
      self.record_label.config(text=title)
      for key, var in self._vars.items():
        var.set(data.get(key, ''))
        try:
          var.label_widget.input.trigger_focusout_validation()
        except AttributeError:
          pass

  # new for ch12

  def _populate_current_seed_sample(self, *_):
    """Auto-populate the current seed sample for Lab and Plot"""
    if not self.settings['autofill sheet data'].get():
      return
    plot = self._vars['Plot'].get()
    lab = self._vars['Lab'].get()

    if plot and lab:
      seed = self.model.get_current_seed_sample(lab, plot)
      self._vars['Seed Sample'].set(seed)

  def _populate_tech_for_lab_check(self, *_):
    """Populate technician based on the current lab check"""
    if not self.settings['autofill sheet data'].get():
      return
    date = self._vars['Date'].get()
    try:
      datetime.fromisoformat(date)
    except ValueError:
      return
    time = self._vars['Time'].get()
    lab = self._vars['Lab'].get()

    if all([date, time, lab]):
      check = self.model.get_lab_check(date, time, lab)
      tech = check['lab_tech'] if check else ''
      self._vars['Technician'].set(tech)


class LoginDialog(Dialog):
  """A dialog that asks for username and password"""

  def __init__(self, parent, title, error=''):

    self._pw = tk.StringVar()
    self._user = tk.StringVar()
    self._error = tk.StringVar(value=error)
    super().__init__(parent, title=title)

  def body(self, frame):
    """Construct the interface and return the widget for initial focus

    Overridden from Dialog
    """
    ttk.Label(frame, text='Login to ABQ').grid(row=0)

    if self._error.get():
      ttk.Label(frame, textvariable=self._error).grid(row=1)
    user_inp = w.LabelInput(
      frame, 'User name:', input_class=w.RequiredEntry,
      var=self._user
    )
    user_inp.grid()
    w.LabelInput(
      frame, 'Password:', input_class=w.RequiredEntry,
      input_args={'show': '*'}, var=self._pw
    ).grid()
    return user_inp.input

  def buttonbox(self):
    box = ttk.Frame(self)
    ttk.Button(
      box, text="Login", command=self.ok, default=tk.ACTIVE
    ).grid(padx=5, pady=5)
    ttk.Button(
      box, text="Cancel", command=self.cancel
    ).grid(row=0, column=1, padx=5, pady=5)
    self.bind("<Return>", self.ok)
    self.bind("<Escape>", self.cancel)
    box.pack()


  def apply(self):
    self.result = (self._user.get(), self._pw.get())


class RecordList(tk.Frame):
  """Display for CSV file contents"""

  column_defs = {
    '#0': {'label': 'Row', 'anchor': tk.W},
    'Date': {'label': 'Date', 'width': 150, 'stretch': True},
    'Time': {'label': 'Time'},
    'Lab': {'label': 'Lab', 'width': 40},
    'Plot': {'label': 'Plot', 'width': 80}
  }
  default_width = 100
  default_minwidth = 10
  default_anchor = tk.CENTER

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    self._inserted = list()
    self._updated = list()
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)

    # New ch12
    self.iid_map = dict()

    # create treeview
    self.treeview = ttk.Treeview(
      self,
      columns=list(self.column_defs.keys())[1:],
      selectmode='browse'
    )
    self.treeview.grid(row=0, column=0, sticky='NSEW')

    # Configure treeview columns
    for name, definition in self.column_defs.items():
      label = definition.get('label', '')
      anchor = definition.get('anchor', self.default_anchor)
      minwidth = definition.get('minwidth', self.default_minwidth)
      width = definition.get('width', self.default_width)
      stretch = definition.get('stretch', False)
      self.treeview.heading(name, text=label, anchor=anchor)
      self.treeview.column(
        name, anchor=anchor, minwidth=minwidth,
        width=width, stretch=stretch
        )

    self.treeview.bind('<Double-1>', self._on_open_record)
    self.treeview.bind('<Return>', self._on_open_record)

    # configure scrollbar for the treeview
    self.scrollbar = ttk.Scrollbar(
      self,
      orient=tk.VERTICAL,
      command=self.treeview.yview
    )
    self.treeview.configure(yscrollcommand=self.scrollbar.set)
    self.scrollbar.grid(row=0, column=1, sticky='NSW')

    # configure tagging
    self.treeview.tag_configure('inserted', background='lightgreen')
    self.treeview.tag_configure('updated', background='lightblue')

    # For ch12, hide first column since row # is no longer meaningful
    self.treeview.config(show='headings')

  # new for ch12

  # update for ch12
  def populate(self, rows):
    """Clear the treeview and write the supplied data rows to it."""

    for row in self.treeview.get_children():
      self.treeview.delete(row)

    self.iid_map.clear()

    cids = list(self.column_defs.keys())[1:]
    for rowdata in rows:
      values = [rowdata[key] for key in cids]
      rowkey = tuple([str(v) for v in values])
      if rowkey in self._inserted:
        tag = 'inserted'
      elif rowkey in self._updated:
        tag = 'updated'
      else:
        tag = ''
      # new ch12 -- save generated IID, assign to rowkey
      iid = self.treeview.insert(
        '', 'end', values=values, tag=tag)
      self.iid_map[iid] = rowkey

    if len(rows) > 0:
      firstrow = self.treeview.identify_row(0)
      self.treeview.focus_set()
      self.treeview.selection_set(firstrow)
      self.treeview.focus(firstrow)

  # update for ch12
  def _on_open_record(self, *_):
    """Handle record open request"""
    self.event_generate('<<OpenRecord>>')

  @property
  def selected_id(self):
    selection = self.treeview.selection()
    return self.iid_map[selection[0]] if selection else None


  def add_updated_row(self, row):
    if row not in self._updated:
      self._updated.append(row)

  def add_inserted_row(self, row):
    if row not in self._inserted:
      self._inserted.append(row)

  def clear_tags(self):
    self._inserted.clear()
    self._updated.clear()
