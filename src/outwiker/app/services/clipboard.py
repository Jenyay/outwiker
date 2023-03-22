# -*- coding: utf-8 -*-

import os.path
from typing import Optional

import wx

from outwiker.core.treetools import generateLink
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment

from .messages import showError


def copyTextToClipboard(text: str) -> bool:
    if not wx.TheClipboard.Open():
        showError(Application.mainWindow, _("Can't open clipboard"))
        return False

    data = wx.TextDataObject(text)

    result = True
    if not wx.TheClipboard.SetData(data):
        showError(Application.mainWindow, _("Can't copy text to clipboard"))
        result = False

    wx.TheClipboard.Flush()
    wx.TheClipboard.Close()
    return result


def getClipboardText() -> Optional[str]:
    if not wx.TheClipboard.Open():
        showError(Application.mainWindow, _("Can't open clipboard"))
        return

    data = wx.TextDataObject()
    getDataResult = wx.TheClipboard.GetData(data)

    wx.TheClipboard.Close()

    if not getDataResult:
        return

    return data.GetText()


def copyPathToClipboard(page) -> bool:
    """
    Копировать путь до страницы в буфер обмена
    """
    assert page is not None
    return copyTextToClipboard(page.path)


# TODO: Сделать тест
def copyAttachPathToClipboard(page, is_current_page: bool = False) -> bool:
    """
    Копировать путь до папки с прикрепленными файлами в буфер обмена
    """
    assert page is not None
    path = Attachment(page).getAttachPath(create=True)
    if is_current_page:
        path = os.path.join(path, page.currentAttachSubdir)

    return copyTextToClipboard(path)


def copyLinkToClipboard(page) -> bool:
    """
    Копировать ссылку на страницу в буфер обмена
    """
    assert page is not None

    link = generateLink(Application, page)
    if link is not None:
        return copyTextToClipboard(link)

    return False


def copyTitleToClipboard(page) -> bool:
    """
    Копировать заголовок страницы в буфер обмена
    """
    assert page is not None
    return copyTextToClipboard(page.display_title)
