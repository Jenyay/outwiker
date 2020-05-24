# -*- coding: utf-8 -*-

import html

from pyparsing import QuotedString

from .tokenattach import AttachToken
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.utilites.urls import is_url


class LinkFactory(object):
    @staticmethod
    def make(parser):
        return LinkToken(parser).getToken()


class LinkToken(object):
    linkStart = "[["
    linkEnd = "]]"
    attachString = u"Attach:"

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        return QuotedString(LinkToken.linkStart,
                            endQuoteChar=LinkToken.linkEnd,
                            multiline=False,
                            convertWhitespaceEscapes=False).setParseAction(self.__convertToLink)("link")

    def __convertToLink(self, _s, _l, t):
        """
        Преобразовать ссылку
        """
        if "->" in t[0]:
            return self.__convertLinkArrow(t[0])
        elif "|" in t[0]:
            return self.__convertLinkLine(t[0])

        return self.__convertEmptyLink(t[0])

    def __convertLinkArrow(self, text):
        """
        Преобразовать ссылки в виде [[comment -> url]]
        """
        comment, url = text.rsplit("->", 1)
        realurl = self.__prepareUrl(url)

        return self.__getUrlTag(realurl, html.escape(comment, False))

    def __convertLinkLine(self, text):
        """
        Преобразовать ссылки в виде [[url | comment]]
        """
        # Т.к. символ | может быть в ссылке и в тексте,
        # считаем, что после ссылки пользователь поставит пробел
        if " |" in text:
            url, comment = text.split(" |", 1)
        else:
            url, comment = text.rsplit("|", 1)
        realurl = self.__prepareUrl(url)

        return self.__getUrlTag(realurl, html.escape(comment, False))

    def __prepareUrl(self, url):
        """
        Подготовить адрес для ссылки.
        Если ссылка - прикрепленный файл, то создать путь до него
        """
        if url.strip().startswith(AttachToken.attachString):
            return url.strip().replace(AttachToken.attachString,
                                       PAGE_ATTACH_DIR + "/", 1)

        return url

    def __getUrlTag(self, url, comment):
        return self.__generateHtmlTag(
                url.strip(),
                self.parser.parseLinkMarkup(comment.strip()))

    def __generateHtmlTag(self, url, comment):
        if (not is_url(url) and
                not url.startswith(AttachToken.attachString) and
                not url.startswith(PAGE_ATTACH_DIR + '/') and
                not url.startswith('#')):
            url = 'page://' + url

        return '<a href="{url}">{comment}</a>'.format(url=url, comment=comment)

    def __convertEmptyLink(self, text):
        """
        Преобразовать ссылки в виде [[link]]
        """
        textStrip = text.strip()

        if textStrip.startswith(AttachToken.attachString):
            # Ссылка на прикрепление
            url = textStrip.replace(
                AttachToken.attachString, PAGE_ATTACH_DIR + "/", 1)
            comment = textStrip.replace(AttachToken.attachString, "")
            return '<a href="{url}">{comment}</a>'.format(url=url, comment=comment)
        elif (textStrip.startswith("#") and
                self.parser.page is not None and
                self.parser.page[textStrip] is None):
            # Ссылка начинается на #, но вложенных страниц с таким именем нет,
            # значит это якорь
            return '<a id="{anchor}"></a>'.format(anchor=textStrip[1:])

        # Ссылка не на прикрепление
        url = text.strip()
        comment = text.strip()
        return self.__generateHtmlTag(url, html.escape(comment, False))
