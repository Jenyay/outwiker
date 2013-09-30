#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.hotkey import HotKey

class HotKeyParser (object):
    """Класс для создания экземпляра класса HotKey из строки и создания строки по HotKey"""
    def __init__(self):
        pass        


    def toString (self, hotkey):
        """
        Создание строки по экземпляру класса HotKey
        """
        ctrlStr = u"Ctrl+" if hotkey.ctrl else u""
        shiftStr = u"Shift+" if hotkey.shift else u""
        altStr = u"Alt+" if hotkey.alt else u""

        return u"{ctrl}{shift}{alt}{key}".format (
                ctrl=ctrlStr,
                shift=shiftStr,
                alt=altStr,
                key=hotkey.key)
