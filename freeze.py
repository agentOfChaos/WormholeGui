#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit,cffi',
        'namespace_packages': 'zope',
        'include_files': [("mainwindow.ui", "mainwindow.ui")],
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(name='Wormhole GUI',
      version='0.1',
      description='Graphical interface for magic-wormhole',
      options=options,
      executables=executables
)
