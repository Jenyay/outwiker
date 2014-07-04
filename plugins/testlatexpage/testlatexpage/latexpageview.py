# -*- coding: UTF-8 -*-

from outwiker.gui.texteditor import TextEditor

from outwiker.pages.wiki.basewikipageview import BaseWikiPageView
from outwiker.pages.wiki.htmlcache import HtmlCache

from .toolbar import LatexToolBar
from .latexhtmlgenerator import LatexHtmlGenerator


class LatexPageView (BaseWikiPageView):
    def __init__ (self, parent, *args, **kwds):
        super (LatexPageView, self).__init__ (parent, *args, **kwds)


    def _isHtmlCodeShown (self):
        return True


    def _getHtmlGenerator (self, page):
        return LatexHtmlGenerator (page)


    def getTextEditor(self):
        return TextEditor


    def _getName (self):
        return u"latex"


    def _getPageTitle (self):
        return _(u"LaTeX")


    def _getMenuTitle (self):
        return _(u"LaTeX")


    def _createToolbar (self, mainWindow):
        return LatexToolBar(mainWindow, mainWindow.auiManager)


    def _getPolyActions (self):
        return []


    def _getSpecificActions (self):
        return []


    def _getCacher (self, page, application):
        return HtmlCache (page, application)


    def _createWikiTools (self):
        pass
