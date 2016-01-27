# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import copyTextToClipboard

from webpage.i18n import get_


class CopySourceURLToClipboardAction (BaseAction):
    stringId = u"webpage_copy_source_url"

    def __init__ (self, application):
        super (CopySourceURLToClipboardAction, self).__init__()
        self._application = application
        global _
        _ = get_()


    def run (self, params):
        page = self._application.selectedPage
        assert page is not None

        url = page.source
        if url is not None:
            copyTextToClipboard (url)


    @property
    def title (self):
        return _(u"Copy source URL to clipboard")


    @property
    def description (self):
        return _(u'WebPage. Copy source URL of the page to clipboard.')
