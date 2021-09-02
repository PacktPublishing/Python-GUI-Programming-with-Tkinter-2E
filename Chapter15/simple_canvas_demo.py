import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(
  root, background='black',
  width=1024, height=768
)
canvas.pack()

# draw a square
canvas.create_rectangle(240, 240, 260, 260, fill='orange')
canvas.create_rectangle(
  (300, 240), (320, 260),
  fill='#FF8800'
)

# draw an oval
canvas.create_oval(
  (350, 200), (450, 250), fill='blue'
)

# draw an arc
canvas.create_arc(
  (100, 200), (200, 300),
  fill='yellow', extent=315, start=25
)

# draw a line
canvas.create_line(
  (0, 180), (1024, 180),
  width=5, fill='cyan'
)

canvas.create_line(
  (0, 320), (500, 320), (500, 768), (640, 768),
  (640, 320), (1024, 320),
  width=5, fill='cyan'
)

# draw a polygon
canvas.create_polygon(
  (350, 225), (350,  300), (375, 275), (400, 300),
  (425, 275), (450, 300), (450, 225),
  fill='blue'
)

# draw text
canvas.create_text(
  (500, 100), text='Insert a Quarter',
  fill='yellow', font='TkDefaultFont 64'
)

# draw an image
smiley = tk.PhotoImage(file='smile.gif')
image_item = canvas.create_image((570, 250), image=smiley)
canvas.tag_bind(image_item, '<Button-1>', lambda e: canvas.delete(image_item))

# add a widget

quit = tk.Button(
  root, text='Quit', bg='black', fg='cyan', font='TkFixedFont 24',
  activeforeground='black', activebackground='cyan', command=root.quit
)
canvas.create_window((100, 700), height=100, width=100, window=quit)

root.mainloop()
