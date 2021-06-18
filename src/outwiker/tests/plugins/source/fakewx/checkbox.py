# -*- coding: UTF-8 -*-

from .control import Control


class CheckBox (Control):
    def __init__ (self):
        self.Value = False


    def IsChecked (self):
        return self.Value


    def SetValue (self, state):
        self.Value = state


    def GetValue (self):
        return self.Value
