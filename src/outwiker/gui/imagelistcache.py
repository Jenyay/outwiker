# -*- coding: utf-8 -*-

import wx

from .controls.safeimagelist import SafeImageList


class ImageListCache(object):
    def __init__(self, defaultImage: str):
        self._defaultImage = wx.Bitmap(defaultImage)
        assert self._defaultImage.IsOk()

        self._imagelist = SafeImageList(self._defaultImage.Width,
                                        self._defaultImage.Height)

        self._iconsCache = {}           # type: Dict[str, int]
        self._defaultId = None
        self.clear()

    def add(self, fname: str) -> int:
        '''
        Return image ID from ImageList or default image ID
        '''
        if fname in self._iconsCache:
            return self._iconsCache[fname]

        image = wx.Bitmap(fname)

        imageId = 0
        if image.IsOk():
            imageId = self._imagelist.Add(image)
            self._iconsCache[fname] = imageId

        return imageId

    def clear(self):
        self._iconsCache = {}
        self._imagelist.RemoveAll()
        self._defaultId = self._imagelist.Add(self._defaultImage)

    def getDefaultImageId(self) -> int:
        return self._defaultId

    def getImageList(self):
        return self._imagelist
