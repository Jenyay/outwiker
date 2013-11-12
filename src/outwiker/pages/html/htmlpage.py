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
from outwiker.pages.html.htmlpageview import HtmlPageView

from actions.headings import *
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
from actions.table import HtmlTableAction
from actions.tablerow import HtmlTableRowAction
from actions.tablecell import HtmlTableCellAction
from actions.listbullets import HtmlListBulletsAction
from actions.listnumbers import HtmlListNumbersAction
from actions.code import HtmlCodeAction
from actions.preformat import HtmlPreformatAction
from actions.quote import HtmlQuoteAction
from actions.image import HtmlImageAction
from actions.link import HtmlLinkAction
from actions.anchor import HtmlAnchorAction
from actions.horline import HtmlHorLineAction
from actions.escapehtml import HtmlEscapeHtmlAction

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
        (HtmlTableAction, HotKey ("Q", ctrl=True)),
        (HtmlTableRowAction, HotKey ("W", ctrl=True)),
        (HtmlTableCellAction, HotKey ("Y", ctrl=True)),
        (HtmlListBulletsAction, HotKey ("G", ctrl=True)),
        (HtmlListNumbersAction, HotKey ("J", ctrl=True)),
        (HtmlHeading1Action, HotKey ("1", ctrl=True)),
        (HtmlHeading2Action, HotKey ("2", ctrl=True)),
        (HtmlHeading3Action, HotKey ("3", ctrl=True)),
        (HtmlHeading4Action, HotKey ("4", ctrl=True)),
        (HtmlHeading5Action, HotKey ("5", ctrl=True)),
        (HtmlHeading6Action, HotKey ("6", ctrl=True)),
        (HtmlCodeAction, HotKey ("D", ctrl=True, alt=True)),
        (HtmlPreformatAction, HotKey ("F", ctrl=True, alt=True)),
        (HtmlQuoteAction, HotKey ("Q", ctrl=True, alt=True)),
        (HtmlImageAction, HotKey ("M", ctrl=True)),
        (HtmlLinkAction, HotKey ("L", ctrl=True)),
        (HtmlAnchorAction, HotKey ("N", ctrl=True, alt=True)),
        (HtmlHorLineAction, HotKey ("H", ctrl=True)),
        (HtmlEscapeHtmlAction, None),
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
        panel = HtmlPageView (parent)

        return panel


    @staticmethod
    def getPrefPanels (parent):
        return []
