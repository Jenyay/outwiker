# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.system import getSpecialDirList
from outwiker.core.commands import MessageBox
from outwiker.utilites.textfile import readTextFile

from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.snippetparser import SnippetParser
import snippets.defines as defines


class GuiController(object):
    def __init__(self, application):
        self._application = application

        self._menu = None
        self._mainMenu = None

        self.MENU_POS = 6
        self._menuName = None

        self._snippets_id = None

    def initialize(self):
        global _
        _ = get_()

        if self._application.mainWindow is not None:
            self._mainMenu = self._application.mainWindow.mainMenu
            self._menuName = _(u'Snippets')
            self._createMenu()

    def _createMenu(self):
        self._snippets_id = {}
        sl = SnippetsLoader(getSpecialDirList(defines.SNIPPETS_DIR))
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

            self._snippets_id[menu_item_id] = snippet

            self._application.mainWindow.Bind(
                wx.EVT_MENU,
                self._onClick,
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

    def _onClick(self, event):
        assert event.GetId() in self._snippets_id
        snippet = self._snippets_id[event.GetId()]

        editor = self._getEditor()
        if editor is not None:
            selectedText = editor.GetSelectedText()

            try:
                template = readTextFile(snippet)
            except EnvironmentError:
                MessageBox(_(u"Can't read the snippet\n{}").format(snippet),
                           _(u"Error"),
                           wx.ICON_ERROR | wx.OK)
                return

            if template.endswith(u'\n'):
                template = template[:-1]

            parser = SnippetParser(template, self._application)
            text = parser.process(selectedText, self._application.selectedPage)
            editor.replaceText(text)

    def _getEditor(self):
        if self._application.selectedPage is None:
            return None

        pageView = self._application.mainWindow.pagePanel.pageView

        if 'GetEditor' in dir(pageView):
            return pageView.GetEditor()
