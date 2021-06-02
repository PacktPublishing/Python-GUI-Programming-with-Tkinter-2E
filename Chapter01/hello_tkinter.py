"""Hello World application for Tkinter"""

# Import tkinter
import tkinter as tk

# Create a root window
root = tk.Tk()

# Create a widget
label = tk.Label(root, text="Hello World")

# Place the label on the root window
label.pack()

# Run the event loop
root.mainloop()
