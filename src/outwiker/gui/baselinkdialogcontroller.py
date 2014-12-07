# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty

import wx

from outwiker.core.commands import getClipboardText


class BaseLinkDialogController (object):
    """
    Базовый класс контроллера для управления классом LinkDialog
    """
    __metaclass__ = ABCMeta


    def __init__ (self, dialog, selectedString):
        """
        dialog - экземпляр класса LinkDialog
        selectedString - строка, выделенная в редакторе
        """
        self._dlg = dialog
        self.selectedString = selectedString

        self.link = u''
        self.comment = u''


    def showDialog (self):
        self._dlg.comment = self.selectedString
        self._dlg.link = self._findLink()

        result = self._dlg.ShowModal()

        if result == wx.ID_OK:
            self.link = self._dlg.link
            self.comment = self._dlg.comment

            if len (self.comment) == 0:
                self.comment = self.link

        return result


    @abstractproperty
    def linkResult (self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTMl, wiki и т.п.)
        """
        pass


    def _findLink (self):
        """
        Попытаться найти ссылку или в выделенном тексте, или в буфере обмена
        """
        if self._isLink (self.selectedString):
            return self.selectedString

        clipboardText = getClipboardText()
        if clipboardText is not None and self._isLink (clipboardText):
            return clipboardText

        return u''


    def _isLink (self, text):
        lowerString = text.lower()
        return (lowerString.startswith (u'http://') or
                lowerString.startswith (u'https://') or
                lowerString.startswith (u'ftp://') or
                lowerString.startswith (u'page://'))
