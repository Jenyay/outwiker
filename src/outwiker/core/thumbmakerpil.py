# -*- coding: utf-8 -*-

from PIL import Image

from outwiker.core.thumbmakerbase import ThumbmakerBase


class ThumbmakerPil(ThumbmakerBase):
    def __init__(self):
        super(ThumbmakerPil, self).__init__()
        self._quality = Image.ANTIALIAS

    def _rescale(self, image, width_new, height_new, fname_out):
        newimage = image.resize((width_new, height_new), self._quality)
        newimage.save(fname_out)

    def _loadImage(self, fname):
        return Image.open(fname)

    def _getSize(self, image):
        return image.size
