# -*- coding: utf-8 -*-

from outwiker.core.config import BaseOption
from outwiker.gui.hotkeyparser import HotKeyParser


class HotKeyOption (BaseOption):
    def _loadValue(self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return HotKeyParser.fromString(self.config.get(self.section,
                                                       self.param))

    def _prepareToWrite(self, val) -> str:
        return u"" if val is None else HotKeyParser.toString(val)
