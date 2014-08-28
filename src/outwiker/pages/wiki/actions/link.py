# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig


def insertLink (application):
    codeEditor = application.mainWindow.pagePanel.pageView.codeEditor
    config = WikiConfig (application.config)

    linkController = LinkDialogContoller (application.mainWindow,
                                          codeEditor.GetSelectedText())

    if linkController.showDialog() == wx.ID_OK:
        linkCreator = LinkCreator (config)
        text = linkCreator.create (linkController.link, linkController.comment)
        codeEditor.replaceText (text)
