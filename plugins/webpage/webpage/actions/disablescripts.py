# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction
from outwiker.api.core.events import PageUpdateNeededParams

from webpage.i18n import get_
from ..defines import PAGE_TYPE_STRING


class DisableScriptsAction(BaseAction):
    """Enable / disable scripts on WebPage."""

    stringId = "WebPageDisableScripts"

    def __init__(self, application):
        self._application = application
        global _
        _ = get_()

    @property
    def title(self):
        return _("Disable scripts on page")

    @property
    def description(self):
        return _("WebPage. Enable / disable scripts on downloaded page.")

    def run(self, checked):
        assert self._application.selectedPage.getTypeString() == PAGE_TYPE_STRING

        self._application.selectedPage.disableScripts = checked
        self._application.onPageUpdateNeeded(
            self._application.selectedPage, PageUpdateNeededParams(None)
        )
