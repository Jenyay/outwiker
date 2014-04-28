#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex

from utils import noConvert


class UrlFactory (object):
    @staticmethod
    def make (parser):
        return UrlToken(parser).getToken()


class UrlToken (object):
    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        token =  Regex (ur"((?# Начало разбора IP )(?<!\.)(?:25[0-5]|2[0-4]\d|1\d\d|0?[1-9]\d|0{,2}[1-9])(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d?\d)){3}(?!\.?[0-9])(?!\w)(?# Конец разбора IP )|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)\.)[-\w0-9\.]+[-\w0-9]+)(:[0-9]*)?(/([-\w0-9_,\$\.\+\!\*\(\):@|&=\?/~\#\%]*[-\w0-9_\$\+\!\*\(\):@|&=\?/~\#\%])?)?", re.IGNORECASE | re.UNICODE)("url")

        token.setParseAction(self.__convertToUrlLink)
        return token


    def __convertToUrlLink (self, s, l, t):
        """
        Преобразовать ссылку на интернет-адрес
        """
        if (not t[0].startswith ("http://") and
                not t[0].startswith ("ftp://") and
                not t[0].startswith ("news://") and
                not t[0].startswith ("gopher://") and
                not t[0].startswith ("telnet://") and
                not t[0].startswith ("nttp://") and
                not t[0].startswith ("file://") and
                not t[0].startswith ("https://")
                ):
            return self.__getUrlTag ("http://" + t[0], t[0])

        return self.__getUrlTag (t[0], t[0])


    def __getUrlTag (self, url, comment):
        return '<a href="%s">%s</a>' % (url.strip(), self.parser.parseLinkMarkup (comment.strip()) )
