#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.linkdialogcontroller import LinkDialogContoller


class HtmlLinkAction (BaseAction):
    """
    Вставка картинки
    """
    stringId = u"HtmlLink"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Link")


    @property
    def description (self):
        return _(u"Insert link for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor

        linkController = LinkDialogContoller (self._application.mainWindow, codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            text = u'<a href="{link}">{comment}</a>'.format (comment=linkController.comment, 
                    link=linkController.link)

            codeEditor.replaceText (text)
