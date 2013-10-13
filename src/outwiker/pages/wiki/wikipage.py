#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.tree import WikiPage
from wikipanel import WikiPagePanel
from wikipreferences import WikiPrefGeneralPanel
from outwiker.core.factory import PageFactory
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.gui.hotkey import HotKey

from actions.bold import WikiBoldAction
from actions.italic import WikiItalicAction
from actions.bolditalic import WikiBoldItalicAction
from actions.underline import WikiUnderlineAction
from actions.strike import WikiStrikeAction
from actions.subscript import WikiSubscriptAction
from actions.superscript import WikiSuperscriptAction
from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.monospace import WikiMonospaceAction


class WikiWikiPage (WikiPage):
    """
    Класс wiki-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)
    

    @staticmethod
    def getTypeString ():
        return u"wiki"


class WikiPageFactory (PageFactory):
    @staticmethod
    def getPageType():
        return WikiWikiPage

    # Обрабатываемый этой фабрикой тип страниц (имеется в виду тип, описываемый строкой)
    @staticmethod
    def getTypeString ():
        return WikiPageFactory.getPageType().getTypeString()

    # Название страницы, показываемое пользователю
    title = _(u"Wiki Page")


    def __init__ (self):
        pass


    @staticmethod
    def create (parent, title, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        return PageFactory.createPage (WikiPageFactory.getPageType(), parent, title, tags)


    @staticmethod
    def getPageView (parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        panel = WikiPagePanel (parent)

        return panel


    @staticmethod
    def getPrefPanels (parent):
        """
        Получить список панелей для окна настроек
        Возвращает список кортежей ("название", Панель)
        """
        generalPanel = WikiPrefGeneralPanel (parent)

        return [ PreferencePanelInfo (generalPanel, _(u"General") ) ]


    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        application.actionController.register (WikiBoldAction (application), 
                HotKey ("B", ctrl=True))
        application.actionController.register (WikiItalicAction (application), 
                HotKey ("I", ctrl=True))
        application.actionController.register (WikiBoldItalicAction (application), 
                HotKey ("I", ctrl=True, shift=True))
        application.actionController.register (WikiUnderlineAction (application), 
                HotKey ("U", ctrl=True))
        application.actionController.register (WikiStrikeAction (application), 
                HotKey ("K", ctrl=True))
        application.actionController.register (WikiSubscriptAction (application), 
                HotKey ("=", ctrl=True))
        application.actionController.register (WikiSuperscriptAction (application), 
                HotKey ("+", ctrl=True))
        application.actionController.register (WikiFontSizeBigAction (application), 
                HotKey (".", ctrl=True))
        application.actionController.register (WikiFontSizeSmallAction (application), 
                HotKey (",", ctrl=True))
        application.actionController.register (WikiMonospaceAction (application), 
                HotKey ("7", ctrl=True))


    @staticmethod
    def removeActions (application):
        application.actionController.removeAction (WikiBoldAction.stringId)
        application.actionController.removeAction (WikiItalicAction.stringId)
        application.actionController.removeAction (WikiBoldItalicAction.stringId)
        application.actionController.removeAction (WikiUnderlineAction.stringId)
        application.actionController.removeAction (WikiStrikeAction.stringId)
        application.actionController.removeAction (WikiSubscriptAction.stringId)
        application.actionController.removeAction (WikiSuperscriptAction.stringId)
        application.actionController.removeAction (WikiFontSizeBigAction.stringId)
        application.actionController.removeAction (WikiFontSizeSmallAction.stringId)
        application.actionController.removeAction (WikiMonospaceAction.stringId)
