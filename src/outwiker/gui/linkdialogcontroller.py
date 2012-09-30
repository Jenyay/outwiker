#!/usr/bin/env python
#-*- coding: utf-8 -*-


from .linkdialog import LinkDialog
from outwiker.core.commands import getClipboardText


class LinkDialogContoller (object):
    """
    Контроллер для управления классом LinkDialog
    """
    def __init__ (self, parent, selectedString):
        """
        parent - родительское окно
        selectedString - строка, выделенная в редакторе
        """
        self.parent = parent
        self.selectedString = selectedString
        self.link = u""
        self.comment = u""


    def _isLink (self, text):
        lowerString = text.lower()
        return (lowerString.startswith (u"http://") or 
                lowerString.startswith (u"https://") or
                lowerString.startswith (u"ftp://"))


    def showDialog (self):
        comment = self.selectedString
        link = self._findLink()

        dlg = LinkDialog (self.parent, link, comment)

        result = dlg.ShowModal()
        self.link = dlg.linkText.GetValue()

        self.comment = dlg.commentText.GetValue()
        if len (self.comment) == 0:
            self.comment = self.link

        dlg.Destroy()

        return result


    def _findLink (self):
        """
        Попытаться найти ссылку или в выделенном тексте, или в буфере обмена
        """
        if self._isLink (self.selectedString):
            return self.selectedString

        clipboardText = getClipboardText()
        if clipboardText != None and self._isLink (clipboardText):
            return clipboardText

        return u""
