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
eater_inp = tk.Checkbutton(root, text='Check this box if you eat bananas')

# Spinboxes are good for number entry
num_label = tk.Label(root, text='How many bananas do you eat per day?')
num_inp = tk.Spinbox(root, from_=0, to=1000, increment=1, value=3)

# Listbox is good for choices

color_label = tk.Label(root, text='What is the best color for a banana?')
color_inp = tk.Listbox(root, height=1)  # Only show selected item
# add choices
color_choices = (
  'Any',
  'Green',
  'Green-Yellow',
  'Yellow',
  'Brown Spotted',
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

# Put our widgets on the root window
title.pack()


# add name label.  It shows up underneath
# 'anchor' specifies which side our widget sticks to
# 'fill' allows our widget to expand into extra space in x, y, or both axes
name_label.pack(anchor='w')
name_inp.pack(fill='x')

# tk constants can be used instead of strings
eater_inp.pack(anchor=tk.W)
num_label.pack(anchor=tk.W)
num_inp.pack(fill=tk.X)

#padx and pady can be used to add horizontal or vertical padding
color_label.pack(anchor=tk.W, pady=10)
color_inp.pack(fill=tk.X, padx=25)

# Use side to change the orientation of packing
# Note that we're packing into the plantain frame, not root!
# This keeps our radio buttons side-by-side
# ipad is "internal padding".
# Using this over regular padding not only separates the buttons,
# it increases the space we can click on to select a button
plantain_yes_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_no_inp.pack(side='left', fill='x', ipadx=10, ipady=5)
plantain_label.pack(fill='x', padx=10, pady=5)
plantain_frame.pack(fill='x')

# fill both ways
# 'expand' means this widget will get any extra space left in the parent
banana_haiku_label.pack(anchor='w')
banana_haiku_inp.pack(fill='both', expand=True)

# Add the button and output
# Specifying side='bottom' means the widgets will be packed
# from the bottom up, so specify the last widget first
# Specifying 'expand' on another widget means extra space
# will be divided amongst the expandable widgets
output_line.pack(side='bottom', fill='x', expand=True)
submit_btn.pack(side='bottom')


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
    color = color_inp.get(selected_idx)

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

# an alternate approach
# note that this sends an event object to the functions
#submit_btn.bind('<Button-1>', on_submit)

###############
# Execute App #
###############

root.mainloop()
