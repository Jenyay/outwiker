#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import cgi

from outwiker.libs.pyparsing import QuotedString

from tokenattach import AttachToken
from utils import isImage
from outwiker.core.attachment import Attachment


class LinkFactory (object):
    @staticmethod
    def make (parser):
        return LinkToken(parser).getToken()


class LinkToken (object):
    linkStart = "[["
    linkEnd = "]]"
    attachString = u"Attach:"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        return QuotedString(LinkToken.linkStart, 
                endQuoteChar = LinkToken.linkEnd, 
                multiline = False).setParseAction(self.__convertToLink)
    

    def __convertToLink (self, s, l, t):
        """
        Преобразовать ссылку
        """
        if "->" in t[0]:
            return self.__convertLinkArrow (t[0])
        elif "|" in t[0]:
            return self.__convertLinkLine (t[0])

        return self.__convertEmptyLink (t[0])


    def __convertLinkArrow (self, text):
        """
        Преобразовать ссылки в виде [[comment -> url]]
        """
        comment, url = text.split ("->")
        realurl = self.__prepareUrl (url)

        return self.__getUrlTag (realurl, cgi.escape (comment) )


    def __convertLinkLine (self, text):
        """
        Преобразовать ссылки в виде [[url | comment]]
        """
        url, comment = text.rsplit ("|", 1)
        realurl = self.__prepareUrl (url)

        return self.__getUrlTag (realurl, cgi.escape (comment) )


    def __prepareUrl (self, url):
        """
        Подготовить адрес для ссылки. Если ссылка - прикрепленный файл, то создать путь до него
        """
        if url.strip().startswith (AttachToken.attachString):
            return url.strip().replace (AttachToken.attachString, Attachment.attachDir + "/", 1)

        return url


    def __getUrlTag (self, url, comment):
        return '<A HREF="%s">%s</A>' % (url.strip(), self.parser.parseLinkMarkup (comment.strip()) )


    def __convertEmptyLink (self, text):
        """
        Преобразовать ссылки в виде [[link]]
        """
        textStrip = text.strip()

        if textStrip.startswith (AttachToken.attachString):
            # Ссылка на прикрепление
            url = textStrip.replace (AttachToken.attachString, Attachment.attachDir + "/", 1)
            comment = textStrip.replace (AttachToken.attachString, "")

        elif (textStrip.startswith ("#") and 
                self.parser.page != None and
                self.parser.page[textStrip] == None):
            # Ссылка начинается на #, но сложенных страниц с таким именем нет,
            # значит это якорь
            return '<A NAME="%s"></A>' % (textStrip[1:])
        else:
            # Ссылка не на прикрепление
            url = text.strip()
            comment = text.strip()

        return '<A HREF="%s">%s</A>' % (url, cgi.escape (comment) )
