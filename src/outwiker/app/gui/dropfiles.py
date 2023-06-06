# -*- coding: utf-8 -*-

from typing import List

import wx


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
