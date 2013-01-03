#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .control import Control


class ComboBox (Control):
    """
    Заглушка вместо ComboBox
    """
    def __init__ (self):
        self.Clear()


    def Clear (self):
        self._items = []
        self.Selection = None


    def AppendItems(self, strings):
        self._items += strings


    def SetSelection(self, n):
        self.Selection = n


    def GetSelection(self):
        return self.Selection


    def GetValue (self):
        if self.Selection != None:
            return self._items[self.Selection]
