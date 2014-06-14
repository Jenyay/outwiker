# -*- coding: utf-8 -*-


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
                lowerString.startswith (u"ftp://") or
                lowerString.startswith (u"page://"))


    def showDialog (self):
        comment = self.selectedString
        link = self._findLink()

        dlg = self._createDialog (self.parent, link, comment)

        result = dlg.ShowModal()
        self.link = dlg.link

        self.comment = dlg.comment
        if len (self.comment) == 0:
            self.comment = self.link

        dlg.Destroy()

        return result


    def _createDialog (self, parent, link, comment):
        return LinkDialog (self.parent, link, comment)


    def _findLink (self):
        """
        Попытаться найти ссылку или в выделенном тексте, или в буфере обмена
        """
        if self._isLink (self.selectedString):
            return self.selectedString

        clipboardText = getClipboardText()
        if clipboardText is not None and self._isLink (clipboardText):
            return clipboardText

        return u""
