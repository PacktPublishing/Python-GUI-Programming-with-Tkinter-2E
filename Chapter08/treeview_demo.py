import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Set up root window
root = tk.Tk()

# Create list of paths
paths = Path('.').glob('**/*')


# Create and configure treeview
tv = ttk.Treeview(
  root, columns=['size', 'modified'], selectmode='none'
)
tv.heading('#0', text='Name')
tv.heading('size', text='Size', anchor='center')
tv.heading('modified', text='Modified', anchor='e')
tv.column('#0', stretch=True)
tv.column('size', width=200)

tv.pack(expand=True, fill='both')

# Populate Treeview
for path in paths:
  meta = path.stat()
  parent = str(path.parent)
  if parent == '.':
    parent = ''
  tv.insert(
    parent,
    'end',
    iid=str(path),
    text=str(path.name),
    values=[meta.st_size, meta.st_mtime]
  )

def sort(tv, col, parent='', reverse=False):
  """Sort the given column of the treeview"""

  # build a sorting list
  sort_index = list()
  for iid in tv.get_children(parent):
    sort_value = tv.set(iid, col) if col != '#0' else iid
    sort_index.append((sort_value, iid))

  # sort the list
  sort_index.sort(reverse=reverse)

  # move each node according to its index in the sort list
  for index, (_, iid) in enumerate(sort_index):
    tv.move(iid, parent, index)

    # sort each child node
    sort(tv, col, parent=iid, reverse=reverse)

  # If this is the top level, reset the headings for reverse sort
  if parent == '':
    tv.heading(
      col,
      command=lambda col=col: sort(tv, col, reverse=not reverse)
    )

for cid in ['#0', 'size', 'modified']:
  tv.heading(cid, command=lambda col=cid: sort(tv, col))


status = tk.StringVar()
tk.Label(root, textvariable=status).pack(side=tk.BOTTOM)

def show_directory_stats(*_):
  clicked_path = Path(tv.focus())
  num_children = len(list(clicked_path.iterdir()))
  status.set(
    f'Directory: {clicked_path.name}, {num_children} children'
  )


tv.bind('<<TreeviewOpen>>', show_directory_stats)
tv.bind('<<TreeviewClose>>', lambda _: status.set(''))

root.mainloop()
