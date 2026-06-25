# -*- coding: utf-8 -*-

import re

from pyparsing import Regex

from outwiker.utilites.urls import is_url
import outwiker.core.cssclasses as css
from .htmlelements import create_link_to_page, create_invalid_link_to_page


class UrlFactory:
    @staticmethod
    def make(parser):
        return UrlToken(parser).getToken()


class UrlToken:
    def __init__(self, parser):
        self.parser = parser
        self.page_protocol = "page://"

    def getToken(self):
        token = Regex(
            r"((?# Начало разбора IP )(?<!\.)(?:25[0-5]|2[0-4]\d|1\d\d|0?[1-9]\d|0{,2}[1-9])(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d?\d)){3}(?!\.[0-9])(?!\w)(?# Конец разбора IP )|(((news|telnet|nttp|file|http|ftp|https|page)://)|(www|ftp)\.)[-\w0-9\.]+[-\w0-9]+)(:[0-9]*)?(/([-\w0-9_,\$\.\+\!\*\(\):@|&=\?/~\#\%]*[-\w0-9_\$\+\!\*\(\):@|&=\?/~\#\%])?)?",
            re.IGNORECASE,
        )("url")

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
        if url.startswith(self.page_protocol):
            page_uid = url[len(self.page_protocol) :]
            if page_uid.endswith("/"):
                page_uid = page_uid[:-1]
            return self._generateLinkToPage(page_uid)

        return f'<a class="{css.CSS_WIKI}" href="{url}">{comment}</a>'

    def _generateLinkToPage(self, page_uid_src: str) -> str:
        params_pos = page_uid_src.rfind("/")
        page_uid = page_uid_src[:params_pos] if params_pos != -1 else page_uid_src

        page = self.parser.application.wikiroot.getPageByUid(page_uid)
        url = self.page_protocol + page_uid_src
        if page is not None:
            return create_link_to_page(url, page.display_title)
        else:
            return create_invalid_link_to_page(url, url)
