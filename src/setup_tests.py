#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

from cx_Freeze import setup, Executable

from outwiker.core.system import getCurrentDir


def getCurrentVersion ():
    """
    Получить текущую версию для файла
    """
    fname = "version.txt"
    path = os.path.join (getCurrentDir(), fname)

    with open (path) as fp:
        lines = fp.readlines()

    version_str = "%s.%s" % (lines[0].strip(), lines[1].strip())

    return version_str

includefiles = ['images', 'locale', 'version.txt', 'tools', 'styles']
includes = []
excludes = []

# Добавляем 'outwiker.pages.wiki.wikipanel',
# т.к. этот модуль используется только в старых версиях плагинов
packages = ['urllib', 'urllib2', 'outwiker.pages.wiki.wikipanel']


setup(
    name = "tests",
    version = getCurrentVersion(),
    description = "tests",
    options = {
        'build_exe': {
            'excludes': excludes,
            'packages': packages,
            'include_files': includefiles,
            'build_exe': '../tests_win',
            'include_msvcr': True,
        }},
    executables = [Executable("tests.py", base = 'Console')])
