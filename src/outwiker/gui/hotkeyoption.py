# -*- coding: utf-8 -*-

from outwiker.core.config import BaseOption
from outwiker.gui.hotkeyparser import HotKeyParser


class HotKeyOption (BaseOption):
    def _loadValue(self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        if self.config.has_option(self.section, self.param):
            return HotKeyParser.fromString(self.config.get(self.section,
                                                           self.param))
        else:
            raise ValueError('Use default hotkey')

    def _prepareToWrite(self, val) -> str:
        return '' if val is None else HotKeyParser.toString(val)
