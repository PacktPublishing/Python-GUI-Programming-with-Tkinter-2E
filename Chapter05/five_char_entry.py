"""Five Character Entry Demo"""

import tkinter as tk

root = tk.Tk()

entry3 = tk.Entry(root)
entry3.grid()
entry3_error = tk.Label(root, fg='red')
entry3_error.grid()

def only_five_chars(proposed):
  return len(proposed) < 6

def only_five_chars_error(proposed):
  entry3_error.configure(
    text=f'{proposed} is too long, only 5 chars allowed.'
  )
validate3_ref = root.register(only_five_chars)
invalid3_ref = root.register(only_five_chars_error)

entry3.configure(
  validate='all',
  validatecommand=(validate3_ref, '%P'),
  invalidcommand=(invalid3_ref, '%P')
)

root.mainloop()
