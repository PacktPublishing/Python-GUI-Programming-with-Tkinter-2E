import tkinter as tk
from tkinter import font
root = tk.Tk()

for name in font.names():
  font_obj = font.nametofont(name)
  tk.Label(root, text=name, font=font_obj).pack()

namedfont = tk.StringVar()
family = tk.StringVar()
size = tk.IntVar()

tk.OptionMenu(root, namedfont, *font.names()).pack()
tk.OptionMenu(root, family, *font.families()).pack()
tk.Spinbox(root, textvariable=size, from_=6, to=128).pack()

def setFont():
  font_obj = font.nametofont(namedfont.get())
  font_obj.configure(family=family.get(), size=size.get())

tk.Button(root, text='Change', command=setFont).pack()

root.mainloop()
