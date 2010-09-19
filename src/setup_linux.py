from cx_Freeze import setup, Executable

includefiles = ['images', 'help', 'readme_rus.txt']
includes = []
excludes = []
packages = []


setup(
	name = "OutWiker",
	version = "1.0 alpha 1",
	description = "Wiki + Outliner",
	options = {'build_exe': {'excludes':excludes, 'packages':packages, 'include_files':includefiles}},
	executables = [Executable("outwiker.py", icon = "images/icon.ico")])

