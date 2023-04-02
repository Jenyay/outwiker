# -*- coding: utf-8 -*-

import os
import shutil

from outwiker.api.services.application import getSpecialDirList, startFile

from snippets.defines import SNIPPETS_DIR
from snippets.i18n import get_


def getImagesPath():
    return os.path.join(getPluginPath(), "images")


def getPluginPath():
    return os.path.dirname(__file__)


def openHelp():
    global _
    _ = get_()

    help_dir = _("help/en")
    help_path = os.path.join(getPluginPath(), help_dir, "__content.html")
    startFile(help_path)


def findUniquePath(path, name, extension=""):
    if not name:
        raise ValueError

    index = 1
    result = os.path.join(path, name)

    while os.path.exists(result):
        suffix = " ({}){}".format(index, extension)

        if name.endswith(extension):
            newname = name[: len(name) - len(extension)] + suffix
        else:
            newname = name + suffix

        result = os.path.join(path, newname)
        index += 1

    return result


def createFile(fname):
    with open(fname, "w"):
        pass


def moveSnippetsTo(src, dest):
    """
    src - source file or directory name,
    dest - directory to moving.
    """
    dirname = os.path.dirname(src)
    if dirname == dest:
        return src

    if os.path.isdir(src):
        return _moveSnippetsDirTo(src, dest)
    else:
        return _moveSnippetFileTo(src, dest)


def _moveSnippetFileTo(src, dest):
    basename = os.path.basename(src)
    newname = findUniquePath(dest, basename, "")
    os.rename(src, newname)
    return newname


def _moveSnippetsDirTo(src, dest):
    basename = os.path.basename(src)
    newname = findUniquePath(dest, basename)
    shutil.move(src, newname)
    return newname


def getSnippetsDir():
    return getSpecialDirList(SNIPPETS_DIR)[-1]
