# -*- coding: utf-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .testpageview import TestPageView
from .defines import PAGE_TYPE_STRING


class TestPage(WikiPage):
    """
    Класс тестовых страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        super().__init__(path, title, parent, readonly)
        self._typeString = PAGE_TYPE_STRING


class TestPageFactory(PageFactory):
    """
    Класс фабрики для тестирования.
    Эта фабрика используется для создания типа страниц "testedPage",
    которая на самом деле является той же текстовой страницей, что и TextWikiPage.
    """

    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return _("Test Page")

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TestPageView(parent, application)

    def getPageTypeString(self):
        return PAGE_TYPE_STRING

    def createPage(self, parent, title, path, readonly=False):
        return TestPage(path, title, parent, readonly)
