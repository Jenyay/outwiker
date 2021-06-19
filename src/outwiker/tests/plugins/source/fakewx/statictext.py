# -*- coding: utf-8 -*-

from .control import Control


class StaticText (Control):
    """
    Заглушка вместо wx.StaticText
    """

    def __init__(self, label=''):
        super().__init__()
        self.LabelText = label
