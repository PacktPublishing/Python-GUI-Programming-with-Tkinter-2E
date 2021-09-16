from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
  IMAGE_DIRECTORY = Path(sys.executable).parent / 'images'
else:
  IMAGE_DIRECTORY = Path(__file__).parent

ABQ_LOGO_16 = IMAGE_DIRECTORY / 'abq_logo-16x10.png'
ABQ_LOGO_32 = IMAGE_DIRECTORY / 'abq_logo-32x20.png'
ABQ_LOGO_64 = IMAGE_DIRECTORY / 'abq_logo-64x40.png'

# PNG icons

SAVE_ICON = IMAGE_DIRECTORY / 'file-2x.png'
RESET_ICON = IMAGE_DIRECTORY / 'reload-2x.png'
LIST_ICON = IMAGE_DIRECTORY / 'list-2x.png'
FORM_ICON = IMAGE_DIRECTORY / 'browser-2x.png'


# BMP icons
QUIT_BMP = IMAGE_DIRECTORY / 'x-2x.xbm'
ABOUT_BMP = IMAGE_DIRECTORY / 'question-mark-2x.xbm'
