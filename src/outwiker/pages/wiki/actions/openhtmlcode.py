# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiOpenHtmlCodeAction (BaseAction):
    """
    Открыть вкладку с кодом HTML
    """
    stringId = u"WikiOpenHtmlCode"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Html Code")


    @property
    def description (self):
        return _(u"Open HTML code for wiki page")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        self._application.mainWindow.pagePanel.pageView.openHtmlCode()
