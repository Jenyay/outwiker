# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.events import PageUpdateNeededParams

from webpage.webnotepage import WebNotePage


class DisableScriptsAction (BaseAction):
    """Enable / disable scripts on WebPage."""

    stringId = u"WebPageDisableScripts"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Disable scripts on page")


    @property
    def description (self):
        return _(u"WebPage. Enable / disable scripts on downloaded page.")


    def run (self, checked):
        assert self._application.selectedPage.getTypeString() == WebNotePage.getTypeString()

        self._application.selectedPage.disableScripts = checked
        self._application.onPageUpdateNeeded (self._application.selectedPage,
                                              PageUpdateNeededParams(None))
