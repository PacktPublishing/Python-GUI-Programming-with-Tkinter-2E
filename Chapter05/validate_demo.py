import tkinter as tk

root = tk.Tk()
entry = tk.Entry(root)
entry.grid()

# create a pointless validation command
def always_good():
  return True

validate_ref = root.register(always_good)

entry.configure(
  validate='all',
  validatecommand=(validate_ref,)
)

# a more useful validation command


entry2 = tk.Entry(root)
entry2.grid(pady=10)

def no_t_for_me(proposed):
  return 't' not in proposed

validate2_ref = root.register(no_t_for_me)
entry2.configure(
  validate='all',
  validatecommand=(validate2_ref, '%P')
)

# An Entry that displays an error

entry3 = tk.Entry(root)
entry3.grid()
entry3_error = tk.Label(root, fg='red')
entry3_error.grid(pady=10)

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
