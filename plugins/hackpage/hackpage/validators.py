# -*- coding: utf-8 -*-

import re

import wx

from outwiker.api.gui.dialogs.messagebox import MessageBox

from hackpage.i18n import get_


class ChangeUidValidator:
    def __init__(self, application, page):
        """
        page - текущая страница, для которой показывается диалог
        """
        global _
        _ = get_()

        self._application = application
        self._page = page

    def __call__(self, value):
        """
        Return True if value is Ok and False otherwise.
        """
        value = value.strip()
        otherpage = self._application.pageUidDepot[value]

        if otherpage is not None and otherpage != self._page:
            MessageBox(
                _("Same identifier exist already"), _("Error"), wx.ICON_ERROR | wx.OK
            )
            return False

        regexp = re.compile(r"^[-\w,\$\.\+\!\*\(\):@|&=\?~\#\%]+$", re.I | re.U)
        match = regexp.match(value)

        if match is None:
            MessageBox(
                _("Identifier contain invalid character"),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )
            return False

        return True
