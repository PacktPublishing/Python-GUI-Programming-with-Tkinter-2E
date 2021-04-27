"""Hello World application for Tkinter"""

# Import all the classes from tkinter
from tkinter import *

# Create a root window
root = Tk()

# Create a widget
label = Label(root, text="Hello World")

# Place the label on the root window
label.pack()

# Run the event loop
root.mainloop()
