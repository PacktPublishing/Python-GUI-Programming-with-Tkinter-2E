import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter  # this is pillow

class PictureViewer(tk.Tk):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title('My Image Viewer')
    self.geometry('800x600')
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    # create the GUI
    self.image_display = ttk.Label(self)
    self.image_display.grid(columnspan=3)

    ttk.Button(
        self, text='Select image', command=self._choose_file
    ).grid(row=1, column=0, sticky='w')

    # Image filtering
    self.filtervar = tk.StringVar()
    filters =[
      'None', 'BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE',
      'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES',
      'SHARPEN', 'SMOOTH', 'SMOOTH_MORE'
    ]
    ttk.Label(self, text='Filter: ').grid(row=1, column=1, sticky='e')
    ttk.OptionMenu(
      self, self.filtervar, 'None', *filters
    ).grid(row=1, column=2)
    self.filtervar.trace_add('write', self._apply_filter)

  def _choose_file(self):
    filename = filedialog.askopenfilename(
      filetypes=(
        ('JPEG files', '*.jpg *.jpeg *.JPG *.JPEG'),
        ('PNG files', '*.png *.PNG'),
        ('All files', '*.*')
      ))
    if filename:
      self.image = Image.open(filename)
      self.photoimage = ImageTk.PhotoImage(self.image)
      self.image_display.config(image=self.photoimage)

  def _apply_filter(self, *_):
    filter_name = self.filtervar.get()
    if filter_name == 'None':
      self.filtered_image = self.image
    else:
      filter_object = getattr(ImageFilter, filter_name)
      self.filtered_image = self.image.filter(filter_object)
    self.photoimage = ImageTk.PhotoImage(self.filtered_image)
    self.image_display.config(image=self.photoimage)


app = PictureViewer()
app.mainloop()
