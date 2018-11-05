# -*- coding: utf-8 -*-

from outwiker.core.attachment import Attachment

from .thumbdialog import ThumbDialog
from .parser.utils import isImage


class ThumbDialogController (object):
    def __init__(self, parent, page, selectedText):
        """
        parent - родительское окно
        page - текущая страница (не может быть равна None)
        selectedText - текст, выбанный в редакторе
        """
        assert page is not None

        self._parent = parent
        self._page = page
        self._selectedText = selectedText.strip()

        # Строка, полученная из параметров, выбанных в диалоге
        self.result = u""

    def showDialog(self):
        filesList = list(
            filter(isImage, Attachment(self._page).getAttachRelative()))
        filesList.sort(key=lambda a: a.lower())

        if (self._selectedText.startswith(u"Attach:") and
                self._selectedText[len(u"Attach:"):] in filesList):
            selectedFile = self._selectedText[len(u"Attach:"):]
        else:
            selectedFile = u""

        dlg = self._createDialog(self._parent, filesList, selectedFile)
        resultDlg = dlg.ShowModal()

        self.result = self.__generateText(dlg)

        dlg.Destroy()

        return resultDlg

    def _createDialog(self, parent, filesList, selectedFile):
        return ThumbDialog(parent, filesList, selectedFile)

    def __generateText(self, dlg):
        size = dlg.size
        fname = dlg.fileName
        scaleType = dlg.scaleType

        if size == 0:
            scaleText = u""
        elif scaleType == ThumbDialog.WIDTH:
            scaleText = u" width={size}".format(size=size)
        elif scaleType == ThumbDialog.HEIGHT:
            scaleText = u" height={size}".format(size=size)
        elif scaleType == ThumbDialog.MAX_SIZE:
            scaleText = u" maxsize={size}".format(size=size)
        else:
            raise NotImplementedError

        if len(fname) > 0:
            fileText = u"Attach:{fname}".format(fname=fname)
        else:
            fileText = u""

        result = u"%thumb{scale}%{fname}%%".format(
            scale=scaleText, fname=fileText)
        return result
