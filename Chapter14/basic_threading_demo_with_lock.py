import tkinter as tk
from threading import Thread, Lock
from time import sleep

print_lock = Lock()

def print_slowly(string):
  #print_lock.acquire()
  with print_lock:
    words = string.split()
    for word in words:
      sleep(1)
      print(word)
  #print_lock.release()

class App(tk.Tk):

  def __init__(self):
    super().__init__()
    self.text = tk.StringVar()
    tk.Entry(self, textvariable=self.text).pack()
    tk.Button(self, text="Run unthreaded",
          command=self.print_unthreaded).pack()
    tk.Button(self, text="Run threaded",
          command=self.print_threaded).pack()

  def print_unthreaded(self):
    print_slowly(self.text.get())

  def print_threaded(self):
    thread = Thread(target=print_slowly, args=(self.text.get(),))
    thread.start()

App().mainloop()
