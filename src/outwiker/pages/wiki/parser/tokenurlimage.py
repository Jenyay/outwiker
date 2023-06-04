# -*- coding: utf-8 -*-

import re

from pyparsing import Regex

import outwiker.core.cssclasses as css

from .htmlelements import create_image


class UrlImageFactory:
    @staticmethod
    def make(parser):
        return UrlImageToken(parser).getToken()


class UrlImageToken:
    """
    Токен для ссылки на картинку
    """

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        token = Regex(
            r"(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[-._\w%+]+)*/[-\w_.%+]+\.(gif|png|jpe?g|bmp|tiff?|webp)",
            re.IGNORECASE,
        ).setParseAction(lambda s, l, t: create_image(t[0], [css.CSS_IMAGE]))("image")
        return token
