# -*- coding: utf-8 -*-

import os.path
import time
from typing import Optional

import wx

from outwiker.core.treetools import generateLink
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment

from .messages import showError


_CLIPBOARD_RETRY_COUNT = 10
_CLIPBOARD_RETRY_DELAY = 0.01


def _wait_clipboard_retry() -> None:
    """
    Pump pending GUI messages and wait before the next clipboard attempt.

    On Windows the OLE clipboard needs a running message loop to finish
    Open / SetData / GetData. Tests do not run the main loop, so pending
    events have to be processed explicitly between attempts.
    """
    app = wx.GetApp()
    if app is not None and not app.IsMainLoopRunning():
        wx.SafeYield()
    time.sleep(_CLIPBOARD_RETRY_DELAY)


def copyTextToClipboard(text: str) -> bool:
    clipboard_opened = False

    for _ in range(_CLIPBOARD_RETRY_COUNT):
        if wx.TheClipboard.Open():
            clipboard_opened = True
            data = wx.TextDataObject(text)
            if wx.TheClipboard.SetData(data):
                wx.TheClipboard.Flush()
                wx.TheClipboard.Close()
                return True
            wx.TheClipboard.Close()

        _wait_clipboard_retry()

    message = (
        _("Can't copy text to clipboard")
        if clipboard_opened
        else _("Can't open clipboard")
    )
    showError(wx.GetApp().getMainWindow(), message)
    return False


def getClipboardText() -> Optional[str]:
    clipboard_opened = False

    for _ in range(_CLIPBOARD_RETRY_COUNT):
        if wx.TheClipboard.Open():
            clipboard_opened = True
            data = wx.TextDataObject()
            getDataResult = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()

            if getDataResult:
                return data.GetText()

        _wait_clipboard_retry()

    if not clipboard_opened:
        showError(wx.GetApp().getMainWindow(), _("Can't open clipboard"))

    return None


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


def copyLinkToClipboard(page, application: Application) -> bool:
    """
    Копировать ссылку на страницу в буфер обмена
    """
    assert page is not None

    link = generateLink(application, page)
    if link is not None:
        return copyTextToClipboard(link)

    return False


def copyTitleToClipboard(page) -> bool:
    """
    Копировать заголовок страницы в буфер обмена
    """
    assert page is not None
    return copyTextToClipboard(page.display_title)
