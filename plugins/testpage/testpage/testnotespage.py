# -*- coding: UTF-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .testpageview import TestPageView


class TestPage (WikiPage):
    """
    Класс тестовых страниц
    """
    def __init__(self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"testpage"


class TestPageFactory (PageFactory):
    """
    Класс фабрики для тестирования.
    Эта фабрика используется для создания типа страниц "testedPage", которая на самом деле является той же текстовой страницей, что и TextWikiPage.
    """
    def getPageType(self):
        return TestPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Test Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TestPageView (parent)
