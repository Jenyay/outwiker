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
        self._panels = [
            NotesTreePathPanel(self, self._application),
            ButtonsPanel(self, self._application)
        ]

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        for panel in self._panels:
            mainSizer.Add(panel, flag=wx.EXPAND | wx.ALL, border=4)

        self.SetSizer(mainSizer)
        self.Layout()

    def UpdateView(self, page):
        for panel in self._panels:
            panel.updatePanel()

    def Clear(self):
        for panel in self._panels:
            panel.clear()

    def Print(self):
        pass

    def Save(self):
        pass

    def checkForExternalEditAndSave(self):
        pass


class ButtonsPanel(wx.Panel):
    '''
    Panel with buttons
    '''
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self._createGUI()

    def updatePanel(self):
        pass

    def clear(self):
        pass

    def _createGUI(self):
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._addNewPageButton = wx.Button(self,
                                           label=_('Create new page...'))
        self._addNewPageButton.Bind(wx.EVT_BUTTON, handler=self._onNewPage)

        buttonsSizer.Add(self._addNewPageButton,
                         flag=wx.ALIGN_LEFT | wx.ALL,
                         border=4)

        self.SetSizer(buttonsSizer)

    def _onNewPage(self, event):
        actionController = self._application.actionController
        actionController.getAction(AddChildPageAction.stringId).run(None)


class NotesTreePathPanel(wx.Panel):
    '''
    Panel with information about path to current notes tree
    '''
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self._createGUI()

    def updatePanel(self):
        if self._application.wikiroot is not None:
            self._pathTextCtrl.SetValue(self._application.wikiroot.path)

    def clear(self):
        pass

    def _createGUI(self):
        self._pathStaticText = wx.StaticText(
            self,
            label=_('Path to current notes tree'),
            style=wx.ALIGN_CENTER_HORIZONTAL)

        self._pathTextCtrl = wx.TextCtrl(self,
                                         style=wx.TE_READONLY,
                                         value=self._application.wikiroot.path)

        pathSizer = wx.FlexGridSizer(cols=2)
        pathSizer.AddGrowableCol(1)
        pathSizer.Add(self._pathStaticText,
                      flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                      border=4)
        pathSizer.Add(self._pathTextCtrl,
                      flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
                      border=4)

        self.SetSizer(pathSizer)
