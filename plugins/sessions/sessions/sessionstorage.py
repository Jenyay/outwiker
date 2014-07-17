# -*- coding: UTF-8 -*-

import os.path


class SessionInfo (object):
    """
    Информация о текущей сессии
    """
    def __init__ (self, path, pages, currentTab):
        """
        path - путь до открытой вики
        pages - список страниц, открытых во вкладках
        currentTab - номер текущей открытой вкладки
        """
        self.path = path
        self.pages = pages
        self.currentTab = currentTab


class SessionStorage (object):
    # Раздел секции в файле настроек, где хранятся сессии
    SECTION_NAME = u"Plugin_Sessions"

    # Параметр в файле настроек. Количество сессий
    SESSIONS_COUNT = u"SessionsCount_{}"

    # Параметр в файле настроек. Имя сессии
    SESSION_NAME = u"SessionName_{}"

    # Параметр в файле настроек. Путь до файла с заметками
    SESSION_PATH = u"SessionPath_{}"

    # Параметр в файле настроек. Количество открытых вкладок
    TABS_COUNT = u"TabsCount_{}"

    # Параметр в файле настроек. Ссылка на страницу, открытую во вкладке
    SESSION_TAB = u"SessionTab_{}_{}"

    # Параметр в файле настроек. Текущая открытая вкладка
    CURRENT_TAB = u"CurrentTab_{}"


    def __init__ (self, application):
        self._application = application


    def getSessions (self):
        return []


    def save (self, name):
        assert self._application.mainWindow is not None

        config = self._application.config
        self._deleteSection (config)


    def getSessionInfo (self):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return SessionInfo (u"", [], 0)

        path = os.path.abspath (self._application.wikiroot.path)

        tabsController = self._application.mainWindow.tabsController

        pages = [tabsController.getPage (n)
                 for n in range (tabsController.getTabsCount())]

        currentTab = tabsController.getSelection()

        return SessionInfo (path, pages, currentTab)


    def _deleteSection (self, config):
        """
        Удалить секцию в окне параметров, чтобы начинать заполнять ее заново
        """
        config.remove_section (self.SECTION_NAME)
