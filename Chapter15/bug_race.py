"""Bug Race

A demo for the Tkinter Canvas
"""

import tkinter as tk
from queue import Queue
from random import randint

class App(tk.Tk):
  """Main application class"""

  def __init__(self):
    super().__init__()
    self.canvas = tk.Canvas(self, background='black')
    self.canvas.pack(fill='both', expand=1)
    self.geometry('800x600')
    self.canvas.wait_visibility()
    self.setup()

  def setup(self):
    self.canvas.left = 0
    self.canvas.top = 0
    self.canvas.right = self.canvas.winfo_width()
    self.canvas.bottom = self.canvas.winfo_height()
    self.canvas.center_x = self.canvas.right // 2
    self.canvas.center_y = self.canvas.bottom // 2
    self.finish_line = self.canvas.create_rectangle(
      (self.canvas.right - 50, 0),
      (self.canvas.right, self.canvas.bottom),
      fill='yellow',
      stipple='gray50'
    )
    self.racers = [
      Racer(self.canvas, 'red'),
      Racer(self.canvas, 'green')
    ]
    self.execute_frame()

  def execute_frame(self):
    for racer in self.racers:
      racer.next_move()
      if self.finish_line in racer.overlapping:
        self.declare_winner(racer)
        return
    self.after(Racer.FRAME_RES, self.execute_frame)

  def declare_winner(self, racer):

    wintext = self.canvas.create_text(
      (self.canvas.center_x, self.canvas.center_y),
      text=f'{racer.name} wins!\nClick to play again.',
      fill='white',
      font='TkDefaultFont 32',
      activefill='violet'
    )
    self.canvas.tag_bind(wintext, '<Button-1>', self.reset)

  def reset(self, *args):
    self.canvas.delete('all')
    self.setup()


class Racer:

  FRAME_RES = 50

  @staticmethod
  def partition(n, k):
    """Return a list of k integers that sum to n"""
    if n == 0:
      return [0] * k
    base_step = int(n // k)
    parts = [base_step] * k
    for i in range(n % k):
        parts[i] += 1
    return parts

  def __init__(self, canvas, color):
    self.canvas = canvas
    self.name = f"{color.title()} player"
    size = 50
    # draw & save id
    self.id = canvas.create_oval(
      (canvas.left, canvas.center_y),
      (canvas.left + size, canvas.center_y + size),
      fill=color
    )
    self.movement_queue = Queue()
    self.plot_course()

  def plot_course(self):
    start_x = self.canvas.left
    start_y = self.canvas.center_y
    total_dx, total_dy = (0, 0)

    while start_x + total_dx < self.canvas.right:
      dx = randint(0, 100)
      dy = randint(-50, 50)
      # bounch from top & bottom
      target_y = start_y + total_dy + dy
      if not (self.canvas.top < target_y < self.canvas.bottom):
        dy = -dy
      time = randint(500, 2000)
      self.queue_move(dx, dy, time)
      total_dx += dx
      total_dy += dy

  def next_move(self):
    if not self.movement_queue.empty():
      nextmove = self.movement_queue.get()
      self.canvas.move(self.id, *nextmove)

  def queue_move(self, dx, dy, time):
    num_steps = time // self.FRAME_RES
    steps = zip(
      self.partition(dx, num_steps),
      self.partition(dy, num_steps))

    for step in steps:
      self.movement_queue.put(step)

  @property
  def overlapping(self):
    bbox = self.canvas.bbox(self.id)
    overlappers = self.canvas.find_overlapping(*bbox)
    return [x for x in overlappers if x!=self.id]

App().mainloop()
