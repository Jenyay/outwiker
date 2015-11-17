# -*- coding: UTF-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .latexpageview import LatexPageView


class LatexPage (WikiPage):
    """
    Класс тестовых страниц
    """
    def __init__(self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"latexpage"


class LatexPageFactory (PageFactory):
    """
    Класс фабрики для тестирования.
    Эта фабрика используется для создания типа страниц "LatexPage", которая на самом деле является той же текстовой страницей, что и TextWikiPage.
    """
    def getPageType(self):
        return LatexPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"LaTeX Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return LatexPageView (parent)
