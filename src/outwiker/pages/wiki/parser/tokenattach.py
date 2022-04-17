# -*- coding: utf-8 -*-

import os.path
import re
from abc import ABCMeta, abstractmethod

from pyparsing import Literal, Regex

from outwiker.core.attachment import Attachment
from outwiker.core.commands import isImage
from outwiker.core.defines import PAGE_ATTACH_DIR, IMAGES_EXTENSIONS

from .utils import concatenate


class AttachFactory:
    @staticmethod
    def make(parser):
        return AttachAllToken(parser).getToken()


class AttachImagesFactory:
    @staticmethod
    def make(parser):
        return AttachImagesToken(parser).getToken()


class AttachToken(metaclass=ABCMeta):
    attachString = 'Attach:'

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        """
        Создать элементы из прикрепленных файлов.
        Отдельно картинки, отдельно все файлы
        """
        fname_without_space_token = self._getRegex()
        fname_with_space_token = self._getRegexWithSpaces()

        # File name with spaces (double quotes)
        token1 = Literal(self.attachString + '"') + fname_with_space_token + Literal('"')
        token1 = token1.setParseAction(self.convertToLink)

        # File name with spaces (single quotes)
        token2 = Literal(self.attachString + "'") + fname_with_space_token + Literal("'")
        token2 = token2.setParseAction(self.convertToLink)

        # File name without spaces
        token3 = Literal(self.attachString) + fname_without_space_token
        token3 = token3.setParseAction(self.convertToLink)

        finalToken = concatenate([token1, token2, token3])('attach')
        return finalToken

    @abstractmethod
    def _getRegex(self):
        pass

    @abstractmethod
    def _getRegexWithSpaces(self):
        pass

        # attachesAll = []

        # attaches = Attachment(self.parser.page).attachmentFull
        # attaches.sort(key=len, reverse=True)

        # for attach in attaches:
        #     fname = os.path.basename(attach)
        #     if self.filterFile(fname):
        #         attach = Literal(fname)
        #         attachesAll.append(attach)

        # finalToken = Literal(self.attachString) + concatenate(attachesAll)
        # finalToken = finalToken.setParseAction(self.convertToLink)('attach')
        # return finalToken

    @abstractmethod
    def convertToLink(self, s, l, t):
        pass


class AttachAllToken(AttachToken):
    def _getRegex(self):
        return Regex(r'[\w.=,#@^&$%;()`~/\-]+', re.I)

    def _getRegexWithSpaces(self):
        return Regex(r'[\w\s.=,#@^&$%;()`~/\-]+', re.I)

    def convertToLink(self, s, l, t):
        fname = t[1]
        return '<a href="%s/%s">%s</a>' % (PAGE_ATTACH_DIR, fname, fname)


class AttachImagesToken(AttachToken):
    def _getImagesExtensions(self):
        ext_list_str = '|'.join([r'(?:\.{})'.format(ext) for ext in IMAGES_EXTENSIONS])
        return ext_list_str

    def _getRegex(self):
        ext_list = self._getImagesExtensions()
        regexp_str = r'[\w.=,#@^&$%;()`~/\-]+?' + '(?:{})'.format(ext_list)
        return Regex(regexp_str, re.I)

    def _getRegexWithSpaces(self):
        ext_list = self._getImagesExtensions()
        regexp_str = r'[\w\s.=,#@^&$%;()`~/\-]+?' + '(?:{})'.format(ext_list)
        return Regex(regexp_str, re.I)

    def convertToLink(self, s, l, t):
        fname = t[1]
        return '<img src="%s/%s"/>' % (PAGE_ATTACH_DIR, fname)
