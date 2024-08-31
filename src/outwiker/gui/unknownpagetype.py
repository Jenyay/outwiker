# coding: utf-8

import wx

from outwiker.core.factory import PageFactory
from outwiker.core.tree import PageAdapter, WikiPage

from outwiker.gui.basepagepanel import BasePagePanel


class UnknownPageTypePanel(BasePagePanel):
    """Page panel for unknown page type"""

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        # Title
        message = _(
            'Unknown page type.\nIt is possible that an additional plugin is required to display this page.')
        self._messageStaticText = wx.StaticText(
            self,
            label=message,
            style=wx.ALIGN_CENTER_HORIZONTAL)

        # Page type
        self._pageTypeStaticText = wx.StaticText(self, label=_('Page type'))
        self._pageTypeTextCtrl = wx.TextCtrl(self, style=wx.TE_READONLY)
        self._pageTypeTextCtrl.SetMinSize((150, -1))

        pageTypeSizer = wx.FlexGridSizer(cols=2)
        pageTypeSizer.AddGrowableCol(1)
        pageTypeSizer.Add(self._pageTypeStaticText,
                          flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                          border=4)
        pageTypeSizer.Add(self._pageTypeTextCtrl,
                          flag=wx.ALIGN_LEFT | wx.ALL,
                          border=4)

        # Content
        self._contentStaticText = wx.StaticText(self, label=_('Page content:'))

        self._contentTextCtrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)

        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(3)

        sizer.Add(self._messageStaticText,
                  flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                  border=16)

        sizer.Add(pageTypeSizer,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                  border=4)

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
        self._pageTypeTextCtrl.SetValue(page.getTypeString())

    def Print(self):
        pass

    def Save(self):
        pass

    def Clear(self):
        pass

    def checkForExternalEditAndSave(self):
        pass


class UnknownPageTypeFactory(PageFactory):
    """
    The fabric to create UnknownPageTypePanel
    """

    def __init__(self, pageTypeString):
        if not pageTypeString:
            pageTypeString = 'unknown'

        self._pageTypeString = pageTypeString

    # def _getPageType(self):
    #     typeName = self._pageTypeString + 'PageType'
    #     attributes = {'getTypeString': lambda: self._pageTypeString}
    #     pagetype = type(typeName, (UnknownPage, ), attributes)
    #     return pagetype

    @property
    def title(self):
        assert False

    def getPageView(self, parent, application):
        return UnknownPageTypePanel(parent, application)

    def getPageTypeString(self):
        return self._pageTypeString

    def createPageAdapter(self, page):
        return UnknownPageAdapter(page)


class UnknownPageAdapter(PageAdapter):
    pass
