# -*- coding: utf-8 -*-

from outwiker.api.core.tree import PageAdapter, PageFactory

from .defines import PAGE_TYPE_STRING
from .i18n import get_
from .markdownpageview import MarkdownPageView


class MarkdownPageAdapter(PageAdapter):
    pass


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

    def createPageAdapter(self, page):
        return MarkdownPageAdapter(page)
