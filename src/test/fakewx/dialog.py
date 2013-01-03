#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .window import Window


class Dialog (Window):
    def __init__ (self):
        self.ReturnCode = -1


    def SetReturnCode (self, code):
        self.ReturnCode = code


    def GetReturnCode (self, code):
        return self.ReturnCode


    def ShowModal (self):
        return self.ReturnCode

