"""Demonstration of using classes with tkinter"""
import tkinter as tk
import json


#############################
# Improving Tkinter classes #
#############################

# Create a JSONVar

class JSONVar(tk.StringVar):
  """A Tk variable that can hold dicts and lists"""

  def __init__(self, *args, **kwargs):
    kwargs['value'] = json.dumps(kwargs.get('value'))
    super().__init__(*args, **kwargs)

  def set(self, value, *args, **kwargs):
    string = json.dumps(value)
    super().set(string, *args, **kwargs)

  def get(self, *args, **kwargs):
    """Get the list or dict value"""
    string = super().get(*args, **kwargs)
    return json.loads(string)


# Uncomment to try it, but comment this code before sub-classing Tk
#root = tk.Tk()
#var1 = JSONVar(root)
#var1.set([1, 2, 3, 4, 5])
#
#var2 = JSONVar(root, value={'a': 10, 'b': 15})
#print("Var1: ", var1.get()[1])
#print("Var2: ", var2.get()['b'])
#root.mainloop()
#exit()

#############################
# Creating compound widgets #
#############################

class LabelInput(tk.Frame):
  """A label and input combined together"""

  def __init__(
    self, parent, label, inp_cls,
    inp_args, *args, **kwargs
   ):
    super().__init__(parent, *args, **kwargs)
    self.label = tk.Label(self, text=label, anchor='w')
    self.input = inp_cls(self, **inp_args)

    # side-by-side layout
    self.columnconfigure(1, weight=1)
    self.label.grid(sticky=tk.E + tk.W)
    self.input.grid(row=0, column=1, sticky=tk.E + tk.W)

    # label-on-top layout
    #self.columnconfigure(0, weight=1)
    #self.label.grid(sticky=tk.E + tk.W)
    #self.input.grid(sticky=tk.E + tk.W)



# Uncomment to try it, but comment this code again before sub-classing tk
#root = tk.Tk()
#li1 = LabelInput(root, 'Name', tk.Entry, {'bg': 'red'})
#li1.grid()
#age_var = tk.IntVar(root, value=21)
#li2 = LabelInput(
#  root,
#  'Age',
#  tk.Spinbox,
#  {'textvariable': age_var, 'from_': 10, 'to': 150}
#)
#li2.grid()
#root.mainloop()
#exit()

##############################
# Building component objects #
##############################

class MyForm(tk.Frame):

  def __init__(self, parent, data_var, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    self.data_var = data_var
    self._vars = {
      'name': tk.StringVar(),
      'age': tk.IntVar(value=2)
    }
    LabelInput(
      self,
      'Name',
      tk.Entry,
      {'textvariable': self._vars['name']}
    ).grid(sticky=tk.E + tk.W)
    LabelInput(
      self,
      'Age',
      tk.Spinbox,
      {'textvariable': self._vars['age'], 'from_': 10, 'to': 150}
    ).grid(sticky=tk.E + tk.W)
    tk.Button(self, text='Submit', command=self._on_submit).grid()

  def _on_submit(self):
    data = { key: var.get() for key, var in self._vars.items() }
    self.data_var.set(data)


# We can even subclass Tk

class Application(tk.Tk):
  """A simple form application"""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.jsonvar = JSONVar()
    self.output_var = tk.StringVar()
    tk.Label(self, text='Please fill the form').grid(sticky='ew')
    MyForm(self, self.jsonvar).grid(sticky='nsew')
    tk.Label(self, textvariable=self.output_var).grid(sticky='ew')
    self.columnconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)

    self.jsonvar.trace_add('write', self._on_data_change)

  def _on_data_change(self, *args, **kwargs):
    data = self.jsonvar.get()
    output = ''.join([
        f'{key} = {value}\n'
        for key, value in data.items()
    ])
    self.output_var.set(output)

#root.mainloop()
if __name__ == '__main__':
  app = Application()
  app.mainloop()
