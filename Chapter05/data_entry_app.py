"""ABQ Data Entry

Chapter 5 version
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path
import csv
from decimal import Decimal, InvalidOperation


##################
# Widget Classes #
##################

class ValidatedMixin:
  """Adds a validation functionality to an input widget"""

  def __init__(self, *args, error_var=None, **kwargs):
    self.error = error_var or tk.StringVar()
    super().__init__(*args, **kwargs)

    vcmd = self.register(self._validate)
    invcmd = self.register(self._invalid)

    self.configure(
      validate='all',
      validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
      invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
    )

  def _toggle_error(self, on=False):
    self.configure(foreground=('red' if on else 'black'))

  def _validate(self, proposed, current, char, event, index, action):
    """The validation method.

    Don't override this, override _key_validate, and _focus_validate
    """
    self.error.set('')
    self._toggle_error()

    valid = True
    # if the widget is disabled, don't validate
    state = str(self.configure('state')[-1])
    if state == tk.DISABLED:
      return valid

    if event == 'focusout':
      valid = self._focusout_validate(event=event)
    elif event == 'key':
      valid = self._key_validate(
      proposed=proposed,
      current=current,
      char=char,
      event=event,
      index=index,
      action=action
    )
    return valid

  def _focusout_validate(self, **kwargs):
    return True

  def _key_validate(self, **kwargs):
    return True

  def _invalid(self, proposed, current, char, event, index, action):
    if event == 'focusout':
      self._focusout_invalid(event=event)
    elif event == 'key':
      self._key_invalid(
        proposed=proposed,
        current=current,
        char=char,
        event=event,
        index=index,
        action=action
      )

  def _focusout_invalid(self, **kwargs):
    """Handle invalid data on a focus event"""
    self._toggle_error(True)

  def _key_invalid(self, **kwargs):
    """Handle invalid data on a key event.  By default we want to do nothing"""
    pass

  def trigger_focusout_validation(self):
    valid = self._validate('', '', '', 'focusout', '', '')
    if not valid:
      self._focusout_invalid(event='focusout')
    return valid



class RequiredEntry(ValidatedMixin, ttk.Entry):
  """An Entry that requires a value"""

  def _focusout_validate(self, event):
    valid = True
    if not self.get():
      valid = False
      self.error.set('A value is required')
    return valid


class DateEntry(ValidatedMixin, ttk.Entry):
  """An Entry that only accepts ISO Date strings"""

  def _key_validate(self, action, index, char, **kwargs):
    valid = True

    if action == '0':  # This is a delete action
      valid = True
    elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
      valid = char.isdigit()
    elif index in ('4', '7'):
      valid = char == '-'
    else:
      valid = False
    return valid

  def _focusout_validate(self, event):
    valid = True
    if not self.get():
      self.error.set('A value is required')
      valid = False
    try:
      datetime.strptime(self.get(), '%Y-%m-%d')
    except ValueError:
      self.error.set('Invalid date')
      valid = False
    return valid


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):
  """A combobox that only takes values from its string list"""

  def _key_validate(self, proposed, action, **kwargs):
    valid = True
    # if the user tries to delete,
    # just clear the field
    if action == '0':
      self.set('')
      return True

    # get our values list
    values = self.cget('values')
    # Do a case-insensitive match against the entered text
    matching = [
      x for x in values
      if x.lower().startswith(proposed.lower())
    ]
    if len(matching) == 0:
      valid = False
    elif len(matching) == 1:
      self.set(matching[0])
      self.icursor(tk.END)
      valid = False
    return valid

  def _focusout_validate(self, **kwargs):
    valid = True
    if not self.get():
      valid = False
      self.error.set('A value is required')
    return valid


class ValidatedSpinbox(ValidatedMixin, ttk.Spinbox):
  """A Spinbox that only accepts Numbers"""

  def __init__(self, *args, min_var=None, max_var=None,
    focus_update_var=None, from_='-Infinity', to='Infinity', **kwargs
   ):
    super().__init__(*args, from_=from_, to=to, **kwargs)
    increment = Decimal(str(kwargs.get('increment', '1.0')))
    self.precision = increment.normalize().as_tuple().exponent
    # there should always be a variable,
    # or some of our code will fail
    self.variable = kwargs.get('textvariable')
    if not self.variable:
      self.variable = tk.DoubleVar()
      self.configure(textvariable=self.variable)

    if min_var:
      self.min_var = min_var
      self.min_var.trace_add('write', self._set_minimum)
    if max_var:
      self.max_var = max_var
      self.max_var.trace_add('write', self._set_maximum)
    self.focus_update_var = focus_update_var
    self.bind('<FocusOut>', self._set_focus_update_var)

  def _set_focus_update_var(self, event):
    value = self.get()
    if self.focus_update_var and not self.error.get():
      self.focus_update_var.set(value)

  def _set_minimum(self, *_):
    current = self.get()
    try:
      new_min = self.min_var.get()
      self.config(from_=new_min)
    except (tk.TclError, ValueError):
      pass
    if not current:
      self.delete(0, tk.END)
    else:
      self.variable.set(current)
    self.trigger_focusout_validation()

  def _set_maximum(self, *_):
    current = self.get()
    try:
      new_max = self.max_var.get()
      self.config(to=new_max)
    except (tk.TclError, ValueError):
      pass
    if not current:
      self.delete(0, tk.END)
    else:
      self.variable.set(current)
    self.trigger_focusout_validation()

  def _key_validate(
    self, char, index, current, proposed, action, **kwargs
  ):
    if action == '0':
      return True
    valid = True
    min_val = self.cget('from')
    max_val = self.cget('to')
    no_negative = min_val >= 0
    no_decimal = self.precision >= 0

    # First, filter out obviously invalid keystrokes
    if any([
        (char not in '-1234567890.'),
        (char == '-' and (no_negative or index != '0')),
        (char == '.' and (no_decimal or '.' in current))
    ]):
      return False

    # At this point, proposed is either '-', '.', '-.',
    # or a valid Decimal string
    if proposed in '-.':
      return True

    # Proposed is a valid Decimal string
    # convert to Decimal and check more:
    proposed = Decimal(proposed)
    proposed_precision = proposed.as_tuple().exponent

    if any([
      (proposed > max_val),
      (proposed_precision < self.precision)
    ]):
      return False

    return valid

  def _focusout_validate(self, **kwargs):
    valid = True
    value = self.get()
    min_val = self.cget('from')
    max_val = self.cget('to')

    try:
      d_value = Decimal(value)
    except InvalidOperation:
      self.error.set(f'Invalid number string: {value}')
      return False

    if d_value < min_val:
      self.error.set(f'Value is too low (min {min_val})')
      valid = False
    if d_value > max_val:
      self.error.set(f'Value is too high (max {max_val})')
      valid = False

    return valid


class ValidatedRadioGroup(ttk.Frame):
  """A validated radio button group"""

  def __init__(
    self, *args, variable=None, error_var=None,
    values=None, button_args=None, **kwargs
  ):
    super().__init__(*args, **kwargs)
    self.variable = variable or tk.StringVar()
    self.error = error_var or tk.StringVar()
    self.values = values or list()
    button_args = button_args or dict()

    for v in self.values:
      button = ttk.Radiobutton(
        self, value=v, text=v, variable=self.variable, **button_args
      )
      button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
    self.bind('<FocusOut>', self.trigger_focusout_validation)

  def trigger_focusout_validation(self, *_):
    self.error.set('')
    if not self.variable.get():
      self.error.set('A value is required')


class BoundText(tk.Text):
  """A Text widget with a bound variable."""

  def __init__(self, *args, textvariable=None, **kwargs):
    super().__init__(*args, **kwargs)
    self._variable = textvariable
    if self._variable:
      # insert any default value
      self.insert('1.0', self._variable.get())
      self._variable.trace_add('write', self._set_content)
      self.bind('<<Modified>>', self._set_var)

  def _set_var(self, *_):
    """Set the variable to the text contents"""
    if self.edit_modified():
      content = self.get('1.0', 'end-1chars')
      self._variable.set(content)
      self.edit_modified(False)

  def _set_content(self, *_):
    """Set the text contents to the variable"""
    self.delete('1.0', tk.END)
    self.insert('1.0', self._variable.get())

##################
# Module Classes #
##################


class LabelInput(ttk.Frame):
  """A widget containing a label and input together."""

  def __init__(
    self, parent, label, var, input_class=ttk.Entry,
      input_args=None, label_args=None, disable_var=None,
      **kwargs
  ):
    super().__init__(parent, **kwargs)
    input_args = input_args or {}
    label_args = label_args or {}
    self.variable = var
    self.variable.label_widget = self

    # setup the label
    if input_class in (ttk.Checkbutton, ttk.Button):
      # Buttons don't need labels, they're built-in
      input_args["text"] = label
    else:
      self.label = ttk.Label(self, text=label, **label_args)
      self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

    # setup the variable
    if input_class in (
      ttk.Checkbutton, ttk.Button,
      ttk.Radiobutton, ValidatedRadioGroup
    ):
      input_args["variable"] = self.variable
    else:
      input_args["textvariable"] = self.variable

    # Setup the input
    if input_class == ttk.Radiobutton:
      # for Radiobutton, create one input per value
      self.input = tk.Frame(self)
      for v in input_args.pop('values', []):
        button = input_class(
          self.input, value=v, text=v, **input_args
        )
        button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
    else:
      self.input = input_class(self, **input_args)
    self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
    self.columnconfigure(0, weight=1)

    # Set up error handling & display
    self.error = getattr(self.input, 'error', tk.StringVar())
    ttk.Label(self, textvariable=self.error).grid(
      row=2, column=0, sticky=(tk.W + tk.E)
    )

    # Set up disable variable
    if disable_var:
      self.disable_var = disable_var
      self.disable_var.trace_add('write', self._check_disable)

  def _check_disable(self, *_):
    if not hasattr(self, 'disable_var'):
      return

    if self.disable_var.get():
      self.input.configure(state=tk.DISABLED)
      self.variable.set('')
      self.error.set('')
    else:
      self.input.configure(state=tk.NORMAL)

  def grid(self, sticky=(tk.E + tk.W), **kwargs):
    """Override grid to add default sticky values"""
    super().grid(sticky=sticky, **kwargs)


class DataRecordForm(tk.Frame):
  """The input form for our widgets"""

  def _add_frame(self, label, cols=3):
    """Add a labelframe to the form"""

    frame = ttk.LabelFrame(self, text=label)
    frame.grid(sticky=tk.W + tk.E)
    for i in range(cols):
      frame.columnconfigure(i, weight=1)
    return frame

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Create a dict to keep track of input widgets
    self._vars = {
      'Date': tk.StringVar(),
      'Time': tk.StringVar(),
      'Technician': tk.StringVar(),
      'Lab': tk.StringVar(),
      'Plot': tk.IntVar(),
      'Seed Sample': tk.StringVar(),
      'Humidity': tk.DoubleVar(),
      'Light': tk.DoubleVar(),
      'Temperature': tk.DoubleVar(),
      'Equipment Fault': tk.BooleanVar(),
      'Plants': tk.IntVar(),
      'Blossoms': tk.IntVar(),
      'Fruit': tk.IntVar(),
      'Min Height': tk.DoubleVar(),
      'Max Height': tk.DoubleVar(),
      'Med Height': tk.DoubleVar(),
      'Notes': tk.StringVar()
    }

    # Build the form
    self.columnconfigure(0, weight=1)

    # Record info section
    r_info = self._add_frame("Record Information")

    # line 1
    LabelInput(
      r_info, "Date", var=self._vars['Date'], input_class=DateEntry
    ).grid(row=0, column=0)
    LabelInput(
      r_info, "Time", input_class=ValidatedCombobox,
      var=self._vars['Time'],
      input_args={"values": ["8:00", "12:00", "16:00", "20:00"]}
    ).grid(row=0, column=1)
    LabelInput(
      r_info, "Technician",  var=self._vars['Technician'],
      input_class=RequiredEntry
    ).grid(row=0, column=2)

    # line 2
    LabelInput(
      r_info, "Lab", input_class=ValidatedRadioGroup,
      var=self._vars['Lab'], input_args={"values": ["A", "B", "C"]}
    ).grid(row=1, column=0)
    LabelInput(
      r_info, "Plot", input_class=ValidatedCombobox,
      var=self._vars['Plot'], input_args={"values": list(range(1, 21))}
    ).grid(row=1, column=1)
    LabelInput(
      r_info, "Seed Sample",  var=self._vars['Seed Sample'],
      input_class=RequiredEntry
    ).grid(row=1, column=2)


    # Environment Data
    e_info = self._add_frame("Environment Data")

    LabelInput(
      e_info, "Humidity (g/m³)",
      input_class=ValidatedSpinbox,  var=self._vars['Humidity'],
      input_args={"from_": 0.5, "to": 52.0, "increment": .01},
      disable_var=self._vars['Equipment Fault']
    ).grid(row=0, column=0)
    LabelInput(
      e_info, "Light (klx)", input_class=ValidatedSpinbox,
      var=self._vars['Light'],
      input_args={"from_": 0, "to": 100, "increment": .01},
      disable_var=self._vars['Equipment Fault']
    ).grid(row=0, column=1)
    LabelInput(
      e_info, "Temperature (°C)",
      input_class=ValidatedSpinbox,  var=self._vars['Temperature'],
      input_args={"from_": 4, "to": 40, "increment": .01},
      disable_var=self._vars['Equipment Fault']
    ).grid(row=0, column=2)
    LabelInput(
      e_info, "Equipment Fault",
      input_class=ttk.Checkbutton,  var=self._vars['Equipment Fault']
    ).grid(row=1, column=0, columnspan=3)


    # Plant Data section
    p_info = self._add_frame("Plant Data")

    LabelInput(
      p_info, "Plants", input_class=ValidatedSpinbox,
      var=self._vars['Plants'], input_args={"from_": 0, "to": 20}
    ).grid(row=0, column=0)
    LabelInput(
      p_info, "Blossoms", input_class=ValidatedSpinbox,
      var=self._vars['Blossoms'], input_args={"from_": 0, "to": 1000}
    ).grid(row=0, column=1)
    LabelInput(
      p_info, "Fruit", input_class=ValidatedSpinbox,
      var=self._vars['Fruit'], input_args={"from_": 0, "to": 1000}
    ).grid(row=0, column=2)

    # Height data
    # create variables to be updated for min/max height
    # they can be referenced for min/max variables
    min_height_var = tk.DoubleVar(value='-infinity')
    max_height_var = tk.DoubleVar(value='infinity')

    LabelInput(
      p_info, "Min Height (cm)",
      input_class=ValidatedSpinbox,  var=self._vars['Min Height'],
      input_args={
        "from_": 0, "to": 1000, "increment": .01,
        "max_var": max_height_var, "focus_update_var": min_height_var
        }
    ).grid(row=1, column=0)
    LabelInput(
      p_info, "Max Height (cm)",
      input_class=ValidatedSpinbox,  var=self._vars['Max Height'],
      input_args={
        "from_": 0, "to": 1000, "increment": .01,
        "min_var": min_height_var, "focus_update_var": max_height_var
        }
    ).grid(row=1, column=1)
    LabelInput(
      p_info, "Median Height (cm)",
      input_class=ValidatedSpinbox,  var=self._vars['Med Height'],
      input_args={
        "from_": 0, "to": 1000, "increment": .01,
        "min_var": min_height_var, "max_var": max_height_var
        }
    ).grid(row=1, column=2)


    # Notes section
    LabelInput(
      self, "Notes",
      input_class=BoundText,  var=self._vars['Notes'],
      input_args={"width": 75, "height": 10}
    ).grid(sticky=(tk.W + tk.E), row=3, column=0)

    # buttons
    buttons = tk.Frame(self)
    buttons.grid(sticky=tk.W + tk.E, row=4)
    self.savebutton = ttk.Button(
      buttons, text="Save", command=self.master._on_save)
    self.savebutton.pack(side=tk.RIGHT)

    self.resetbutton = ttk.Button(
      buttons, text="Reset", command=self.reset)
    self.resetbutton.pack(side=tk.RIGHT)

    # default the form
    self.reset()

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
    plot_values = (
      self._vars['Plot'].label_widget.input.cget('values')
    )

    # clear all values
    for var in self._vars.values():
      if isinstance(var, tk.BooleanVar):
        var.set(False)
      else:
        var.set('')

    # Autofill Date
    current_date = datetime.today().strftime('%Y-%m-%d')
    self._vars['Date'].set(current_date)
    self._vars['Time'].label_widget.input.focus()

    # check if we need to put our values back, then do it.
    if plot not in ('', 0, plot_values[-1]):
      self._vars['Lab'].set(lab)
      self._vars['Time'].set(time)
      self._vars['Technician'].set(technician)
      next_plot_index = plot_values.index(str(plot)) + 1
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


class Application(tk.Tk):
  """Application root window"""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.title("ABQ Data Entry Application")
    self.columnconfigure(0, weight=1)

    ttk.Label(
      self,
      text="ABQ Data Entry Application",
      font=("TkDefaultFont", 16)
    ).grid(row=0)


    self.recordform = DataRecordForm(self)
    self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))

    # status bar
    self.status = tk.StringVar()
    ttk.Label(
      self, textvariable=self.status
    ).grid(sticky=(tk.W + tk.E), row=3, padx=10)

    self._records_saved = 0

  def _on_save(self):
    """Handles save button clicks"""

    # Check for errors first

    errors = self.recordform.get_errors()
    if errors:
      self.status.set(
        "Cannot save, error in fields: {}"
        .format(', '.join(errors.keys()))
      )
      return

    # For now, we save to a hardcoded filename with a datestring.
    # If it doesnt' exist, create it,
    # otherwise just append to the existing file
    datestring = datetime.today().strftime("%Y-%m-%d")
    filename = f"abq_data_record_{datestring}.csv"
    newfile = not Path(filename).exists()

    data = self.recordform.get()

    with open(filename, 'a') as fh:
      csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
      if newfile:
        csvwriter.writeheader()
      csvwriter.writerow(data)

    self._records_saved += 1
    self.status.set(
      f"{self._records_saved} records saved this session"
    )
    self.recordform.reset()


if __name__ == "__main__":

  app = Application()
  app.mainloop()
