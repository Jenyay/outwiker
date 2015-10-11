# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty, abstractmethod
import os.path

import wx

from outwiker.core.commands import getClipboardText
from outwiker.core.attachment import Attachment


class BaseLinkDialogController (object):
    """
    Базовый класс контроллера для управления классом LinkDialog
    """
    __metaclass__ = ABCMeta


    def __init__ (self, page, dialog, selectedString):
        """
        page - текущая страница, для будет показываться диалог
        dialog - экземпляр класса LinkDialog
        selectedString - строка, выделенная в редакторе
        """
        assert page is not None
        assert dialog is not None
        assert selectedString is not None

        self._page = page
        self._dlg = dialog
        self._selectedString = selectedString

        self.link = u''
        self.comment = u''


    def showDialog (self):
        self._prepareDialog()

        result = self._dlg.ShowModal()

        if result == wx.ID_OK:
            self.link = self._dlg.link
            self.comment = self._dlg.comment

            if len (self.comment) == 0:
                self.comment = self.link

        return result


    @abstractmethod
    def createFileLink (self, fname):
        """
        Создать ссылку на прикрепленный файл
        """


    @abstractproperty
    def linkResult (self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTMl, wiki и т.п.)
        """
        pass


    def _prepareDialog (self):
        attach = Attachment (self._page)

        attachList = [self.createFileLink (fname)
                      for fname
                      in attach.getAttachRelative()
                      if (not fname.startswith (u'__')
                          or os.path.isfile (attach.getFullPath (fname)))]

        attachList.sort ()
        self._dlg.linkText.AppendItems (attachList)

        if not self._dlg.comment:
            self._dlg.comment = self._selectedString

        if not self._dlg.link:
            self._dlg.link = self._findLink()


    def _findLink (self):
        """
        Попытаться найти ссылку или в выделенном тексте, или в буфере обмена
        """
        if self._isLink (self._selectedString):
            return self._selectedString

        clipboardText = getClipboardText()
        if clipboardText is not None and self._isLink (clipboardText):
            return clipboardText

        return u''


    def _isLink (self, text):
        lowerString = text.lower()
        return (lowerString.startswith (u'http://') or
                lowerString.startswith (u'https://') or
                lowerString.startswith (u'ftp://') or
                lowerString.startswith (u'page://') or
                text.strip() in self._dlg.linkText.GetItems())
