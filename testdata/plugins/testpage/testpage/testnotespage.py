# -*- coding: utf-8 -*-

from outwiker.api.core.tree import PageAdapter, PageFactory

from .testpageview import TestPageView
from .defines import PAGE_TYPE_STRING


class TestPageAdapter(PageAdapter):
    pass


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

    def createPageAdapter(self, page):
        return TestPageAdapter(page)
