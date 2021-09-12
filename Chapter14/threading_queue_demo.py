from time import sleep
from threading import Thread
import tkinter as tk
from queue import Queue


class Backend(Thread):

  def __init__(self, queue, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.queue = queue

  def run(self):
    self.queue.put('ready')
    for n in range(1, 5):
      self.queue.put(f'stage {n}')
      print(f'stage {n}')
      sleep(2)
    self.queue.put('done')


class App(tk.Tk):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.status = tk.StringVar(self, value='ready')
    tk.Label(self, textvariable=self.status).pack()

    tk.Button(self, text="Run process", command=self.go).pack()
    self.queue = Queue()

  def go(self):
    p = Backend(self.queue)
    p.start()
    self.check_queue()

  def check_queue(self):
    msg = ''
    while not self.queue.empty():
      msg = self.queue.get()
      self.status.set(msg)
    if msg != 'done':
      self.after(100, self.check_queue)

App().mainloop()
