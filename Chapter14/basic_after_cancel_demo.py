import tkinter as tk

root = tk.Tk()
task_id = root.after(3000, root.quit)
tk.Button(
  root,
  text='Do not quit!', command=lambda: root.after_cancel(task_id)
).pack()
root.mainloop()
