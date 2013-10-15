#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiLinkAction (BaseAction):
    """
    Вставка миниатюры
    """
    stringId = u"WikiLink"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Link")


    @property
    def description (self):
        return _(u"Insert link for wiki page")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        config = WikiConfig (self._application.config)

        linkController = LinkDialogContoller (self._application.mainWindow, 
                codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            linkCreator = LinkCreator (config)
            text = linkCreator.create (linkController.link, linkController.comment)
            codeEditor.replaceText (text)
