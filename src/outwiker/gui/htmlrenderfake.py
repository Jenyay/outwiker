# -*- coding: utf-8 -*-

from .htmlrender import HtmlRender


class HtmlRenderFake(HtmlRender):
    def __init__(self, parent):
        HtmlRender.__init__(self, parent)

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
