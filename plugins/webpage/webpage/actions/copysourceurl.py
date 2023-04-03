# -*- coding: utf-8 -*-

import wx

from outwiker.api.app.clipboard import copyTextToClipboard
from outwiker.api.gui.actions import BaseAction

from webpage.i18n import get_


class CopySourceURLToClipboardAction(BaseAction):
    stringId = "webpage_copy_source_url"

    def __init__(self, application):
        super().__init__()
        self._application = application
        global _
        _ = get_()

    def run(self, params):
        page = self._application.selectedPage
        assert page is not None

        url = page.source
        if url is not None:
            copyTextToClipboard(url)

    @property
    def title(self):
        return _("Copy source URL to clipboard")

    @property
    def description(self):
        return _("WebPage. Copy source URL of the page to clipboard.")
