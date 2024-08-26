# -*- coding: utf-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage
from outwiker.gui.hotkey import HotKey
from outwiker.gui.actioninfo import ActionInfo

from .actions.attachlist import WikiAttachListAction
from .actions.childlist import WikiChildListAction
from .actions.dates import WikiDateCreationAction, WikiDateEditionAction
from .actions.fontsizebig import WikiFontSizeBigAction
from .actions.fontsizesmall import WikiFontSizeSmallAction
from .actions.include import WikiIncludeAction
from .actions.multilineblock import MultilineBlockAction
from .actions.nonparsed import WikiNonParsedAction
from .actions.openhtmlcode import WikiOpenHtmlCodeAction
from .actions.thumb import WikiThumbAction
from .actions.updatehtml import WikiUpdateHtmlAction
from .actions.wikistyle import WikiStyleAdvancedAction, WikiStyleOnlyAction
from .actions.listitemstyle import ListItemStyleAction
from .wikipageview import WikiPageView

from .defines import PAGE_TYPE_STRING


wiki_actions = [
    ActionInfo(WikiFontSizeBigAction, HotKey(".", ctrl=True)),
    ActionInfo(WikiFontSizeSmallAction, HotKey(",", ctrl=True)),
    ActionInfo(WikiNonParsedAction, None),
    ActionInfo(WikiThumbAction, HotKey("M", ctrl=True)),
    ActionInfo(WikiOpenHtmlCodeAction, HotKey("F4", shift=True)),
    ActionInfo(WikiUpdateHtmlAction, HotKey("F4", ctrl=True)),
    ActionInfo(WikiAttachListAction, None),
    ActionInfo(WikiChildListAction, None),
    ActionInfo(WikiIncludeAction, None),
    ActionInfo(WikiDateCreationAction, None),
    ActionInfo(WikiDateEditionAction, None),
    ActionInfo(WikiStyleOnlyAction, None),
    ActionInfo(WikiStyleAdvancedAction, None),
    ActionInfo(MultilineBlockAction, None),
    ActionInfo(ListItemStyleAction, None),
]


class WikiWikiPage(WikiPage):
    """
    Класс wiki-страниц
    """

    def __init__(self, path, title, parent, readonly=False):
        super().__init__(path, title, parent, readonly)

    @staticmethod
    def getTypeString():
        return PAGE_TYPE_STRING


class WikiPageFactory(PageFactory):
    """
    Фабрика для создания викистраниц и их представлений
    """

    def getPageType(self):
        return WikiWikiPage

    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return _("Wiki Page")

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return WikiPageView(parent, application)

    @staticmethod
    def registerActions(application):
        """
        Зарегистрировать все действия, связанные с викистраницей
        """
        [application.actionController.register(actionTuple.action_type(application), actionTuple.hotkey)
         for actionTuple in wiki_actions]

    @staticmethod
    def removeActions(application):
        [application.actionController.removeAction(actionTuple.action_type.stringId)
         for actionTuple in wiki_actions]
