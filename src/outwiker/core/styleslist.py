#!/usr/bin/python
# -*- coding: UTF-8 -*-

class StylesList (object):
    """
    Класс для хранения списка существующих стилей страниц
    """
    def __init__ (self, dirlist):
        """
        dirlist - список директорий, где ищутся стили
        """
        self.__dirlist = dirlist[:]
