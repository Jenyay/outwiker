import os

from typing import List

import wx

from outwiker.app.services.attachment import attachFiles
from outwiker.gui.dialogs.messagebox import MessageBox


class BaseDropFilesTarget(wx.FileDropTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и панелью с прикрепленными файлами.
    """
    def __init__(self, application, targetWindow):
        super().__init__()
        self._application = application
        self._targetWindow = targetWindow
        self._targetWindow.SetDropTarget(self)

    def destroy(self):
        self._targetWindow.SetDropTarget(None)
        self._targetWindow = None

    @property
    def targetWindow(self) -> wx.Window:
        return self._targetWindow

    def correctFileNames(self, files: List[str]) -> List[str]:
        if len(files) == 1 and '\n' in files[0]:
            files = files[0].split('\n')

        file_protocol = 'file://'

        correctedFiles = []
        for fname in files:
            if not fname.strip():
                continue

            if fname.startswith(file_protocol):
                fname = fname[len(file_protocol):]

            correctedFiles.append(fname)

        return correctedFiles

    def OnDropFiles(self, x: int, y: int, files: List[str]) -> bool:
        raise NotImplementedError


class PageItemsDropFilesTarget(BaseDropFilesTarget):
    def OnDropFiles(self, x, y, files):
        correctedFiles = self.correctFileNames(files)
        page = self.targetWindow.HitTest((x, y))
        if page is not None:
            file_names = [os.path.basename(fname) for fname in correctedFiles]

            text = _("Attach files to the note '{title}'?\n\n{files}").format(
                title=page.display_title, files="\n".join(file_names)
            )

            if (
                MessageBox(
                    text,
                    _("Attach files to the note?"),
                    wx.YES_NO | wx.ICON_QUESTION,
                )
                == wx.YES
            ):
                attachFiles(self._application.mainWindow, page, correctedFiles)
            return True
        return False
