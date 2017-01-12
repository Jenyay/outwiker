# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import testreadonly, testPageTitle
from outwiker.core.exceptions import ReadonlyException

from hackpage.gui.changeuiddialog import (ChangeUidDialog,
                                          ChangeUidDialogController)


@testreadonly
def changeUidWithDialog(page, application):
    """
    Show dialog to change page UID
    """
    if page is None or page.parent is None:
        return

    if page.readonly:
        raise ReadonlyException

    with ChangeUidDialog(application.mainWindow) as dlg:
        dlgController = ChangeUidDialogController(application, dlg, page)
        result = dlgController.showDialog()

        if result == wx.ID_OK:
            # Не отлавливаем исключения, поскольку считаем,
            # что правильность идентификатора проверил DialogController
            application.pageUidDepot.changeUid(page, dlg.uid)


@testreadonly
def setAliasWithDialog(page, application):
    """
    Show dialog to set page alias
    """
    if page is None or page.parent is None:
        return

    if page.readonly:
        raise ReadonlyException

    defaultValue = page.alias if page.alias is not None else u''
    with wx.TextEntryDialog(application.mainWindow,
                            _(u'Enter new page alias'),
                            _(u'Set page alias'),
                            defaultValue) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            page.alias = dlg.GetValue()


@testreadonly
def setPageFolderWithDialog(page, application):
    """
    Change page folder and set alias which matches old display_title
    """
    if page is None or page.parent is None:
        return

    if page.readonly:
        raise ReadonlyException

    oldTitle = page.title
    oldDisplayTitle = page.display_title

    with wx.TextEntryDialog(application.mainWindow,
                            _(u'Enter the page folder name'),
                            _(u'Set page folder'),
                            oldTitle) as dlg:
        while True:
            result = dlg.ShowModal()
            if result != wx.ID_OK:
                break

            if testPageTitle(dlg.GetValue()):
                page.title = dlg.GetValue()
                page.alias = oldDisplayTitle
                break
