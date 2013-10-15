#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os.path

from outwiker.core.config import BooleanOption
from outwiker.core.tree import WikiPage
from outwiker.core.factory import PageFactory
from outwiker.gui.hotkey import HotKey
from outwiker.pages.html.htmlpanel import HtmlPagePanel

from actions.bold import HtmlBoldAction
from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction


class HtmlWikiPage (WikiPage):
    """
    Класс HTML-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)

        self.__autoLineWrapSection = u"General"
        self.__autoLineWrapParam = u"LineWrap"

    
    @property
    def autoLineWrap (self):
        """
        Добавлять ли теги <BR> и <P> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        return option.value


    @autoLineWrap.setter
    def autoLineWrap (self, value):
        """
        Добавлять ли теги <BR> и <P> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        option.value = value
        self.root.onPageUpdate (self)

    
    @staticmethod
    def getTypeString ():
        return u"html"


class HtmlPageFactory (PageFactory):
    @staticmethod
    def getPageType():
        return HtmlWikiPage


    @staticmethod
    def getTypeString ():
        return HtmlPageFactory.getPageType().getTypeString()


    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        application.actionController.register (HtmlBoldAction (application), 
                HotKey ("B", ctrl=True))
        application.actionController.register (HtmlAutoLineWrap (application))
        application.actionController.register (SwitchCodeResultAction (application),
                HotKey ("F4"))


    @staticmethod
    def removeActions (application):
        application.actionController.removeAction (HtmlBoldAction.stringId)
        application.actionController.removeAction (HtmlAutoLineWrap.stringId)
        application.actionController.removeAction (SwitchCodeResultAction.stringId)


    # Название страницы, показываемое пользователю
    title = _(u"HTML Page")

    def __init__ (self):
        pass


    @staticmethod
    def create (parent, title, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        return PageFactory.createPage (HtmlPageFactory.getPageType(), parent, title, tags)


    @staticmethod
    def getPageView (parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        panel = HtmlPagePanel (parent)

        return panel


    @staticmethod
    def getPrefPanels (parent):
        return []
