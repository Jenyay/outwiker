#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.linkdialogcontroller import LinkDialogContoller


def insertLink (application):
    assert application.mainWindow != None
    assert application.mainWindow.pagePanel != None

    codeEditor = application.mainWindow.pagePanel.pageView.codeEditor

    linkController = LinkDialogContoller (application.mainWindow, codeEditor.GetSelectedText())

    if linkController.showDialog() == wx.ID_OK:
        text = u'<a href="{link}">{comment}</a>'.format (comment=linkController.comment, 
                link=linkController.link)

        codeEditor.replaceText (text)
