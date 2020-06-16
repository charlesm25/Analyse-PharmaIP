import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('BouclePrincipal.py', base="Win32GUI")
]

setup(name='simple_Tkinter',
      version='0.1',
      description='Sample cx_Freeze Tkinter script',
      executables=executables
      )