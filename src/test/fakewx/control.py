# -*- coding: UTF-8 -*-

from .window import Window


class Control (Window):
    def __init__ (self):
        super (Control, self).__init__ ()
        self.LabelText = u""


    def GetLabelText (self):
        return self.LabelText
