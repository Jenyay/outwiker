# -*- coding: UTF-8 -*-

import sys
import os


def addToSysPath(path):
    """
    Add path to sys.path to use outwiker modules
    """
    encoding = sys.getfilesystemencoding()
    cmd_folder = os.path.abspath(path)

    syspath = [unicode(item, encoding)
               if not isinstance(item, unicode)
               else item for item in sys.path]

    if cmd_folder not in syspath:
        sys.path.insert(0, cmd_folder)
