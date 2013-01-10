#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""

from outwiker.pages.wiki.parser.tokenattach import AttachToken

def getFileName (fileParam):
    """
    Получить имя прикрепленного файла по параметру file
    fileParam - значение параметра file
    """
    fname = fileParam.strip()

    if fname.startswith (AttachToken.attachString):
        fname = fname[len (AttachToken.attachString): ]

    return fname
