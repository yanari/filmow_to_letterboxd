# import os
from cx_Freeze import setup, Executable

# os.environ['TCL_LIBRARY'] = r'C:\Users\my\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\Users\my\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'

setup(
    name = "filmow_to_letterboxd",
    version = "2.0.0",
    options = {"build_exe": {
        'packages': ["os","wx", "wx.lib.scrolledpanel", "wx.richtext", "wx.lib.agw.hyperlink", "requests", "bs4", "queue", "idna.idnadata"],
        'include_files': ['icon.png'],
        'include_msvcr': True,
    }},
    executables = [Executable("app.py",base="Win32GUI")]
    )