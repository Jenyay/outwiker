# coding: utf-8

import wx

from .basepagepanel import BasePagePanel
from outwiker.actions.addchildpage import AddChildPageAction


class RootPagePanel(BasePagePanel):
    """Page panel for the notes root"""

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        # Path to wiki GUI
        self._pathStaticText = wx.StaticText(
            self,
            label=_('Path to current notes tree'),
            style=wx.ALIGN_CENTER_HORIZONTAL)

        self._pathTextCtrl = wx.TextCtrl(self,
                                         style=wx.TE_READONLY,
                                         value=self._application.wikiroot.path)

        # Add new note button
        self._addNewPageButton = wx.Button(self,
                                           label=_('Create new page...'))
        self._addNewPageButton.Bind(wx.EVT_BUTTON, handler=self._onNewPage)

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

        mainSizer.Add(self._addNewPageButton,
                      flag=wx.ALIGN_LEFT | wx.ALL,
                      border=4)

        self.SetSizer(mainSizer)
        self.Layout()

    def _onNewPage(self, event):
        self._application.actionController.getAction(AddChildPageAction.stringId).run(None)

    def UpdateView(self, page):
        if self._application.wikiroot is not None:
            self._pathTextCtrl.SetValue(self._application.wikiroot.path)

    def Print(self):
        pass

    def Save(self):
        pass

    def Clear(self):
        pass

    def checkForExternalEditAndSave(self):
        pass
