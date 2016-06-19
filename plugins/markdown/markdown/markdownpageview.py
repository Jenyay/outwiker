# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.system import getImagesDir
from outwiker.gui.texteditor import TextEditor
from outwiker.pages.wiki.basewikipageview import BaseWikiPageView
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.actions.polyactionsid import *

from .toolbar import MarkdownToolBar
from .markdownhtmlgenerator import MarkdownHtmlGenerator


class MarkdownPageView(BaseWikiPageView):
    def __init__(self, parent, *args, **kwds):
        super(MarkdownPageView, self).__init__(parent, *args, **kwds)
        self.imagesDir = getImagesDir()

    def _isHtmlCodeShown(self):
        return True

    def _getHtmlGenerator(self, page):
        return MarkdownHtmlGenerator(page)

    def getTextEditor(self):
        return TextEditor

    def _getName(self):
        return u"markdown"

    def _getPageTitle(self):
        return _(u"Markdown")

    def _getMenuTitle(self):
        return _(u"Markdown")

    def _createToolbar(self, mainWindow):
        return MarkdownToolBar(mainWindow, mainWindow.auiManager)

    def _getPolyActions(self):
        return [
            BOLD_STR_ID,
            ITALIC_STR_ID,
            BOLD_ITALIC_STR_ID,
            HEADING_1_STR_ID,
            HEADING_2_STR_ID,
            HEADING_3_STR_ID,
            HEADING_4_STR_ID,
            HEADING_5_STR_ID,
            HEADING_6_STR_ID,
            # PREFORMAT_STR_ID,
            # CODE_STR_ID,
            # HORLINE_STR_ID,
            # LINK_STR_ID,
            # LIST_BULLETS_STR_ID,
            # LIST_NUMBERS_STR_ID,
            # HTML_ESCAPE_STR_ID,
            # CURRENT_DATE,
        ]

    def _getSpecificActions(self):
        return []

    def _getCacher(self, page, application):
        return HtmlCache(page, application)

    def _createWikiTools(self):
        assert self.mainWindow is not None

        self._addFontTools()
        self._addToolbarSeparator()
        self._addHeadingTools()


    def _addFontTools(self):
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self.toolsMenu

        # Bold
        self._application.actionController.getAction(BOLD_STR_ID).setFunc(
            lambda param: self.turnText(u"**", u"**"))

        self._application.actionController.appendMenuItem(BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            BOLD_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold.png"),
            fullUpdate=False)

        # Italic
        self._application.actionController.getAction(ITALIC_STR_ID).setFunc(
            lambda param: self.turnText(u"*", u"*"))

        self._application.actionController.appendMenuItem(ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_italic.png"),
            fullUpdate=False)

        # Bold italic
        bold_italic_action = self._application.actionController.getAction(
            BOLD_ITALIC_STR_ID)
        bold_italic_action.setFunc(lambda param: self.turnText(u"**_", u"_**"))

        self._application.actionController.appendMenuItem(BOLD_ITALIC_STR_ID,
                                                          menu)
        self._application.actionController.appendToolbarButton(
            BOLD_ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold_italic.png"),
            fullUpdate=False)

    def _addHeadingTools(self):
        """
        Added headings buttons
        """
        self._headingMenu = wx.Menu()
        self.toolsMenu.AppendSeparator()
        self.toolsMenu.AppendSubMenu(self._headingMenu, _(u"Heading"))

        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self._headingMenu

        self._application.actionController.getAction(HEADING_1_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"# "))
        self._application.actionController.getAction(HEADING_2_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"## "))
        self._application.actionController.getAction(HEADING_3_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"### "))
        self._application.actionController.getAction(HEADING_4_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"#### "))
        self._application.actionController.getAction(HEADING_5_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"##### "))
        self._application.actionController.getAction(HEADING_6_STR_ID).setFunc(lambda param: self._toddleSelectedLinesPrefix(u"###### "))

        self._application.actionController.appendMenuItem(HEADING_1_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_1_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_1.png"),
                                                               fullUpdate=False)

        self._application.actionController.appendMenuItem(HEADING_2_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_2_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_2.png"),
                                                               fullUpdate=False)

        self._application.actionController.appendMenuItem(HEADING_3_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_3_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_3.png"),
                                                               fullUpdate=False)

        self._application.actionController.appendMenuItem(HEADING_4_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_4_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_4.png"),
                                                               fullUpdate=False)

        self._application.actionController.appendMenuItem(HEADING_5_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_5_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_5.png"),
                                                               fullUpdate=False)

        self._application.actionController.appendMenuItem(HEADING_6_STR_ID, menu)
        self._application.actionController.appendToolbarButton(HEADING_6_STR_ID,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "text_heading_6.png"),
                                                               fullUpdate=False)

    def _addToolbarSeparator(self):
        toolbar = self.mainWindow.toolbars[self._getName()]
        toolbar.AddSeparator()

    def _toddleSelectedLinesPrefix(self, prefix):
        editor = self._application.mainWindow.pagePanel.pageView.codeEditor
        editor.toddleSelectedLinesPrefix(prefix)
