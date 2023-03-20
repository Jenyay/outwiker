# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

import wx
from wx.svg import SVGimage

from outwiker.core.exceptions import InvalidImageFormat
from outwiker.core.images import isSVG, isImage


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

        bitmap_corrected = self._correctSize(bitmap)
        return super().Add(bitmap_corrected)

    def AddFromFile(self, fname: Union[str, Path]) -> int:
        fname = str(fname)
        if isImage(fname):
            bitmap = wx.Bitmap(fname)
        elif isSVG(fname):
            with open(fname, 'rb') as fp:
                data = fp.read()
                svg = SVGimage.CreateFromBytes(data)
            bitmap = svg.ConvertToScaledBitmap((self._width, self._height))
        else:
            raise InvalidImageFormat(fname)

        return self.Add(bitmap)

    def _correctSize(self, bitmap):
        """
        Convert bitmap to valid size
        """
        size_src = bitmap.GetSize()
        # Create transparent bitmap
        bitmap_new = wx.Bitmap(self._width, self._height)
        dc = wx.MemoryDC(bitmap_new)
        dc.SetBackground(wx.Brush("magenta"))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        bitmap_new.SetMaskColour("magenta")

        scale_x = float(size_src[0]) / float(self._width)
        scale_y = float(size_src[1]) / float(self._height)

        max_scale = max(scale_x, scale_y)
        image_new = bitmap.ConvertToImage()
        if max_scale >= 1.0:
            image_new.Rescale(int(size_src[0] / max_scale),
                              int(size_src[1] / max_scale))

        size_new = image_new.GetSize()
        result_image = bitmap_new.ConvertToImage()
        paste_x = (self._width - size_new[0]) // 2
        paste_y = (self._height - size_new[1]) // 2
        result_image.Paste(image_new, paste_x, paste_y)

        return result_image.ConvertToBitmap()
