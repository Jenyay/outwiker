#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .control import Control


class SpinCtrl (Control):
    """
    Заглушка вместо wx.SpinCtrl
    """
    def __init__ (self, value=0):
        self.Value = value


    def GetValue (self):
        return self.Value


    def SetValue (self, value):
        self.Value = value


    def SetRange(self, minVal, maxVal):
        pass
