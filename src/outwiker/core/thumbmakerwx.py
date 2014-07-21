# -*- coding: UTF-8 -*-

import wx

from outwiker.core.thumbmakerbase import ThumbmakerBase


class ThumbmakerWx (ThumbmakerBase):
    def _rescale (self, image, width_new, height_new, fname_out):
        image.Rescale (width_new, height_new, wx.IMAGE_QUALITY_HIGH)
        image.SaveFile (fname_out, self.__getImageType (fname_out))


    def _loadImage (self, fname):
        return wx.Image (fname)


    def _getSize (self, image):
        return (image.GetWidth(), image.GetHeight())


    def __getImageType (self, fname):
        if fname.lower().endswith (".jpg") or fname.lower().endswith (".jpeg"):
            return wx.BITMAP_TYPE_JPEG

        if fname.lower().endswith (".bmp"):
            return wx.BITMAP_TYPE_BMP

        if fname.lower().endswith (".png"):
            return wx.BITMAP_TYPE_PNG

        if fname.lower().endswith (".tif") or fname.lower().endswith (".tiff"):
            return wx.BITMAP_TYPE_TIF
