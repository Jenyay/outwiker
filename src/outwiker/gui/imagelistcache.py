# -*- coding: utf-8 -*-

from typing import Dict

from .controls.safeimagelist import SafeImageList
from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT
from outwiker.gui.images import readImage


class ImageListCache:
    def __init__(self, defaultImage: str):
        self._defaultImage = readImage(defaultImage, ICONS_WIDTH, ICONS_HEIGHT)
        assert self._defaultImage.IsOk()

        self._imagelist = SafeImageList(self._defaultImage.Width,
                                        self._defaultImage.Height)

        self._iconsCache: Dict[str, int] = {}
        self._defaultId = None
        self.clear()

    def add(self, fname: str) -> int:
        '''
        Return image ID from ImageList or default image ID
        '''
        if fname in self._iconsCache:
            return self._iconsCache[fname]

        image = readImage(fname, ICONS_WIDTH, ICONS_HEIGHT)

        imageId = 0
        if image.IsOk():
            imageId = self._imagelist.Add(image)
            self._iconsCache[fname] = imageId

        return imageId

    def replace(self, fname: str) -> int:
        '''
        Replace an existing picture in ImageList and return image ID.
        If the picture does not exist in the list, it will be added.
        '''
        imageId = 0
        if fname not in self._iconsCache:
            return self.add(fname)

        imageId = self._iconsCache[fname]
        bitmap = readImage(fname, ICONS_WIDTH, ICONS_HEIGHT)

        if not bitmap.IsOk():
            return imageId

        self._imagelist.Replace(imageId, bitmap)
        return imageId

    def clear(self):
        self._iconsCache = {}
        self._imagelist.RemoveAll()
        self._defaultId = self._imagelist.Add(self._defaultImage)

    def getDefaultImageId(self) -> int:
        return self._defaultId

    def getImageList(self):
        return self._imagelist
