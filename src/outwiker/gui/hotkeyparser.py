# -*- coding: utf-8 -*-

import re

from outwiker.gui.hotkey import HotKey


class HotKeyParser:
    """
    Класс для создания экземпляра класса HotKey из строки
    и создания строки по HotKey
    """
    # Регулярное выражение для получения горячей клавиши по строке
    _regex = re.compile(r"((?P<ctrl>\s*ctrl\s*\+)|(?P<shift>\s*shift\s*\+)|(?P<alt>\s*alt\s*\+))*(?P<key>.*)",
                        re.I | re.U)

    @staticmethod
    def toString(hotkey):
        """
        Создание строки по экземпляру класса HotKey
        """
        ctrlStr = u"Ctrl+" if hotkey.ctrl else u""
        shiftStr = u"Shift+" if hotkey.shift else u""
        altStr = u"Alt+" if hotkey.alt else u""

        return u"{ctrl}{shift}{alt}{key}".format(
            ctrl=ctrlStr,
            shift=shiftStr,
            alt=altStr,
            key=hotkey.key)

    @staticmethod
    def fromString(hotkeyStr):
        """
        Создание экземпляра класса HotKey по строке
        """
        match = HotKeyParser._regex.match(hotkeyStr)

        # match всегда находится из-за выражения (?P<key>.*) в конце _regex
        assert match is not None

        elements = match.groupdict()
        key = elements["key"].strip()

        ctrl = elements["ctrl"] is not None
        shift = elements["shift"] is not None
        alt = elements["alt"] is not None

        if len(key) == 0:
            return None

        if (u" " in key or
                u"\t" in key):
            return None

        return HotKey(key, ctrl=ctrl, shift=shift, alt=alt)
