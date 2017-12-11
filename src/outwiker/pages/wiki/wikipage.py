# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os

from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage
from outwiker.gui.hotkey import HotKey
from .wikipageview import WikiPageView

from .actions.fontsizebig import WikiFontSizeBigAction
from .actions.fontsizesmall import WikiFontSizeSmallAction
from .actions.nonparsed import WikiNonParsedAction
from .actions.thumb import WikiThumbAction
from .actions.openhtmlcode import WikiOpenHtmlCodeAction
from .actions.updatehtml import WikiUpdateHtmlAction
from .actions.attachlist import WikiAttachListAction
from .actions.childlist import WikiChildListAction
from .actions.include import WikiIncludeAction
from .actions.dates import WikiDateCreationAction, WikiDateEditionAction


wiki_actions = [
   (WikiFontSizeBigAction, HotKey(".", ctrl=True)),
   (WikiFontSizeSmallAction, HotKey(",", ctrl=True)),
   (WikiNonParsedAction, None),
   (WikiThumbAction, HotKey("M", ctrl=True)),
   (WikiOpenHtmlCodeAction, HotKey("F4", shift=True)),
   (WikiUpdateHtmlAction, HotKey("F4", ctrl=True)),
   (WikiAttachListAction, None),
   (WikiChildListAction, None),
   (WikiIncludeAction, None),
   (WikiDateCreationAction, None),
   (WikiDateEditionAction, None),
]


class WikiWikiPage(WikiPage):
    """
    Класс wiki-страниц
    """
    def __init__(self, path, title, parent, readonly=False):
        WikiPage.__init__(self, path, title, parent, readonly)

    @staticmethod
    def getTypeString():
        return u"wiki"

    def getHtmlPath(self):
        """
        Получить путь до результирующего файла HTML
        """
        return os.path.join(self.path, PAGE_RESULT_HTML)


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
        return _(u"Wiki Page")

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
        map(lambda actionTuple: application.actionController.register(actionTuple[0](application),
                                                                      actionTuple[1]),
            wiki_actions)

    @staticmethod
    def removeActions(application):
        map(lambda actionTuple: application.actionController.removeAction(actionTuple[0].stringId),
            wiki_actions)
