#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import shutil

from .system import getTemplatesDir
from .htmltemplate import HtmlTemplate


class Style (object):
    def __init__ (self):
        self._styleFname = u"__style.html"
        self._styleDir = u"__style"

        self._defaultDir = u"__default"


    def getPageStyle (self, page):
        """
        Возвращает путь до файла стиля для страницы page
        """
        pageStylePath = os.path.join (page.path, self._styleFname)

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
        return os.path.join (getTemplatesDir(), self._defaultDir, self._styleFname)


    def setPageStyle (self, page, style):
        """
        Установить стиль для страницы
        style может быть путем до папки или до файла __style.html
        Может бросить исключение IOError
        """
        self.setPageStyleDefault (page)

        # Путь до стиля (папка)
        styledir = style if os.path.isdir (style) else os.path.dirname (style)

        # Пути до файла __style.html и до папки __style
        style_fname = os.path.join (styledir, self._styleFname)
        style_folder = os.path.join (styledir, self._styleDir)

        assert os.path.exists (style_fname)
        shutil.copy (style_fname, page.path)

        if os.path.exists (style_folder):
            shutil.copytree (style_folder, os.path.join (page.path, self._styleDir) )


    def setPageStyleDefault (self, page):
        """
        Удалить прикрепленный к странице стиль
        Может бросить исключение IOError
        """
        style_file = os.path.join (page.path, self._styleFname)
        style_dir = os.path.join (page.path, self._styleDir)

        if os.path.exists (style_file):
            os.remove (style_file)

        if os.path.exists (style_dir):
            shutil.rmtree (style_dir)

