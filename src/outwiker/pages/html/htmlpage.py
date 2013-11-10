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
from actions.italic import HtmlItalicAction
from actions.underline import HtmlUnderlineAction
from actions.strike import HtmlStrikeAction
from actions.subscript import HtmlSubscriptAction
from actions.superscript import HtmlSuperscriptAction
from actions.alignleft import HtmlAlignLeftAction
from actions.aligncenter import HtmlAlignCenterAction
from actions.alignright import HtmlAlignRightAction
from actions.alignjustify import HtmlAlignJustifyAction

from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction

_actions = [
        (HtmlBoldAction, HotKey ("B", ctrl=True)),
        (HtmlItalicAction, HotKey ("I", ctrl=True)),
        (HtmlUnderlineAction, HotKey ("U", ctrl=True)),
        (HtmlStrikeAction, HotKey ("K", ctrl=True)),
        (HtmlSubscriptAction, HotKey ("=", ctrl=True)),
        (HtmlSuperscriptAction, HotKey ("+", ctrl=True)),
        (HtmlAlignLeftAction, HotKey ("L", ctrl=True, alt=True)),
        (HtmlAlignCenterAction, HotKey ("C", ctrl=True, alt=True)),
        (HtmlAlignRightAction, HotKey ("R", ctrl=True, alt=True)),
        (HtmlAlignJustifyAction, HotKey ("J", ctrl=True, alt=True)),
        (HtmlAutoLineWrap, None),
        (SwitchCodeResultAction, HotKey ("F4")),
        ]


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
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application), actionTuple[1] ), _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId), _actions)


    # Название страницы, показываемое пользователю
    title = _(u"HTML Page")


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
