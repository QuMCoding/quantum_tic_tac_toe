import sys

from cx_Freeze import setup, Executable

build_exe_options = {'icon': 'chkimg.ico', 'include_files': ['chkimg.ico', 'folder.gif'], 'packages':['lxml']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executable = Executable('chkimg.pyw', base=base)

setup(
        name = "chkimg",
        version = "0.2",
        description = "Check Image",
        options = {'build_exe': build_exe_options},
        executables = [executable])
