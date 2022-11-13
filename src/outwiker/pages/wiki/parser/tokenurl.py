# -*- coding: utf-8 -*-

import re

from pyparsing import Regex

from outwiker.utilites.urls import is_url
import outwiker.core.cssclasses as css


class UrlFactory (object):
    @staticmethod
    def make(parser):
        return UrlToken(parser).getToken()


class UrlToken (object):
    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        token = Regex(
            r'((?# Начало разбора IP )(?<!\.)(?:25[0-5]|2[0-4]\d|1\d\d|0?[1-9]\d|0{,2}[1-9])(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d?\d)){3}(?!\.[0-9])(?!\w)(?# Конец разбора IP )|(((news|telnet|nttp|file|http|ftp|https|page)://)|(www|ftp)\.)[-\w0-9\.]+[-\w0-9]+)(:[0-9]*)?(/([-\w0-9_,\$\.\+\!\*\(\):@|&=\?/~\#\%]*[-\w0-9_\$\+\!\*\(\):@|&=\?/~\#\%])?)?', re.IGNORECASE)("url")

        token.setParseAction(self.__convertToUrlLink)
        return token

    def __convertToUrlLink(self, s, l, t):
        """
        Преобразовать ссылку на интернет-адрес
        """
        if not is_url(t[0]):
            return self.__getUrlTag("http://" + t[0], t[0])

        return self.__getUrlTag(t[0], t[0])

    def __getUrlTag(self, url, comment):
        if url.startswith('page://'):
            return f'<a class="{css.CSS_WIKI} {css.CSS_LINK_PAGE}" href="{url}">{comment}</a>'

        return f'<a class="{css.CSS_WIKI}" href="{url}">{comment}</a>'
