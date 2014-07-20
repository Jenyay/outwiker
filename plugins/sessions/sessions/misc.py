# -*- coding: UTF-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""
import os.path

from outwiker.core.system import getOS


def getImagePath (imageName):
    """
    Получить полный путь до картинки
    """
    imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
    fname = os.path.join (imagedir, imageName)
    return fname
