import wx

from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.html.tabledialogcontroller import (
    TableDialogController,
    TableRowsDialogController,
)


def insertTable(application, editor):
    parent = application.mainWindow

    with TableDialog(parent) as dlg:
        controller = TableDialogController(dlg, application.config)
        if controller.showDialog() == wx.ID_OK:
            result = controller.getResult()
            editor.replaceText(result)


def insertTableRows(application, editor):
    parent = application.mainWindow

    with TableRowsDialog(parent) as dlg:
        controller = TableRowsDialogController(dlg, application.config)
        if controller.showDialog() == wx.ID_OK:
            result = controller.getResult()
            editor.replaceText(result)
