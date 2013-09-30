#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

from outwiker.gui.hotkey import HotKey


class HotKeyParser (object):
    """Класс для создания экземпляра класса HotKey из строки и создания строки по HotKey"""
    def __init__(self):
        self._regex = re.compile ("((?P<ctrl>\s*ctrl\s*\+)|(?P<shift>\s*shift\s*\+)|(?P<alt>\s*alt\s*\+))*(?P<key>.*)",
                re.I | re.U)


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


    def fromString (self, hotkeyStr):
        """
        Создание экземпляра класса HotKey по строке
        """
        match = self._regex.match (hotkeyStr)
        if match == None:
            raise ValueError ("Invalid hot key string")

        elements = match.groupdict()
        key = elements["key"].strip()

        ctrl = elements["ctrl"] != None
        shift = elements["shift"] != None
        alt = elements["alt"] != None

        if (len (key) == 0 and
                (ctrl or shift or alt) ):
            raise ValueError ("Invalid hot key string")

        return HotKey (key, ctrl=ctrl, shift=shift, alt=alt)
