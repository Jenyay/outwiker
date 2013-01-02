#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Набор небольших функций, которые могут использоваться в разных классах
"""

import os.path
from outwiker.core.system import getOS

def getLangList ():
    """
    Прочитать список поддерживаемых языков
    """
    fname = u"languages.txt"
    cmd_folder = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding )
    fullpath = os.path.join (cmd_folder, fname)

    try:
        with open (fullpath) as fp:
            return [item.strip() for item in fp.readlines()]
    except IOError:
        return [u"text"]
