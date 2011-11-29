#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod


class PageTitleTester (object):
    """
    Класс для проверки правильности заголовка страницы
    """

    @abstractmethod
    def testForError (self, title):
        """
        Должен возвращать None, если в будущем имени страницы нет ошибок (недопустимых символов и т.п.) В противном случае должен вернуть текст ошибки для отображения пользователю
        """
        pass


    @abstractmethod
    def testForWarning (self, title):
        """
        Должен возвращать None, если в будущем имени страницы нет подозрительных символов, которые могут вызвать проблемы. В противном случае должен вернуть текст предупреждения для отображения пользователю
        """
        pass


class WindowsPageTitleTester (PageTitleTester):
    """
    Проверка имени страницы для Windows
    """
    def testForError (self, title):
        pass


    def testForWarning (self, title):
        pass


class LinuxPageTitleTester (PageTitleTester):
    """
    Проверка имени страницы для Linux
    """
    def testForError (self, title):
        pass


    def testForWarning (self, title):
        pass
