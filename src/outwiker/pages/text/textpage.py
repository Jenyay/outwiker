# -*- coding: utf-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage
from outwiker.pages.text.textpanel import TextPanel


class TextWikiPage(WikiPage):
    """
    Класс текстовых страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        WikiPage.__init__(self, path, title, parent, readonly)

    @staticmethod
    def getTypeString():
        return "text"


class TextPageFactory(PageFactory):
    """
    Фабрика для создания текстовой страницы и ее представления
    """

    def getPageType(self):
        return TextWikiPage

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
