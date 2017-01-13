# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import testreadonly, testPageTitle
from outwiker.core.exceptions import ReadonlyException

from hackpage.gui.validators import ChangeUidValidator
from hackpage.gui.textentrydialog import TextEntryDialog
from hackpage.i18n import get_


@testreadonly
def changeUidWithDialog(page, application):
    """
    Show dialog to change page UID
    """
    global _
    _ = get_()

    if page is None or page.parent is None:
        return

    if page.readonly:
        raise ReadonlyException

    title = _(u"Change page identifier")
    message = _(u'Enter new identifier for page "{}"').format(
        page.display_title)
    prefix = u'page://'
    value = application.pageUidDepot.createUid(page)
    validator = ChangeUidValidator(application, page)

    with TextEntryDialog(application.mainWindow,
                         title=title,
                         message=message,
                         prefix=prefix,
                         value=value,
                         validator=validator) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            # Не отлавливаем исключения, поскольку считаем,
            # что правильность идентификатора проверил validator
            application.pageUidDepot.changeUid(page, dlg.Value)


@testreadonly
def setAliasWithDialog(page, application):
    """
    Show dialog to set page alias
    """
    global _
    _ = get_()

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
    global _
    _ = get_()

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
