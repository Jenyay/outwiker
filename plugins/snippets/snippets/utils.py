# -*- coding: UTF-8 -*-

import os

from outwiker.core.system import getOS


def getImagesPath():
    return unicode(
        os.path.join(os.path.dirname(__file__), "images"),
        getOS().filesEncoding
    )
