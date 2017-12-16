# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import re


class PageTitleError(BaseException):
    """
    Исключение, которое бросается, если заголовок не может быть
    использован во всех ОС
    """
    def __init__(self, message):
        BaseException.__init__(self, message)


class PageTitleWarning(BaseException):
    """
    Исключение, которое бросается, если заголовок не может быть использован в
    некоторых ОС (читай, под Windows)
    """
    def __init__(self, message):
        BaseException.__init__(self, message)


class PageTitleTester(object, metaclass=ABCMeta):
    """
    Класс для проверки правильности заголовка страницы
    """

    def test(self, title):
        """
        Проверить правильность заголовка
        Если есть ошибки или предупреждения, бросаются исключения
        PageTitleError или PageTitleWarning соответственно
        """
        self._testCommonErrors(title)
        self._testForError(title)

        self._testCommonWarnings(title)
        self._testForWarning(title)

    @staticmethod
    def _testCommonWarnings(title):
        """
        Проверка на предупреждения, общие для всех систем
        """
        # Проверка, содержит ли имя выражение виде %xx, где x - 16-ричное число
        regex = "%[0-9a-fA-F]{2}"
        if re.search(regex, title, flags=re.IGNORECASE) is not None:
            raise PageTitleWarning(_(u'The page title contains the expression "%xx". Links on this page may be invalid.'))

    def _testCommonErrors(self, title):
        """
        Проверка на ошибки, общие для всех систем
        """
        striptitle = title.strip()

        if len(striptitle) == 0:
            raise PageTitleError(_(u"The page title is empty"))

        if striptitle == u".":
            raise PageTitleError(_(u"Invalid the page title"))

        if striptitle.startswith(u"__"):
            raise PageTitleError(_(u"The page title can not begin with __"))

        invalidCharacters = '\\/\0'

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleError(_(u"The page title contains invalid characters"))

    @staticmethod
    def _testForInvalidChar(title, invalidCharacters):
        """
        Возвращает True, если в заголовке title есть заперещенные символы из
        строки invalidCharacters
        """
        return len([char for char in invalidCharacters if char in title]) == 0

    @abstractmethod
    def _testForError(self, title):
        """
        Если есть ошибки в будущем заголовке страницы, то бросается
        исключение PageTitleError
        """
        pass

    @abstractmethod
    def _testForWarning(self, title):
        """
        Если есть ошибки в будущем заголовке страницы, то бросается
        исключение PageTitleWarning
        """
        pass

    def replaceDangerousSymbols(self, title, replace):
        """Replace dangerous symbols by 'replace'"""
        regexp = re.compile(r'[><|?*:"\\/]|(%[0-9a-fA-F]{2})', re.U)
        return regexp.sub(replace, title)


class WindowsPageTitleTester(PageTitleTester):
    """
    Проверка имени страницы для Windows
    """
    def _testForError(self, title):
        invalidCharacters = '><|?*:"\\'
        striptitle = title.strip()

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleError(_(u"The page title contains invalid characters"))

    def _testForWarning(self, title):
        pass


class LinuxPageTitleTester(PageTitleTester):
    """
    Проверка имени страницы для Linux
    """
    def _testForError(self, title):
        pass

    def _testForWarning(self, title):
        invalidCharacters = '><|?*:"'
        striptitle = title.strip()

        if not self._testForInvalidChar(striptitle, invalidCharacters):
            raise PageTitleWarning(
                _(u"The page title contains invalid characters for Microsoft Windows operating system"))
