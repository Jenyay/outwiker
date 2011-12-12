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

includefiles = ['images', 'msvcr90.dll', 'Microsoft.VC90.CRT.manifest', 'locale', 'version.txt', 'tools', 'templates']
includes = []
excludes = []
packages = []


setup(
    name = "tests",
    version = getCurrentVersion(),
    description = "tests",
    options = {'build_exe': {'excludes':excludes, 'packages':packages, 'include_files':includefiles, 'build_exe':'../distrib/tests_win'}},
    executables = [Executable("tests.py", base = 'Console')])

