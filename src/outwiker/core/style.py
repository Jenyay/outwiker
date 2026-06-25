# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from .exceptions import ReadonlyException
from .system import getTemplatesDir
from . import events


def getPageStyle(page) -> str:
    return Style().getPageStyle(page)


class Style:
    """
    Class for working with page styles
    """

    def __init__(self):
        self._styleFname = "__style.html"
        self._styleDir = "__style"

        self._defaultDir = "__default"

    def getPageStyle(self, page) -> str:
        """
        Returns the path to the style file for page page
        """
        if self.check(page.path):
            style = os.path.join(page.path, self._styleFname)
        else:
            style = self.getDefaultStyle()

        return style

    def getDefaultStyle(self) -> str:
        """
        Returns the path to the default style
        """
        return os.path.join(getTemplatesDir(), self._defaultDir, self._styleFname)

    def setPageStyle(self, page, style: str) -> None:
        """
        Set style for page
        style can be a path to a folder or to the __style.html file
        Can raise IOError exception
        """
        if page is None:
            return

        if page.readonly:
            raise ReadonlyException

        # Path to style (folder)
        styledir = style if os.path.isdir(style) else os.path.dirname(style)

        # Paths to __style.html file and __style folder
        style_fname = os.path.join(styledir, self._styleFname)
        style_folder = os.path.join(styledir, self._styleDir)

        if os.path.abspath(style_fname) == os.path.abspath(self.getPageStyle(page)):
            return

        if os.path.abspath(style_fname) == os.path.abspath(self.getDefaultStyle()):
            self.setPageStyleDefault(page)
            return

        self._removeStyleFromPage(page)
        shutil.copy(style_fname, page.path)

        if os.path.exists(style_folder):
            shutil.copytree(style_folder, os.path.join(page.path, self._styleDir))

        page.updateDateTime()
        page.root.onPageUpdate(page, change=events.PAGE_UPDATE_STYLE)

    def _removeStyleFromPage(self, page):
        """
        Remove style files from page
        Can raise IOError exception
        """
        assert not page.readonly

        style_file = os.path.join(page.path, self._styleFname)
        style_dir = os.path.join(page.path, self._styleDir)

        if os.path.exists(style_file):
            os.remove(style_file)

        if os.path.exists(style_dir):
            shutil.rmtree(style_dir)

    def setPageStyleDefault(self, page):
        """
        Remove attached style from page
        Can raise IOError exception
        """
        if page is None:
            return

        if page.readonly:
            raise ReadonlyException

        self._removeStyleFromPage(page)
        page.updateDateTime()
        page.root.onPageUpdate(page, change=events.PAGE_UPDATE_STYLE)

    def check(self, path: str):
        """
        Returns True if path is a path to a correct style
        """
        style_file = os.path.join(path, self._styleFname)
        file_correct = os.path.exists(style_file) and os.path.isfile(style_file)

        return file_correct
