# -*- coding: utf-8 -*-

import wx

from .htmlrender import HtmlRenderBase


class HtmlRenderFake(HtmlRenderBase):
    def __init__(self, parent):
        super().__init__(parent)

    def _createRender(self):
        return wx.Panel(self)

    @property
    def page(self):
        return None

    @page.setter
    def page(self, value):
        pass

    def Print(self):
        pass

    def Stop(self):
        pass

    def LoadPage(self, fname):
        pass

    def SetPage(self, htmltext, basepath):
        pass

    def Sleep(self):
        pass

    def Awake(self):
        pass
