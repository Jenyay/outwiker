# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.actions import BaseAction
from outwiker.api.services.application import startFile
from outwiker.api.gui.dialogs.messagebox import MessageBox

from webpage.i18n import get_


class OpenSourceURLAction(BaseAction):
    stringId = "webpage_open_source_url"

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
            try:
                startFile(url)
            except OSError:
                text = _("Can't open URL '{}'").format(url)
                MessageBox(text, "Error", wx.ICON_ERROR | wx.OK)

    @property
    def title(self):
        return _("Open source URL in browser")

    @property
    def description(self):
        return _("WebPage. Open source URL of the page in the browser.")
