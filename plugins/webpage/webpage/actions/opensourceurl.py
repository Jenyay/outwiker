# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getOS
from outwiker.core.commands import MessageBox


class OpenSourceURLAction (BaseAction):
    stringId = u"webpage_open_source_url"

    def __init__ (self, application):
        super (OpenSourceURLAction, self).__init__()
        self._application = application


    def run (self, params):
        page = self._application.selectedPage
        assert page is not None

        url = page.source

        if url is not None:
            try:
                getOS().startFile (url)
            except OSError:
                text = _(u"Can't execute file '%s'") % (url)
                MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)


    @property
    def title (self):
        return _(u"Open source URL in browser")


    @property
    def description (self):
        return _(u'WebPage. Open source URL of the page in the browser.')
