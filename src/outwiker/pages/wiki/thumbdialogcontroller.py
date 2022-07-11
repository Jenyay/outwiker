# -*- coding: utf-8 -*-

from pathlib import Path

from outwiker.core.attachment import Attachment
from outwiker.core.commands import isImage

from .thumbdialog import ThumbDialog


class ThumbDialogController:
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
        self.result = ""

    def showDialog(self):
        # filesList = list(
        #     filter(isImage, Attachment(self._page).getAttachRelative()))
        # filesList.sort(key=lambda a: a.lower())

        # if (self._selectedText.startswith("Attach:") and
        #         self._selectedText[len("Attach:"):] in filesList):
        #     selectedFile = self._selectedText[len("Attach:"):]
        # else:
        #     selectedFile = ""

        resultDlg = None
        selectedFile = ""

        if self._page is not None:
            attach = Attachment(self._page)
            root_dir = Path(attach.getAttachPath(create=False))

            if root_dir.exists():
                with ThumbDialog(self._parent, self._page, selectedFile) as dlg:
                    resultDlg = dlg.ShowModal()
                    self.result = self._generateText(dlg)

        return resultDlg

    def _generateText(self, dlg):
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
