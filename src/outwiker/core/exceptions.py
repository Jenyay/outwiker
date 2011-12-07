#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class OutWikerException (BaseException):
    def __init__ (self):
        BaseException.__init__(self)


class TreeException (OutWikerException):
    def __init__ (self):
        OutWikerException.__init__(self)


class RootFormatError (TreeException):
    """
    Исключение бросается при ошибке чтения файла __page.opt корня вики
    """
    def __init__ (self):
        TreeException.__init__(self)


class ClearConfigError (TreeException):
    """
    Исключение бросается, когда не удается сбросить файл __page.opt
    """
    def __init__ (self):
        TreeException.__init__(self)


class DublicateTitle (TreeException):
    def __init__ (self):
        TreeException.__init__(self)


class ReadonlyException (OutWikerException):
    def __init__ (self):
        OutWikerException.__init__(self)


class PreferencesException (OutWikerException):
    def __init__ (self):
        OutWikerException.__init__(self)
