# -*- coding: utf-8 -*-

import html

from pyparsing import QuotedString

from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.utilites.urls import is_url

from .tokenattach import AttachToken
from .htmlelements import (create_anchor,
                           create_link,
                           create_link_to_page,
                           create_link_to_attached_file)
import outwiker.core.cssclasses as css


class LinkFactory(object):
    @staticmethod
    def make(parser):
        return LinkToken(parser).getToken()


class LinkToken(object):
    linkStart = "[["
    linkEnd = "]]"
    attachString = "Attach:"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(LinkToken.linkStart,
                            endQuoteChar=LinkToken.linkEnd,
                            multiline=False,
                            convertWhitespaceEscapes=False).setParseAction(self._convertToLink)("link")

    def _isHasImage(self, text: str) -> bool:
        return '<img' in text.lower()

    def _convertToLink(self, _s, _l, t):
        """
        Преобразовать ссылку
        """
        if "->" in t[0]:
            return self._convertLinkArrow(t[0])
        elif "|" in t[0]:
            return self._convertLinkLine(t[0])

        return self._convertEmptyLink(t[0])

    def _convertLinkArrow(self, text):
        """
        Преобразовать ссылки в виде [[comment -> url]]
        """
        comment, url = text.rsplit("->", 1)
        realurl = self._prepareUrl(url)

        return self._getUrlTag(realurl, html.escape(comment, False))

    def _convertLinkLine(self, text):
        """
        Преобразовать ссылки в виде [[url | comment]]
        """
        # Т.к. символ | может быть в ссылке и в тексте,
        # считаем, что после ссылки пользователь поставит пробел
        if " |" in text:
            url, comment = text.split(" |", 1)
        else:
            url, comment = text.rsplit("|", 1)
        realurl = self._prepareUrl(url)

        return self._getUrlTag(realurl, html.escape(comment, False))

    def _prepareUrl(self, url):
        """
        Подготовить адрес для ссылки.
        Если ссылка - прикрепленный файл, то создать путь до него
        """
        # Prepare URL to attached file
        if url.strip().startswith(AttachToken.attachString):
            url = url.strip()

            # Extract path to attached file
            url = url[len(AttachToken.attachString):]
            url = self._removeQuotes(url)

            return '{}/{}'.format(PAGE_ATTACH_DIR, url)

        return url

    def _removeQuotes(self, text):
        if ((text.startswith("'") and text.endswith("'")) or
                ((text.startswith('"') and text.endswith('"')))):
            text = text[1:-1]

        return text

    def _getUrlTag(self, url, comment):
        return self._generateHtmlTag(
            url.strip(),
            self.parser.parseLinkMarkup(comment.strip()))

    def _generateHtmlTag(self, url, comment):
        if (not is_url(url) and
                not url.startswith(PAGE_ATTACH_DIR + '/') and
                not url.startswith('#') and
                not url.startswith('mailto:')):
            url = 'page://' + url

        if url.startswith(PAGE_ATTACH_DIR + '/') and not self._isHasImage(comment):
            return create_link_to_attached_file(url, comment)

        if url.startswith('page://'):
            return create_link_to_page(url, comment)

        return create_link(url, comment, [css.CSS_WIKI])

    def _convertEmptyLink(self, text):
        """
        Преобразовать ссылки в виде [[link]]
        """
        textStrip = text.strip()

        if textStrip.startswith(AttachToken.attachString):
            # Ссылка на прикрепление
            attach_name = self._removeQuotes(
                    textStrip[len(AttachToken.attachString):])

            url = '{}/{}'.format(PAGE_ATTACH_DIR, attach_name)
            comment = attach_name
            return create_link_to_attached_file(url, comment)
        elif (textStrip.startswith("#") and
                self.parser.page is not None and
                self.parser.page[textStrip] is None):
            # Ссылка начинается на #, но вложенных страниц с таким именем нет,
            # значит это якорь
            return create_anchor(textStrip[1:])

        # Ссылка не на прикрепление
        url = text.strip()
        comment = text.strip()
        return self._generateHtmlTag(url, html.escape(comment, False))
