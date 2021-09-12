import tkinter as tk
from tkinter.messagebox import showinfo
from threading import Thread
from time import sleep, localtime

class Window(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        tk.Entry(self, textvariable=parent.variable).pack()


class App(tk.Tk):

  def __init__(self, *args, **kwargs):
    super().__init__()
    self.variable = tk.StringVar(value='hello')
    Thread(target=Window, args=(self,)).start()
    Thread(target=Window, args=(self,)).start()
    Thread(target=Window, args=(self,)).start()



if __name__ == '__main__':
  app = App()
  app.mainloop()
