# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.exceptions import ReadonlyException

from .sessionstorage import SessionInfo


class SessionController (object):
    """
    Класс для получения текущей сессии и восстановления сессий
    """
    def __init__ (self, application):
        self._application = application
        self._protocol = u"page://"


    def _getPageLink (self, page):
        """
        Функция возвращает ссылку на страницу. Если страница открыта в режиме только для чтения и не содержит UID, то функция возвращает ссылку в старом стиле в виде пути. Если страница уже имеет UID или открыта в обычном режиме, возвращается ссылка вида page://...
        """
        try:
            link = self._protocol + self._application.pageUidDepot.createUid (page)
        except ReadonlyException:
            link = page.subpath

        return link


    def getCurrentSession (self):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return SessionInfo (u"", [], 0)

        path = os.path.abspath (self._application.wikiroot.path)

        tabsController = self._application.mainWindow.tabsController

        pages = [self._getPageLink (tabsController.getPage (n))
                 for n in range (tabsController.getTabsCount())]

        currentTab = tabsController.getSelection()

        return SessionInfo (path, pages, currentTab)
