# -*- coding: UTF-8 -*-

import wx

from outwiker.pages.html.htmllinkdialogcontroller import HtmlLinkDialogController
from outwiker.gui.dialogs.linkdialog import LinkDialog


def insertLink(application):
    assert application.mainWindow is not None
    assert application.mainWindow.pagePanel is not None

    codeEditor = application.mainWindow.pagePanel.pageView.codeEditor

    with LinkDialog(application.mainWindow) as dlg:
        linkController = HtmlLinkDialogController(
            application.selectedPage,
            dlg,
            codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            codeEditor.replaceText(linkController.linkResult)
