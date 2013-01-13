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

        if self.Selection == None:
            self.Selection = 0


    def GetItems (self):
        return self._items


    def GetCount (self):
        return len (self._items)


    def SetSelection(self, n):
        assert n < len (self._items)
        self.Selection = n


    def GetSelection(self):
        return self.Selection


    def GetValue (self):
        if self.Selection != None:
            return self._items[self.Selection]
