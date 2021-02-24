# -*- coding: utf-8 -*-

import re

from pyparsing import Regex

from outwiker.core.thumbexception import ThumbException
from outwiker.core.defines import PAGE_ATTACH_DIR
from .pagethumbmaker import PageThumbmaker


class ThumbnailFactory:
    """
    Класс для создания токена ThumbnailToken
    """
    @staticmethod
    def make(page, thumb_size):
        return ThumbnailToken(page, thumb_size).getToken()


class ThumbnailToken:
    """
    Класс, содержащий все необходимое для разбора и создания превьюшек
    картинок на вики-странице
    """

    def __init__(self, page, thumb_size):
        self._page = page
        self._thumb_size = thumb_size
        self._thumbmaker = PageThumbmaker()

    def getToken(self):
        result = Regex(r"""%\s*?
                        (?:
                            (?:thumb\s+)?
                            (?:width\s*?=\s*?(?P<width>\d+)
                            |height\s*?=\s*?(?P<height>\d+)
                            |maxsize\s*?=\s*?(?P<maxsize>\d+))\s*?
                            (?:px)?
                            |thumb\s*?
                        )\s*?
                        %\s*?
                        Attach:(?P<fname>.*?\.(?:jpe?g|bmp|gif|tiff?|png|webp))\s*?%%""",
                       re.IGNORECASE | re.VERBOSE)
        result = result.setParseAction(self.__convertThumb)("thumbnail")
        return result

    def __convertThumb(self, s, l, t):
        if t["width"] is not None:
            size = int(t["width"])
            func = self._thumbmaker.createThumbByWidth

        elif t["height"] is not None:
            size = int(t["height"])
            func = self._thumbmaker.createThumbByHeight

        elif t["maxsize"] is not None:
            size = int(t["maxsize"])
            func = self._thumbmaker.createThumbByMaxSize

        else:
            size = self._thumb_size
            func = self._thumbmaker.createThumbByMaxSize

        fname = t["fname"]

        try:
            thumb = func(self._page, fname, size)

        except (ThumbException, IOError):
            return _("<b>Can't create thumbnail for \"{}\"</b>").format(fname)

        return '<a href="%s/%s"><img src="%s"/></a>' % (
            PAGE_ATTACH_DIR,
            fname,
            thumb.replace("\\", "/")
        )
