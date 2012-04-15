#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path

from .system import getTemplatesDir
from .htmltemplate import HtmlTemplate


class Style (object):
    def __init__ (self):
        self._templateFname = u"__style.html"
        self._defaultFolder = u"__default"


    def getPageStyle (self, page):
        """
        Возвращает путь до файла стиля для страницы page
        """
        pageStylePath = os.path.join (page.path, self._templateFname)

        if (os.path.exists (pageStylePath) and
                os.path.isfile (pageStylePath)):
            style = pageStylePath
        else:
            style = self.getDefaultStyle()

        return style


    def getDefaultStyle (self):
        """
        Возвращает путь до стиля по умолчанию
        """
        return os.path.join (getTemplatesDir(), self._defaultFolder, self._templateFname)
