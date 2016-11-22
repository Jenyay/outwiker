# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.system import getSpecialDirList
from outwiker.core.commands import MessageBox
from outwiker.utilites.textfile import readTextFile

from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.gui.variablesdialog import VariablesDialogController
import snippets.defines as defines

from jinja2 import TemplateError


class GuiController(object):
    def __init__(self, application):
        self._application = application

        self._menu = None
        self._mainMenu = None

        self.MENU_POS = 6
        self._menuName = None

        self._snippets_id = None
        self._varDialogController = VariablesDialogController(
            self._application
        )

    def initialize(self):
        global _
        _ = get_()

        if self._application.mainWindow is not None:
            self._mainMenu = self._application.mainWindow.mainMenu
            self._menuName = _(u'Snippets')
            self._createMenu()
            self._varDialogController.onFinishDialog += self._onFinishDialog

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
            self._varDialogController.onFinishDialog -= self._onFinishDialog

        self._varDialogController.destroy()

    def _onClick(self, event):
        assert event.GetId() in self._snippets_id
        snippet_fname = self._snippets_id[event.GetId()]

        editor = self._getEditor()
        if editor is not None:
            try:
                template = self._loadTemplate(snippet_fname)
            except EnvironmentError:
                MessageBox(
                    _(u"Can't read the snippet\n{}").format(snippet_fname),
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)
                return

            selectedText = editor.GetSelectedText()
            try:
                self._varDialogController.ShowDialog(selectedText, template)
            except TemplateError as e:
                text = _(u'Template error:\n{}').format(unicode(e.message))
                editor.replaceText(text)

    def _loadTemplate(self, fname):
        template = readTextFile(fname)
        if template.endswith(u'\n'):
            template = template[:-1]
        return template

    def _getEditor(self):
        if self._application.selectedPage is None:
            return None
        pageView = self._application.mainWindow.pagePanel.pageView
        if 'GetEditor' in dir(pageView):
            return pageView.GetEditor()

    def _onFinishDialog(self, params):
        editor = self._getEditor()
        if editor is not None:
            editor.replaceText(params.text)
