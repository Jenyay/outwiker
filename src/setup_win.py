#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cx_Freeze import setup, Executable
import os

import outwiker.core.system

def getCurrentVersion ():
    """
    Получить текущую версию для файла
    """
    fname = "version.txt"
    path = os.path.join (outwiker.core.system.getCurrentDir(), fname)

    with open (path) as fp:
        lines = fp.readlines()

    version_str = "%s.%s" % (lines[0].strip(), lines[1].strip())

    return version_str

includefiles = ['images', 
    'help', 
    'locale', 
    'version.txt', 
    'tools', 
    'styles', 
    'plugins']

includes = []
excludes = []
# Добавляем 'outwiker.pages.wiki.wikipanel', 
# т.к. этот модуль используется только в старых версиях плагинов
packages = ['urllib',
            'urllib2',
            'outwiker.pages.wiki.wikipanel',
            'PIL.Image',
            'PIL.ImageDraw',
            'PIL.ImageFont',
            'PIL.ImageFilter',
            ]


setup(
    name = "OutWiker",
    version = getCurrentVersion(),
    description = "Wiki + Outliner",
    options = {'build_exe': {
        'excludes':excludes, 
        'packages':packages, 
        'include_files':includefiles, 
        'build_exe':'../build/outwiker_win',
        'include_msvcr': True,
        }},
    executables = [Executable("runoutwiker.py", base = 'Win32GUI', icon = "images/outwiker.ico", targetName="outwiker.exe")])

