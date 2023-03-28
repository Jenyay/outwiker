# -*- coding: utf-8 -*-

import os

from outwiker.api.core.defines import PAGE_RESULT_HTML
from outwiker.api.core.tree import WikiPage, PageFactory

from .markdownpageview import MarkdownPageView
from .i18n import get_


class MarkdownPage(WikiPage):
    """
    Класс тестовых страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        super(MarkdownPage, self).__init__(path, title, parent, readonly)

    @staticmethod
    def getTypeString():
        return "markdown"

    def getHtmlPath(self):
        """
        Получить путь до результирующего файла HTML
        """
        return os.path.join(self.path, PAGE_RESULT_HTML)


class MarkdownPageFactory(PageFactory):
    def getPageType(self):
        return MarkdownPage

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
