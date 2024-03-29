# -*- coding: utf-8 -*-

import re
import os.path
from abc import ABCMeta, abstractmethod

from pyparsing import Literal, Regex

import outwiker.core.cssclasses as css
from outwiker.core.defines import PAGE_ATTACH_DIR, IMAGES_EXTENSIONS
from outwiker.core.attachment import Attachment

from .utils import concatenate
from .attachregex import attach_regex_no_spaces, attach_regex_with_spaces
from .htmlelements import (
    create_link_to_attached_file,
    create_image,
    create_invalid_attached_file,
)


class AttachFactory:
    @staticmethod
    def make(parser):
        return AttachAllToken(parser).getToken()


class AttachImagesFactory:
    @staticmethod
    def make(parser):
        return AttachImagesToken(parser).getToken()


class AttachToken(metaclass=ABCMeta):
    attachString = "Attach:"

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
        token1 = (
            Literal(self.attachString + '"') + fname_with_space_token + Literal('"')
        )

        # File name with spaces (single quotes)
        token2 = (
            Literal(self.attachString + "'") + fname_with_space_token + Literal("'")
        )

        # File name without spaces
        token3 = Literal(self.attachString) + fname_without_space_token

        finalToken = concatenate([token1, token2, token3])(self._getTokenName())
        finalToken = finalToken.setParseAction(self._convertToLink)
        return finalToken

    @abstractmethod
    def _getRegex(self):
        pass

    @abstractmethod
    def _getRegexWithSpaces(self):
        pass

    @abstractmethod
    def _convertToLink(self, s, l, t):
        pass

    @abstractmethod
    def _getTokenName(self):
        pass


class AttachAllToken(AttachToken):
    def _getRegex(self):
        return Regex(attach_regex_no_spaces, re.I)

    def _getRegexWithSpaces(self):
        return Regex(attach_regex_with_spaces, re.I)

    def _convertToLink(self, s, l, t):
        fname = t[1]
        fname_fix_slash = fname.replace("\\", "/")
        href = "{dirname}/{fname}".format(dirname=PAGE_ATTACH_DIR, fname=fname_fix_slash)
        text = fname

        if Attachment(self.parser.page).exists(fname_fix_slash):
            return create_link_to_attached_file(href, text)

        return create_invalid_attached_file(fname)

    def _getTokenName(self):
        return "attach"


class AttachImagesToken(AttachToken):
    def _getImagesExtensions(self):
        ext_list_str = "|".join([r"(?:\.{})".format(ext) for ext in IMAGES_EXTENSIONS])
        return ext_list_str

    def _getRegex(self):
        ext_list = self._getImagesExtensions()
        regexp_str = r"[\w.=,#@^&$%;()`~/\\-]+?" + "(?:{})".format(ext_list)
        return Regex(regexp_str, re.I)

    def _getRegexWithSpaces(self):
        ext_list = self._getImagesExtensions()
        regexp_str = r"[\w\s.=,#@^&$%;()`~/\\-]+?" + "(?:{})".format(ext_list)
        return Regex(regexp_str, re.I)

    def _convertToLink(self, s, l, t):
        fname = t[1]
        fname_fix_slash = fname.replace("\\", "/")
        src = "{dirname}/{fname}".format(dirname=PAGE_ATTACH_DIR, fname=fname_fix_slash)

        if Attachment(self.parser.page).exists(fname_fix_slash):
            return create_image(src, [css.CSS_IMAGE])

        return create_invalid_attached_file(fname)

    def _getTokenName(self):
        return "attachImage"
