# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty, abstractmethod
from pathlib import Path

import wx

from outwiker.core.attachfilters import getHiddenFilter, notFilter
from outwiker.core.commands import getClipboardText
from outwiker.core.attachment import Attachment
from outwiker.core.pageuiddepot import PageUidDepot


class BaseLinkDialogController(metaclass=ABCMeta):
    """
    Базовый класс контроллера для управления классом LinkDialog
    """

    def __init__(self, page, dialog, selectedString):
        """
        page - текущая страница, для которой будет показываться диалог
        dialog - экземпляр класса LinkDialog
        selectedString - строка, выделенная в редакторе
        """
        assert page is not None
        assert dialog is not None
        assert selectedString is not None

        self._page = page
        self._dlg = dialog
        self._selectedString = selectedString

        self._link = ''
        self._comment = ''

    @property
    def link(self):
        return self._link

    @property
    def comment(self):
        return self._comment

    def showDialog(self):
        self._prepareDialog()

        result = self._dlg.ShowModal()

        if result == wx.ID_OK:
            self._link = self._dlg.link
            if self._isLinkToAttach(self._link):
                self._link = self.createFileLink(self._link)

            self._comment = self._dlg.comment

            if len(self._comment) == 0:
                self._comment = self._link

        return result

    @abstractproperty
    def linkResult(self) -> str:
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTML, wiki и т.п.)
        """
        pass

    @abstractmethod
    def createFileLink(self, fname: str) -> str:
        """
        Создать ссылку на прикрепленный файл
        """
        pass

    def prepareAttachLink(self, text: str) -> str:
        return text

    def _prepareDialog(self):
        attach = Attachment(self._page)
        attach_path = Path(attach.getAttachPath(create=False))
        if attach_path.exists():
            files_filter = notFilter(getHiddenFilter(self._page))
            self._dlg.linkText.SetFilterFunc(files_filter)
            self._dlg.linkText.SetRootDir(attach_path)

        if not self._dlg.comment:
            self._dlg.comment = self._selectedString

        if not self._dlg.link:
            self._dlg.link = self._findLink()

        if self._isPageLink(self._dlg.link):
            prefix = 'page://'
            uid = self._dlg.link[len(prefix):]
            page = PageUidDepot(self._page.root)[uid]
            if page is not None and not self._selectedString:
                self._dlg.comment = page.display_title

    def _findLink(self):
        """
        Попытаться найти ссылку или в выделенном тексте, или в буфере обмена
        """
        text = self.prepareAttachLink(self._selectedString)

        if self._isLink(text):
            return text

        clipboardText = getClipboardText()
        if clipboardText is not None and self._isLink(clipboardText):
            return clipboardText

        return ''

    def _isLinkToAttach(self, text):
        if not text.strip():
            return False

        attach = Attachment(self._page)
        path = Path(attach.getAttachPath(create=False), text.replace('\\', '/'))
        try:
            return path.exists()
        except OSError:
            return False

    def _isLink(self, text):
        lowerString = text.lower()
        return (lowerString.startswith('http://') or
                lowerString.startswith('https://') or
                lowerString.startswith('ftp://') or
                lowerString.startswith('page://') or
                text.startswith('#') or
                self._isLinkToAttach(text))

    def _isPageLink(self, text):
        lowerString = text.lower()
        return lowerString.startswith('page://')
