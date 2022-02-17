"""A banana preferences survey written in Python with Tkinter"""

import tkinter as tk

# Create the root window
root = tk.Tk()

# set the title
root.title('Banana interest survey')

# set the root window size
root.geometry('640x480+300+300')
root.resizable(False, False)

###########
# Widgets #
###########

# Use a Label to show the title
# 'font' lets us set a font
title = tk.Label(
  root,
  text='Please take the survey',
  font=('Arial 16 bold'),
  bg='brown',
  fg='#FF0'
)

# Use an Entry to get a string
name_label = tk.Label(root, text='What is your name?')
name_inp = tk.Entry(root)

# Use Checkbutton to get a boolean
eater_inp = tk.Checkbutton(
  root,
  text='Check this box if you eat bananas'
)

# Spinboxes are good for number entry
num_label = tk.Label(
  root,
  text='How many bananas do you eat per day?'
)
num_inp = tk.Spinbox(root, from_=0, to=1000, increment=1)

# Listbox is good for choices

color_label = tk.Label(
  root,
  text='What is the best color for a banana?'
)
color_inp = tk.Listbox(root, height=1)  # Only show selected item
# add choices
color_choices = (
  'Any',
  'Green',
  'Green-Yellow',
  'Yellow',
  'Brown spotted',
  'Black'
)
for choice in color_choices:
  # END is a tkinter constant that means the end of an input
  color_inp.insert(tk.END, choice)


# RadioButtons are good for small choices

plantain_label = tk.Label(root, text='Do you eat plantains?')
# Use a Frame to keep widgets together
plantain_frame = tk.Frame(root)
plantain_yes_inp = tk.Radiobutton(plantain_frame, text='Yes')
plantain_no_inp = tk.Radiobutton(plantain_frame, text='Ewww, no!')

# The Text widget is good for long pieces of text
banana_haiku_label = tk.Label(root, text='Write a haiku about bananas')
banana_haiku_inp = tk.Text(root, height=3)

# Buttons are used to trigger actions

submit_btn = tk.Button(root, text='Submit Survey')

# Use a label to display a line of output
# 'anchor' sets where the text is stuck if the label is wider than needed.
# 'justify' determines how multiple lines of text are aligned
output_line = tk.Label(root, text='', anchor='w', justify='left')


#######################
# Geometry Management #
#######################
# Using Grid instead of pack
# Put our widgets on the root window
#title.grid()
# columnspan allows the widget to span multiple columns
title.grid(columnspan=2)

# add name label and input
# Column defaults to 0
name_label.grid(row=1, column=0)

# The grid automatically expands
# when we add a widget to the next row or column
name_inp.grid(row=1, column=1)

# 'sticky' attaches the widget to the named sides,
# so it will expand with the grid
eater_inp.grid(row=2, columnspan=2, sticky='we')
# tk constants can be used instead of strings
num_label.grid(row=3, sticky=tk.W)
num_inp.grid(row=3, column=1, sticky=(tk.W + tk.E))

#padx and pady can still be used to add horizontal or vertical padding
color_label.grid(row=4, columnspan=2, sticky=tk.W, pady=10)
color_inp.grid(row=5, columnspan=2, sticky=tk.W + tk.E, padx=25)

# We can still use pack on the plantain frame.
# pack and grid can be mixed in a layout as long as we don't
# use them in the same frame
plantain_yes_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_no_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_label.grid(row=6, columnspan=2, sticky=tk.W)
plantain_frame.grid(row=7, columnspan=2, sticky=tk.W)

# Sticky on all sides will allow the widget to fill vertical and horizontal
banana_haiku_label.grid(row=8, sticky=tk.W)
banana_haiku_inp.grid(row=9, columnspan=2, sticky='NSEW')

# Add the button and output
submit_btn.grid(row=99)
output_line.grid(row=100, columnspan=2, sticky='NSEW')

# columnconfigure can be used to set options on the columns of the grid
# 'weight' means that column will be preferred for expansion
root.columnconfigure(1, weight=1)

# rowconfigure works for rows
root.rowconfigure(99, weight=2)
root.rowconfigure(100, weight=1)

#####################
# Add some behavior #
#####################

def on_submit():
  """To be run when the user submits the form"""

  # Many widgets use "get" to retrieve contents
  name = name_inp.get()
  # spinboxes return a str, not a float or int!
  number = num_inp.get()
  # Listboxes are more involved
  selected_idx = color_inp.curselection()
  if selected_idx:
    color = color_inp.get(selected_idx)
  else:
    color = ''
  # We're going to need some way to get our button values!
  # banana_eater = ????

  # Text widgets require a range
  haiku = banana_haiku_inp.get('1.0', tk.END)

  # Update the text in our output
  message = (
    f'Thanks for taking the survey, {name}.\n'
    f'Enjoy your {number} {color} bananas!'
    )
  output_line.configure(text=message)
  print(haiku)


# configure the button to trigger submission
submit_btn.configure(command=on_submit)

###############
# Execute App #
###############

root.mainloop()
