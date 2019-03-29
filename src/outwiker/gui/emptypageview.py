# coding: utf-8

import wx

from .basepagepanel import BasePagePanel


class RootPagePanel(BasePagePanel):
    """Page panel for the notes root"""

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        self._pathStaticText = wx.StaticText(
            self,
            label=_('Path to current notes tree'),
            style=wx.ALIGN_CENTER_HORIZONTAL)

        self._pathTextCtrl = wx.TextCtrl(self,
                                         style=wx.TE_READONLY,
                                         value=self._application.wikiroot.path)

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        pathSizer = wx.FlexGridSizer(cols=2)
        pathSizer.AddGrowableCol(1)
        pathSizer.Add(self._pathStaticText,
                      flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                      border=4)
        pathSizer.Add(self._pathTextCtrl,
                      flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
                      border=4)

        mainSizer.Add(pathSizer,
                      flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                      border=4)

        self.SetSizer(mainSizer)
        self.Layout()

    def UpdateView(self, page):
        pass

    def Print(self):
        pass

    def Save(self):
        pass

    def Clear(self):
        pass

    def checkForExternalEditAndSave(self):
        pass
