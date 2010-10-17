from cx_Freeze import setup, Executable

includefiles = ['images', 'msvcr90.dll', 'Microsoft.VC90.CRT.manifest', 'help']
includes = []
excludes = []
packages = []


setup(
	name = "OutWiker",
	version = "1.0 alpha 1",
	description = "Wiki + Outliner",
	options = {'build_exe': {'excludes':excludes, 'packages':packages, 'include_files':includefiles}},
	executables = [Executable("outwiker.py", base = 'Win32GUI', icon = "images/icon.ico")])

