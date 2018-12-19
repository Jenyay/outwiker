# -*- coding: utf-8 -*-

from outwiker.core.config import BaseOption
from outwiker.gui.hotkeyparser import HotKeyParser


class HotKeyOption (BaseOption):
    def __init__(self, config, section, param, defaultValue):
        super(HotKeyOption, self).__init__(
            config, section, param, defaultValue)

    def _loadValue(self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return HotKeyParser.fromString(self.config.get(self.section, self.param))

    def _prepareToWrite(self, value):
        return u"" if value is None else HotKeyParser.toString(value)
