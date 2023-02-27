# -*- coding: utf-8 -*-

import wx

from outwiker.api.core.tree import testreadonly
from outwiker.api.gui.dialogs.messagebox import MessageBox
from outwiker.api.services.messages import showError
from outwiker.core.application import Application
from outwiker.core.exceptions import ReadonlyException


@testreadonly
def removePage(page: 'outwiker.core.tree.WikiPage'):
    assert page is not None

    if page.readonly:
        raise ReadonlyException

    if page.parent is None:
        showError(Application.mainWindow, _(
            "You can't remove the root element"))
        return

    if (MessageBox(_('Remove page "{}" and all subpages?\nAll attached files will also be deleted.').format(page.title),
                   _("Remove page?"),
                   wx.YES_NO | wx.ICON_QUESTION) == wx.YES):
        try:
            page.remove()
        except IOError:
            showError(Application.mainWindow, _("Can't remove page"))
