# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.commands import isImage, showError
from outwiker.gui.windowssizesaver import WindowSizeSaver

from .thumbdialog import ThumbDialog


class ThumbDialogController:
    def __init__(self, application, parent, page, selectedText):
        """
        parent - родительское окно
        page - текущая страница (не может быть равна None)
        selectedText - текст, выбанный в редакторе
        """
        assert page is not None

        self._parent = parent
        self._page = page
        self._selectedText = selectedText.strip()

        # Files list (relative paths) from ThumbDialog. Used for testing
        self._files_list = []

        # Selected in the dialog file (relative path)
        self._selected_file = None

        # Строка, полученная из параметров, выбанных в диалоге
        self.result = ""

        self._size_saver = WindowSizeSaver('wiki_thumb_dialog',
                                           application.config)

    @property
    def filesList(self):
        return self._files_list

    @property
    def selectedFile(self):
        return self._selected_file

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
            if Attachment(self._page).getAttachRelative():
                with ThumbDialog(self._parent, self._page) as dlg:
                    self._size_saver.restoreSize(dlg)
                    dlg.SetSelectedFile(selected_file)
                    resultDlg = dlg.ShowModal()

                    self._files_list = dlg.GetFilesListRelative()
                    self._selected_file = dlg.fileName

                    if resultDlg == wx.ID_OK:
                        self.result = self._generate_text(dlg)

                    self._size_saver.saveSize(dlg)
            else:
                showError(self._parent,
                          _("Current page does not have any attachments"))

        return resultDlg

    def _generate_text(self, dlg):
        size = dlg.scale
        fname = dlg.fileName
        scaleType = dlg.scaleType

        if size == 0:
            scaleText = ""
        elif scaleType == ThumbDialog.WIDTH:
            scaleText = " width={size}".format(size=size)
        elif scaleType == ThumbDialog.HEIGHT:
            scaleText = " height={size}".format(size=size)
        elif scaleType == ThumbDialog.MAX_SIZE:
            scaleText = " maxsize={size}".format(size=size)
        else:
            raise NotImplementedError

        if len(fname) > 0:
            fileText = "Attach:{fname}".format(fname=fname)
        else:
            fileText = ""

        result = "%thumb{scale}%{fname}%%".format(
            scale=scaleText, fname=fileText)
        return result
