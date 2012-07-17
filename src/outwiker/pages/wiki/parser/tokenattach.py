#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
from abc import ABCMeta, abstractmethod

from outwiker.libs.pyparsing import replaceWith, Literal
from outwiker.core.attachment import Attachment

from utils import concatenate, isImage


class AttachFactory (object):
    @staticmethod
    def make (parser):
        return AttachAllToken (parser).getToken()


class AttachImagesFactory (object):
    @staticmethod
    def make (parser):
        return AttachImagesToken (parser).getToken()


class AttachToken (object):
    __metaclass__ = ABCMeta
    attachString = u"Attach:"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        """
        Создать элементы из прикрепленных файлов.
        Отдельно картинки, отдельно все файлы
        """
        attachesAll = []

        attaches = Attachment (self.parser.page).attachmentFull
        attaches.sort (self.sortByLength, reverse=True)

        for attach in attaches:
            fname = os.path.basename (attach)
            if self.filterFile (fname):
                attach = Literal (fname)
                attachesAll.append (attach)

        finalToken = Literal (self.attachString) + concatenate (attachesAll)
        finalToken.setParseAction (self.convertToLink)
        return finalToken


    def convertToLink (self, s, l, t):
        fname = t[1]

        if isImage (fname):
            return '<IMG SRC="%s/%s"/>' % (Attachment.attachDir, fname)
        else:
            return '<A HREF="%s/%s">%s</A>' % (Attachment.attachDir, fname, fname)
    

    # TODO: Вынести в отдельный модуль
    def sortByLength (self, fname1, fname2):
        """
        Функция для сортировки имен по длине имени
        """
        if len (fname1) > len (fname2):
            return 1
        elif len (fname1) < len (fname2):
            return -1

        return 0


    @abstractmethod
    def filterFile (self, fname):
        """
        Должен возвращать True, если файл подходит для токена и False в противном случае
        """


class AttachAllToken (AttachToken):
    def filterFile (self, fname):
        return True


class AttachImagesToken (AttachToken):
    def filterFile (self, fname):
        return isImage (fname)
