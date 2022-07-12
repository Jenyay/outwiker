# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional

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

    def _get_selected_file(self, selected_text: str) -> Optional[str]:
        prefix = "Attach:"
        selected_file = None

        if (selected_text.startswith(prefix)):
            selected_file = selected_text[len(prefix):]
            if ((selected_file.startswith('"') and selected_file.endswith('"')) or
                    (selected_file.startswith("'") and selected_file.endswith("'"))):
                selected_file = selected_file[1:-1]

            if not isImage(selected_file):
                return None

            file_path = Path(Attachment(self._page).getAttachPath(create=False),
                             selected_file)

            if not file_path.exists() or file_path.is_dir():
                return None

        return selected_file

    def showDialog(self):
        resultDlg = None
        selected_file = self._get_selected_file(self._selectedText)

        if self._page is not None:
            attach = Attachment(self._page)
            root_dir = Path(attach.getAttachPath(create=False))

            if root_dir.exists():
                with ThumbDialog(self._parent, self._page, selected_file) as dlg:
                    resultDlg = dlg.ShowModal()
                    if resultDlg == wx.ID_OK:
                        self.result = self._generate_text(dlg)

        return resultDlg

    def _generate_text(self, dlg):
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
