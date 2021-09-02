import tkinter as tk
from random import randint, choice

# Create root and canvas
root = tk.Tk()

canvas = tk.Canvas(
  root, background='black',
  width=1024, height=768,
)
canvas.grid(row=0, column=0)

# Draw stars
colors = ['#FCC', '#CFC', '#CCF', '#FFC', '#FFF', '#CFF']
for _ in range(1000):
  x = randint(0, 2048)
  y = randint(0, 1536)
  z = randint(1, 10)
  c = choice(colors)
  canvas.create_oval((x - z, y - z), (x + z, y + z), fill=c)

# configure the scroll region
canvas.configure(scrollregion=(0, 0, 2048, 1536))

# create scrollbars and connect to canvas
xscroll = tk.Scrollbar(
  root,
  command=canvas.xview,
  orient=tk.HORIZONTAL
)
xscroll.grid(row=1, column=0, sticky='new')

yscroll = tk.Scrollbar(root, command=canvas.yview)
yscroll.grid(row=0, column=1, sticky='nsw')

canvas.configure(yscrollcommand=yscroll.set)
canvas.configure(xscrollcommand=xscroll.set)


root.mainloop()
