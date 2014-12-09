# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.linkdialog import LinkDialog
from outwiker.pages.wiki.wikilinkdialogcontroller import WikiLinkDialogController


def insertLink (application):
    codeEditor = application.mainWindow.pagePanel.pageView.codeEditor

    with LinkDialog (application.mainWindow) as dlg:
        linkController = WikiLinkDialogController (application,
                                                   application.selectedPage,
                                                   dlg,
                                                   codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            codeEditor.replaceText (linkController.linkResult)
