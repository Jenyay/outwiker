#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""
import os.path

from outwiker.pages.wiki.parser.tokenattach import AttachToken
from outwiker.core.system import getOS


def getFileName (fileParam):
    """
    Получить имя прикрепленного файла по параметру file
    fileParam - значение параметра file
    """
    fname = fileParam.strip()

    if fname.startswith (AttachToken.attachString):
        fname = fname[len (AttachToken.attachString): ]

    return fname


def getImagePath (imageName):
    """
    Получить полный путь до картинки
    """
    imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
    fname = os.path.join (imagedir, imageName)
    return fname
