# coding: utf-8

import wx

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .basepagepanel import BasePagePanel


class UnknownPageTypePanel(BasePagePanel):
    """Page panel for unknown page type"""

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        message = _(
            'Unknown page type.\nIt is possible that an additional plugin is required to display this page.')
        self._messageStaticText = wx.StaticText(
            self,
            label=message,
            style=wx.ALIGN_CENTER_HORIZONTAL)

        self._contentStaticText = wx.StaticText(self, label=_('Page content:'))

        self._contentTextCtrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)

        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(2)

        sizer.Add(self._messageStaticText,
                  flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                  border=16)

        sizer.Add(self._contentStaticText,
                  flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                  border=4)

        sizer.Add(self._contentTextCtrl,
                  flag=wx.EXPAND | wx.ALL,
                  border=4)

        self.SetSizer(sizer)
        self.Layout()

    def UpdateView(self, page):
        self._contentTextCtrl.SetValue(page.content)

    def Print(self):
        pass

    def Save(self):
        pass

    def Clear(self):
        pass

    def checkForExternalEditAndSave(self):
        pass


class UnknownPageTypeFactory (PageFactory):
    """
    The fabric to create UnknownPageTypePanel
    """

    def getPageType(self):
        return UnknownPage

    @property
    def title(self):
        assert False

    def getPageView(self, parent, application):
        return UnknownPageTypePanel(parent, application)


class UnknownPage (WikiPage):
    def __init__(self, path, title, parent, readonly=False):
        WikiPage.__init__(self, path, title, parent, readonly=True)

    @staticmethod
    def getTypeString():
        return 'unknown'
