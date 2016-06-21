# -*- coding: UTF-8 -*-

import wx

from markdown.links.linkdialog import LinkDialog
from markdown.links.linkdialogcontroller import LinkDialogController


def insertLink(application):
    codeEditor = application.mainWindow.pagePanel.pageView.codeEditor

    with LinkDialog(application.mainWindow) as dlg:
        linkController = LinkDialogController(application,
                                              application.selectedPage,
                                              dlg,
                                              codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            codeEditor.replaceText(linkController.linkResult)
