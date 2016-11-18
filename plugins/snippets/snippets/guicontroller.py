# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.system import getSpecialDirList

from .i18n import get_
from .snippetsloader import SnippetsLoader
from .defines import SNIPPETS_DIR
from .snippetparser import SnippetParser


class GuiController(object):
    def __init__(self, application):
        self._application = application

        self._menu = None
        self._mainMenu = None

        self.MENU_POS = 6
        self._menuName = None

    def initialize(self):
        global _
        _ = get_()

        if self._application.mainWindow is not None:
            self._mainMenu = self._application.mainWindow.mainMenu
            self._menuName = _(u'Snippets')
            self._createMenu()

    def _createMenu(self):
        sl = SnippetsLoader(getSpecialDirList(SNIPPETS_DIR))
        snippets_tree = sl.getSnippets()

        self._menu = wx.Menu(u'')
        self._buildTree(snippets_tree, self._menu)
        self._mainMenu.Insert(self.MENU_POS, self._menu, self._menuName)

    def _buildTree(self, snippets_tree, menu):
        # Create menu items
        for snippet in snippets_tree.snippets:
            name = os.path.basename(snippet)[:-4]
            menu_item_id = wx.Window.NewControlId()
            menu.Append(menu_item_id, name)

            self._application.mainWindow.Bind(
                wx.EVT_MENU,
                lambda event: self._onClick(snippet),
                id=menu_item_id
            )

        # Create submenus
        menu.AppendSeparator()
        for subdir in snippets_tree.dirs:
            submenu = wx.Menu(u'')
            self._buildTree(subdir, submenu)
            menu.AppendSubMenu(submenu, subdir.name)

    def _destroyMenu(self):
        index = self._mainMenu.FindMenu(self._menuName)
        assert index != wx.NOT_FOUND

        self._mainMenu.Remove(index)
        self._menu = None

    def destroy(self):
        if self._application.mainWindow is not None:
            self._destroyMenu()

    def _onClick(self, snippet):
        editor = self._getEditor()
        if editor is not None:
            parser = SnippetParser(snippet)
            text = parser.process()
            editor.replaceText(text)

    def _getEditor(self):
        if self._application.selectedPage is None:
            return None

        pageView = self._application.mainWindow.pagePanel.pageView

        if 'GetEditor' in dir(pageView):
            return pageView.GetEditor()
