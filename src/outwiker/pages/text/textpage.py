# -*- coding: utf-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage
from outwiker.pages.text.defines import PAGE_TYPE_STRING
from outwiker.pages.text.textpanel import TextPanel


class TextWikiPage(WikiPage):
    """
    Класс текстовых страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        super().__init__(path, title, parent, readonly)

    def getTypeString(self):
        return PAGE_TYPE_STRING


class TextPageFactory(PageFactory):
    """
    Фабрика для создания текстовой страницы и ее представления
    """

    def getPageTypeString(self):
        return PAGE_TYPE_STRING

    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return _("Text Page")

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TextPanel(parent, application)

    def createPage(self, parent, title, path, readonly=False):
        return TextWikiPage(path, title, parent, readonly)
