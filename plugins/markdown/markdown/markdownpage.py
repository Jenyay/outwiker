# -*- coding: utf-8 -*-

from outwiker.api.core.tree import WikiPage, PageFactory

from .defines import PAGE_TYPE_STRING
from .i18n import get_
from .markdownpageview import MarkdownPageView


class MarkdownPage(WikiPage):
    """
    Класс тестовых страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        super().__init__(path, title, parent, readonly)

    def getTypeString(self) -> str:
        return PAGE_TYPE_STRING


class MarkdownPageFactory(PageFactory):
    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        _ = get_()
        return _("Markdown Page")

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return MarkdownPageView(parent, application)

    def getPageTypeString(self):
        return PAGE_TYPE_STRING

    def createPage(self, parent, title, path, readonly=False):
        return MarkdownPage(path, title, parent, readonly)
