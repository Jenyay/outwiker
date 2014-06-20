# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.tree import WikiPage
from wikipageview import WikiPageView
from wikipreferences import WikiPrefGeneralPanel
from outwiker.core.factory import PageFactory
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.gui.hotkey import HotKey

from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.nonparsed import WikiNonParsedAction
from actions.thumb import WikiThumbAction
from actions.equation import WikiEquationAction
from actions.openhtmlcode import WikiOpenHtmlCodeAction
from actions.updatehtml import WikiUpdateHtmlAction
from actions.attachlist import WikiAttachListAction
from actions.childlist import WikiChildListAction
from actions.include import WikiIncludeAction


_actions = [
    (WikiFontSizeBigAction, HotKey (".", ctrl=True)),
    (WikiFontSizeSmallAction, HotKey (",", ctrl=True)),
    (WikiNonParsedAction, None),
    (WikiThumbAction, HotKey ("M", ctrl=True)),
    (WikiEquationAction, HotKey ("Q", ctrl=True)),
    (WikiOpenHtmlCodeAction, HotKey ("F4", shift=True)),
    (WikiUpdateHtmlAction, HotKey ("F4", ctrl=True)),
    (WikiAttachListAction, None),
    (WikiChildListAction, None),
    (WikiIncludeAction, None),
]


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
    """
    Фабрика для создания викистраниц и их представлений
    """
    def getPageType(self):
        return WikiWikiPage


    @property
    def title (self, title):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Wiki Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return WikiPageView (parent)


    def getPrefPanels (self, parent):
        """
        Получить список панелей для окна настроек
        Возвращает список кортежей ("название", Панель)
        """
        generalPanel = WikiPrefGeneralPanel (parent)

        return [PreferencePanelInfo (generalPanel, _(u"General"))]


    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с викистраницей
        """
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application),
                                                                        actionTuple[1]),
             _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId),
             _actions)
