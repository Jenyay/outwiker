# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import testreadonly
from outwiker.core.exceptions import ReadonlyException

from changepageuid.dialog import ChangeUidDialog
from changepageuid.dialogcontroller import DialogController


@testreadonly
def changeUidWithDialog(page, application):
    """
    Вызвать диалог для изменения UID страницы
    """
    if page is None or page.parent is None:
        return

    if page.readonly:
        raise ReadonlyException

    with ChangeUidDialog(application.mainWindow) as dlg:
        dlgController = DialogController(application, dlg, page)
        result = dlgController.showDialog()

        if result == wx.ID_OK:
            # Не отлавливаем исключения, поскольку считаем,
            # что правильность идентификатора проверил DialogController
            application.pageUidDepot.changeUid(page, dlg.uid)
