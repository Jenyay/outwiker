# -*- coding: UTF-8 -*-

import wx


class SafeImageList (wx.ImageList):
    """
    ImageList which can accept any bitmap size.
    Added in OutWiker 2.0.0.795
    """
    def __init__(self, width, height):
        super(SafeImageList, self).__init__(width, height)
        self._width = width
        self._height = height

    def Add(self, bitmap):
        size_src = bitmap.GetSize()
        if size_src[0] == self._width and size_src[1] == self._height:
            return super(SafeImageList, self).Add(bitmap)

        bitmap_corrected = self._correctSize(bitmap)
        return super(SafeImageList, self).Add(bitmap_corrected)

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

        # maxsize = max(size_src[0], size_src[1])
        scale_x = float(size_src[0]) / float(self._width)
        scale_y = float(size_src[1]) / float(self._height)

        max_scale = max(scale_x, scale_y)
        image_new = bitmap.ConvertToImage()
        if max_scale >= 1.0:
            image_new.Rescale(int(size_src[0] / max_scale),
                              int(size_src[1] / max_scale))

        size_new = image_new.GetSize()
        result_image = bitmap_new.ConvertToImage()
        paste_x = (self._width - size_new[0]) / 2
        paste_y = (self._height - size_new[1]) / 2
        result_image.Paste(image_new, paste_x, paste_y)

        return result_image.ConvertToBitmap()
