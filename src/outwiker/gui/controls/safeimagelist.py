# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

import wx

from outwiker.gui.images import readImage, resizeBitmap


class SafeImageList(wx.ImageList):
    """
    ImageList which can accept any bitmap size.
    """

    def __init__(self, width: int, height: int, scale: float = 1):
        self._width = int(width * scale)
        self._height = int(height * scale)
        super().__init__(self._width, self._height)

    def Add(self, bitmap) -> int:
        size_src = bitmap.GetSize()
        if size_src[0] == self._width and size_src[1] == self._height:
            return super().Add(bitmap)

        bitmap_corrected = resizeBitmap(bitmap, self._width, self._height)
        return super().Add(bitmap_corrected)

    def AddFromFile(self, fname: Union[str, Path]) -> int:
        fname = str(fname)
        bitmap = readImage(fname, self._width, self._height)
        return self.Add(bitmap)

    def Replace(self, index: int, bitmap: wx.Bitmap) -> None:
        size_src = bitmap.GetSize()
        if size_src[0] == self._width and size_src[1] == self._height:
            super().Replace(index, bitmap)
            return

        bitmap_corrected = resizeBitmap(bitmap, self._width, self._height)
        super().Replace(index, bitmap_corrected)
