#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.pages.wiki.thumbdialogcontroller import ThumbDialogController


class WikiThumbAction (BaseAction):
    """
    Вставка миниатюры
    """
    stringId = u"WikiThumbnail"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Thumbnail")


    @property
    def description (self):
        return _(u"Insert thumbnail on wiki page")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor

        dlgController = ThumbDialogController (self._application.mainWindow, 
                self._application.selectedPage, 
                codeEditor.GetSelectedText())

        if dlgController.showDialog() == wx.ID_OK:
            codeEditor.replaceText (dlgController.result)
