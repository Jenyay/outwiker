# -*- coding: UTF-8 -*-

from outwiker.gui.texteditor import TextEditor

from outwiker.pages.wiki.basewikipageview import BaseWikiPageView
from outwiker.pages.wiki.htmlcache import HtmlCache

from .toolbar import MarkdownToolBar
from .markdownhtmlgenerator import MarkdownHtmlGenerator


class MarkdownPageView (BaseWikiPageView):
    def __init__ (self, parent, *args, **kwds):
        super (MarkdownPageView, self).__init__ (parent, *args, **kwds)


    def _isHtmlCodeShown (self):
        return True


    def _getHtmlGenerator (self, page):
        return MarkdownHtmlGenerator (page)


    def getTextEditor(self):
        return TextEditor


    def _getName (self):
        return u"markdown"


    def _getPageTitle (self):
        return _(u"Markdown")


    def _getMenuTitle (self):
        return _(u"Markdown")


    def _createToolbar (self, mainWindow):
        return MarkdownToolBar(mainWindow, mainWindow.auiManager)


    def _getPolyActions (self):
        return []


    def _getSpecificActions (self):
        return []


    def _getCacher (self, page, application):
        return HtmlCache (page, application)


    def _createWikiTools (self):
        pass
