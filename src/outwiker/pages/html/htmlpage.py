# -*- coding: utf-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.config import BooleanOption
from outwiker.core.events import PAGE_UPDATE_CONTENT
from outwiker.core.factory import PageFactory
from outwiker.core.tree import PageAdapter
from outwiker.gui.actioninfo import ActionInfo
from outwiker.gui.hotkey import HotKey
from outwiker.pages.html.defines import PAGE_TYPE_STRING
from outwiker.pages.html.htmlpageview import HtmlPageView

from .actions.autolinewrap import HtmlAutoLineWrap
from .actions.switchcoderesult import SwitchCodeResultAction

html_actions = [
    ActionInfo(HtmlAutoLineWrap, None),
    ActionInfo(SwitchCodeResultAction, HotKey("F4")),
]


class HtmlPageAdapter(PageAdapter):
    """
    Класс HTML-страниц
    """

    def __init__(self, page):
        super().__init__(page)
        self.__autoLineWrapSection = "General"
        self.__autoLineWrapParam = "LineWrap"

    @property
    def autoLineWrap(self):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption(
            self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True
        )
        return option.value

    @autoLineWrap.setter
    def autoLineWrap(self, value):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption(
            self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True
        )
        option.value = value
        self.root.onPageUpdate(self.page, change=PAGE_UPDATE_CONTENT)


class HtmlPageFactory(PageFactory):
    """
    Фабрика для создания HTML-страниц и их представлений
    """

    @staticmethod
    def registerActions(application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        [
            application.actionController.register(
                actionTuple.action_type(application), actionTuple.hotkey
            )
            for actionTuple in html_actions
        ]

    @staticmethod
    def removeActions(application):
        [
            application.actionController.removeAction(actionTuple.action_type.stringId)
            for actionTuple in html_actions
        ]

    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return _("HTML Page")

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return HtmlPageView(parent, application)

    def getPageTypeString(self):
        return PAGE_TYPE_STRING

    def createPageAdapter(self, page):
        return HtmlPageAdapter(page)
