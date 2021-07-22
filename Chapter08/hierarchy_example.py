import tkinter as tk
from tkinter import ttk

berries = [
    {'number': '1', 'parent': '',  'value': 'Raspberry'},
    {'number': '4', 'parent': '1', 'value': 'Red Raspberry'},
    {'number': '5', 'parent': '1', 'value': 'Blackberry'},
    {'number': '2', 'parent': '', 'value': 'Banana'},
    {'number': '3', 'parent': '', 'value': 'Strawberry'}
]

root = tk.Tk()

tv = ttk.Treeview(root, columns=['value'])
tv.heading('#0', text='Node')
tv.heading('value', text='Value')
tv.grid(sticky='news')

for berry in berries:
    tv.insert(
        berry['parent'],
        'end',
        iid=berry['number'],
        text=berry['number'],
        values=[berry['value']]
    )





root.mainloop()
