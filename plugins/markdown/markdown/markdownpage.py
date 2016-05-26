# -*- coding: UTF-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .markdownpageview import MarkdownPageView


class MarkdownPage (WikiPage):
    """
    Класс тестовых страниц
    """
    def __init__(self, path, title, parent, readonly = False):
        super(MarkdownPage, self).__init__ (path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"markdown"


class MarkdownPageFactory (PageFactory):
    def getPageType(self):
        return MarkdownPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Markdown Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return MarkdownPageView (parent)
