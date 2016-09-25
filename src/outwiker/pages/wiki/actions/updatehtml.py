# -*- coding: UTF-8 -*-

from outwiker.core.events import PageUpdateNeededParams
from outwiker.gui.baseaction import BaseAction


class WikiUpdateHtmlAction (BaseAction):
    """
    Обновить (пересоздать) код HTML
    """
    stringId = u"WikiUpdateHtml"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Update HTML Code")


    @property
    def description (self):
        return _(u"Update HTML code for wiki page")


    def run (self, params):
        selectedPage = self._application.selectedPage

        assert selectedPage is not None
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        self._application.onPageUpdateNeeded(selectedPage,
                                             PageUpdateNeededParams(True))
