import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\my\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\my\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'

setup(
    name = "filmow_to_letterboxd",
    version = "2.0.0",
    options = {"build_exe": {
        'packages': ["os","sys","ctypes","wx", "wx.lib.scrolledpanel", "wx.richtext", "wx.lib.agw.hyperlink", "requests", "bs4", "idna.idnadata"],
        'include_files': ['filmow_to_letterboxd.py', 'utils.py'],
        'include_msvcr': True,
    }},
    executables = [Executable("app.py",base="Win32GUI")]
    )