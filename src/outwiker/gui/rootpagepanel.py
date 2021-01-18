# coding: utf-8

import wx

from .basepagepanel import BasePagePanel
from .controls.pagelist import PageList, EVT_PAGE_CLICK
from .controls.pagelist_columns import ColumnsFactory
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.gui.guiconfig import GeneralGuiConfig


class RootPagePanel(BasePagePanel):
    """Page panel for the notes root"""

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._createGUI()

    def _createGUI(self):
        self._panels = [
            NotesTreePathPanel(self, self._application),
            ButtonsPanel(self, self._application),
            BookmarksPanel(self, self._application),
        ]

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        for panel in self._panels:
            mainSizer.Add(panel, flag=wx.EXPAND | wx.ALL, border=4)

        self.SetSizer(mainSizer)
        self.Layout()
        self.SetupScrolling()

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


class BookmarksPanel(wx.Panel):
    '''
    Panel with bookmarks list
    '''
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self._config = GeneralGuiConfig(self._application.config)
        self._createGUI()

    def updatePanel(self):
        self._updateBookmarks()

    def clear(self):
        # wx.SafeYield()
        self._pageList.updateColumnsWidth()
        columns_string = ColumnsFactory.toString(self._pageList.getColumns())
        self._config.bookmarksHeaders.value = columns_string

    def _updateBookmarks(self):
        assert self._application.wikiroot is not None

        wikiroot = self._application.wikiroot
        page_list = [wikiroot.bookmarks[n]
                     for n
                     in range(len(wikiroot.bookmarks))
                     if wikiroot.bookmarks[n] is not None]
        self._pageList.setPageList(page_list)

    def _createPageList(self):
        pageList = PageList(self)
        pageList.SetMinSize((-1, 250))

        columnsFactory = ColumnsFactory()
        columns = columnsFactory.createColumnsFromString(self._config.bookmarksHeaders.value)
        if not columns:
            columns = columnsFactory.createDefaultColumns()

        pageList.setColumns(columns)
        pageList.Bind(EVT_PAGE_CLICK, handler=self._onPageClick)
        return pageList

    def _createGUI(self):
        self._bookmarksLabel = wx.StaticText(self, label=_('Bookmarks'))
        self._pageList = self._createPageList()

        bookmarksSizer = wx.FlexGridSizer(cols=1)
        bookmarksSizer.AddGrowableCol(0)
        bookmarksSizer.AddGrowableRow(1)

        bookmarksSizer.Add(self._bookmarksLabel,
                           flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                           border=4)

        bookmarksSizer.Add(self._pageList,
                           flag=wx.EXPAND | wx.ALL,
                           border=4)

        self.SetSizer(bookmarksSizer)

    def _onPageClick(self, event):
        self._application.selectedPage = event.page
