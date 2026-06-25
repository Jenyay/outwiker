# -*- coding: utf-8 -*-

import re
from abc import ABCMeta, abstractmethod


class PageTitleError(Exception):
    """Exception raised for title if it can't be used in all OS systems.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class PageTitleWarning(Exception):
    """Exception raised for title if it can't be used in Windows system.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class PageTitleTester(metaclass=ABCMeta):
    """Class for testing the correctness of the page title."""

    def test(self, title):
        """
        Test the correctness of the title.

        If there are errors or warnings, exceptions
        PageTitleError or PageTitleWarning are raised respectively.
        """
        self._testCommonErrors(title)
        self._testForError(title)

        self._testCommonWarnings(title)
        self._testForWarning(title)

    @staticmethod
    def _testCommonWarnings(title):
        """Test for warnings common to all systems."""
        # Check if the name contains an expression in the form %xx, where x is a hexadecimal number
        regex = "%[0-9a-fA-F]{2}"
        if re.search(regex, title, flags=re.IGNORECASE) is not None:
            raise PageTitleWarning(
                _(
                    'The page title contains the expression "%xx". Links on this page may be invalid.'
                )
            )

    def _testCommonErrors(self, title):
        """Test for errors common to all systems."""
        striptitle = title.strip()

        if len(striptitle) == 0:
            raise PageTitleError(_("The page title is empty"))

        if striptitle == ".":
            raise PageTitleError(_("Invalid the page title"))

        if striptitle.startswith("__"):
            raise PageTitleError(_("The page title can not begin with __"))

        invalidCharacters = "\\/\0"

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleError(_("The page title contains invalid characters"))

    @staticmethod
    def _testForInvalidChar(title, invalidCharacters):
        """
        Returns True if the title contains forbidden characters from
        the invalidCharacters string.
        """
        return len([char for char in invalidCharacters if char in title]) == 0

    @abstractmethod
    def _testForError(self, title):
        """
        If there are errors in the future page title, a
        PageTitleError exception is raised.
        """
        pass

    @abstractmethod
    def _testForWarning(self, title):
        """
        If there are warnings in the future page title, a
        PageTitleWarning exception is raised.
        """
        pass

    def replaceDangerousSymbols(self, title, replacement):
        """Replace dangerous symbols by 'replacement'"""
        regexp = re.compile(r'[><|?*:"\\/#]|(%[0-9a-fA-F]{2})')
        return regexp.sub(replacement, title)


class WindowsPageTitleTester(PageTitleTester):
    """Test page name for Windows."""

    def _testForError(self, title):
        invalidCharacters = '><|?*:"\\'
        striptitle = title.strip()

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleError(_("The page title contains invalid characters"))

    def _testForWarning(self, title):
        pass


class LinuxPageTitleTester(PageTitleTester):
    """Test page name for Linux."""

    def _testForError(self, title):
        pass

    def _testForWarning(self, title):
        invalidCharacters = '><|?*:"'
        striptitle = title.strip()

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleWarning(
                _(
                    "The page title contains invalid characters for Microsoft Windows operating system"
                )
            )
