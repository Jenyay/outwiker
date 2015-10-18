# -*- coding: UTF-8 -*-

import os
import os.path

from outwiker.libs.pyparsing import QuotedString
from texrender import getTexRender
from outwiker.pages.wiki.thumbnails import Thumbnails


class TexFactory (object):
    @staticmethod
    def make (parser):
        return TexToken(parser).getToken()


class TexToken (object):
    """
    Класс токена для разбора формул
    """
    texStart = "{$"
    texEnd = "$}"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        return QuotedString (TexToken.texStart,
                             endQuoteChar = TexToken.texEnd,
                             multiline = True).setParseAction(self.makeTexEquation)("tex")


    def makeTexEquation (self, s, l, t):
        eqn = t[0].strip()
        if len (eqn) == 0:
            return u""

        thumb = Thumbnails(self.parser.page)

        try:
            path = thumb.getThumbPath (True)
        except IOError:
            return u"<b>{}</b>".format(_(u"Can't create thumbnails directory"))

        tex = getTexRender (path)

        try:
            image_fname = tex.makeImage (eqn)
        except IOError:
            return u"<b>{}</b>".format(_(u"Can't create image file"))

        image_path = os.path.join (Thumbnails.getRelativeThumbDir(), image_fname)
        result = u'<img src="{image}"/>'.format (image=image_path.replace ("\\", "/"))

        return result
