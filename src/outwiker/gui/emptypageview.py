# coding: utf-8

import wx

from .basepagepanel import BasePagePanel
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.open import OpenAction
from outwiker.actions.new import NewAction
from outwiker.core.commands import openWiki


class ClosedTreePanel(BasePagePanel):
    '''
    The panel showed when notes tree is closed
    '''

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        # Button to create new notes tree
        self._createNotesTreeButton = wx.Button(
            self,
            label=_('Create new notes tree...'))

        self._createNotesTreeButton.Bind(wx.EVT_BUTTON,
                                         handler=self._onCreateNotes)

        # Button to open notes tree
        self._openNotesTreeButton = wx.Button(
            self,
            label=_('Open notes tree from disk...'))
        self._openNotesTreeButton.Bind(wx.EVT_BUTTON,
                                       handler=self._onOpenNotes)

        # Buttons sizer
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(self._createNotesTreeButton,
                         flag=wx.ALL,
                         border=4)
        buttonsSizer.Add(self._openNotesTreeButton,
                         flag=wx.ALL,
                         border=4)

        # Recently opened notes tree
        recentlyText = wx.StaticText(
            self,
            label=_('Recently used notes tree:'))

        self._recentlyListBox = wx.ListBox(self, style=wx.LB_SINGLE)
        self._recentlyListBox.Bind(wx.EVT_LISTBOX_DCLICK,
                                   handler=self._onOpenSelectedNotesTree)

        self._recentlyOpenButton = wx.Button(self, label=_('Open'))
        self._recentlyOpenButton.Bind(wx.EVT_BUTTON,
                                      handler=self._onOpenSelectedNotesTree)

        self._recentlySizer = wx.FlexGridSizer(cols=1)
        self._recentlySizer.AddGrowableCol(0)
        self._recentlySizer.AddGrowableRow(1)

        self._recentlySizer.Add(recentlyText, flag=wx.ALL, border=4)
        self._recentlySizer.Add(self._recentlyListBox,
                                flag=wx.ALL | wx.EXPAND,
                                border=4)
        self._recentlySizer.Add(self._recentlyOpenButton,
                                flag=wx.ALL,
                                border=4)

        # Main sizer
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(1)

        sizer.Add(buttonsSizer, flag=wx.ALL, border=4)
        sizer.Add(self._recentlySizer, flag=wx.ALL | wx.EXPAND, border=4)

        self.SetSizer(sizer)
        self._updateNotesTree()
        self.Layout()

    def _updateNotesTree(self):
        path_list = self._application.recentWiki.get_all()
        if path_list:
            self._recentlyListBox.AppendItems(path_list)
            self._recentlyListBox.SetSelection(0)
            self._recentlySizer.ShowItems(True)
        else:
            self._recentlySizer.ShowItems(False)

    def _onCreateNotes(self, event):
        actionController = self._application.actionController
        actionController.getAction(NewAction.stringId).run(None)

    def _onOpenNotes(self, event):
        actionController = self._application.actionController
        actionController.getAction(OpenAction.stringId).run(None)

    def _onOpenSelectedNotesTree(self, event):
        openWiki(self._recentlyListBox.GetStringSelection())

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
        actionController = self._application.actionController
        actionController.getAction(AddChildPageAction.stringId).run(None)

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
