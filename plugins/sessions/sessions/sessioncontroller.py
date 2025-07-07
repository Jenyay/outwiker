# -*- coding: utf-8 -*-

import os.path

from outwiker.api.app.tree import openWiki
from outwiker.api.core.tree import closeWiki
from outwiker.api.core.exceptions import ReadonlyException

from .sessionstorage import SessionInfo


class SessionController:
    """
    Класс для получения текущей сессии и восстановления сессий
    """

    def __init__(self, application):
        self._application = application
        self._protocol = "page://"

    def _getPageLink(self, page) -> str:
        """
        Функция возвращает ссылку на страницу.
        Если страница открыта в режиме только для чтения и не содержит UID, то функция возвращает ссылку в старом стиле в виде пути.
        Если страница уже имеет UID или открыта в обычном режиме, возвращается ссылка вида page://...
        """
        if page is None:
            return ''

        try:
            link = self._protocol + \
                self._application.pageUidDepot.createUid(page)
        except ReadonlyException:
            link = page.subpath

        return link

    def getCurrentSession(self):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return SessionInfo('', [], 0, True)

        path = os.path.abspath(self._application.wikiroot.path)

        tabsController = self._application.mainWindow.tabsController

        pages = [self._getPageLink(tabsController.getPage(n))
                 for n in range(tabsController.getTabsCount())]

        currentTab = tabsController.getSelection()

        return SessionInfo(path, pages, currentTab,
                           self._application.wikiroot.readonly)

    def restore(self, session):
        """
        Восстановить состояние по сессии
        """
        # Закрыть вики
        if (self._application.wikiroot is not None and
                os.path.abspath(self._application.wikiroot.path) != os.path.abspath(session.path)):
            closeWiki(self._application)

        # Открыть новую вики
        wiki = openWiki(os.path.abspath(session.path), self._application, session.readonly)
        if wiki is None:
            return

        self._application.wikiroot = wiki

        # Закрыть все вкладки
        tabsController = self._application.mainWindow.tabsController
        for n in range(tabsController.getTabsCount() - 1):
            tabsController.closeTab(1)

        # Открыть новые вкладки
        self._application.selectedPage = self._getPage(session.pages[0])

        for n in range(1, len(session.pages)):
            tabsController.openInTab(self._getPage(session.pages[-n]), False)

        # Выбрать нужную вкладку
        tabsController.setSelection(session.currentTab)

    def _getPage(self, link):
        """
        Возвращает страницу по ссылке.
        link - ссылка вида page://... или в виде относительного пути
        """
        if link is None:
            return None

        if link.startswith(self._protocol):
            uid = link[len(self._protocol):]
            return self._application.pageUidDepot[uid]

        return self._application.wikiroot[link]
