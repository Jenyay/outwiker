# -*- coding: UTF-8 -*-

import os

from outwiker.core.system import getOS


def getImagesPath():
    return unicode(
        os.path.join(os.path.dirname(__file__), "images"),
        getOS().filesEncoding
    )


def findUniquePath(path, name, extension=u''):
    if not name:
        raise ValueError

    index = 1
    result = os.path.join(path, name)

    while os.path.exists(result):
        suffix = u' ({}){}'.format(index, extension)

        if name.endswith(extension):
            newname = name[:len(name) - len(extension)] + suffix
        else:
            newname = name + suffix

        result = os.path.join(path, newname)
        index += 1

    return result


def createFile(fname):
    with open(fname, 'w'):
        pass
