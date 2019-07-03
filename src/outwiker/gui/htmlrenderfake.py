# -*- coding: utf-8 -*-

from .htmlrender import HtmlRenderForPage


class HtmlRenderFake(HtmlRenderForPage):
    def __init__(self, parent):
        super().__init__(parent)

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
