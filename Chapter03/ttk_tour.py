"""A tour of ttk widgets we can use in our application"""

import tkinter as tk
from tkinter import ttk


root = tk.Tk()

my_string_var = tk.StringVar(value='Test')
my_int_var = tk.IntVar()
my_dbl_var = tk.DoubleVar()
my_bool_var = tk.BooleanVar()
pack_args = {"padx": 20, "pady": 20}

def my_callback(*_):
  print("Callback called!")

# Entry

myentry = ttk.Entry(root, textvariable=my_string_var, width=20)
myentry.pack(**pack_args)

# Spinbox

myspinbox = ttk.Spinbox(
  root,
  from_=0, to=100, increment=.01,
  textvariable=my_int_var,
  command=my_callback
)
myspinbox.pack(**pack_args)

# Checkbutton

mycheckbutton = ttk.Checkbutton(
  root,
  variable=my_bool_var,
  textvariable=my_string_var,
  command=my_callback
)
mycheckbutton.pack(**pack_args)

mycheckbutton2 = ttk.Checkbutton(
  root,
  variable=my_dbl_var,
  text='Would you like Pi?',
  onvalue=3.14159,
  offvalue=0,
  underline=15
)
mycheckbutton2.pack(**pack_args)

# Radiobutton
buttons = tk.Frame(root)
buttons.pack()

r1 = ttk.Radiobutton(
  buttons,
  variable=my_int_var,
  value=1,
  text='One'
)
r2 = ttk.Radiobutton(
  buttons,
  variable=my_int_var,
  value=2,
  text='Two'
)
r1.pack(side='left')
r2.pack(side='left')

# Combobox Widget

mycombo = ttk.Combobox(
  root, textvariable=my_string_var,
  values=['This option', 'That option', 'Another option']
)
mycombo.pack(**pack_args)

# Text widget

mytext = tk.Text(
  root,
  undo=True, maxundo=100,
  spacing1=10, spacing2=2, spacing3=5,
  height=5, wrap='char'
)
mytext.pack(**pack_args)

# insert a string at the beginning
mytext.insert('1.0', "I love my text widget!")
# insert a string into the current text
mytext.insert('1.2', 'REALLY ')
# get the whole string
mytext.get('1.0', tk.END)
# delete the last character.
# Note that there is always a newline character inserted automatically
# at the end of the input, so we backup 2 chars instead of 1.
mytext.delete('end - 2 chars')


# Button widget

mybutton = ttk.Button(
  root,
  command=my_callback,
  text='Click Me!',
  default='active'
)
mybutton.pack(**pack_args)

# LabelFrame Widget
mylabelframe = ttk.LabelFrame(
  root,
  text='Button frame'
)

b1 = ttk.Button(
  mylabelframe,
  text='Button 1'
)
b2 = ttk.Button(
  mylabelframe,
  text='Button 2'
)
b1.pack()
b2.pack()
mylabelframe.pack(**pack_args)

# Label Widget

mylabel = ttk.Label(root, text='This is a label')
mylabel.pack(**pack_args)

root.mainloop()
