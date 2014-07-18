# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption, StringOption


class SessionInfo (object):
    """
    Информация о текущей сессии
    """
    def __init__ (self, path, pages, currentTab):
        """
        path - путь до открытой вики
        pages - список ссылок на страницы, открытые во вкладках. Элментами списка могут быть ссылки вида page://... или путь относительно корня вики
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

        # Словарь с сессиями. Ключ - имя сессии, значение - экземпляр класса SessionInfo
        self._sessions = self._loadAllSessions(self._application.config)


    def getSessions (self):
        return self._sessions


    def _getConfig (self):
        return self._application.config


    def _loadAllSessions (self, config):
        """
        Загрузить список сессий из конфига
        """
        result = {}

        config = self._application.config

        sessionsCount = IntegerOption (config, self.SECTION_NAME, self.SESSIONS_COUNT, 0).value
        for n in range (sessionsCount):
            self._loadSession (result, n)

        return result


    def _loadSession (self, sessions, nSession):
        """
        Прочитать сессию с номером nSession из конфига и добавить ее в словарь sessions. Ключ в словаре - имя сессии
        """
        config = self._getConfig()

        # Прочитаем имя сессии
        name = StringOption (config,
                             self.SECTION_NAME,
                             self.SESSION_NAME.format (nSession),
                             u"").value
        if len (name) == 0:
            return

        # Прочитаем путь до вики
        path = StringOption (config,
                             self.SECTION_NAME,
                             self.SESSION_PATH.format (nSession),
                             u"").value

        if len (path) == 0:
            return

        links = []

        # Прочитаем количество вкладок
        tabsCount = IntegerOption (config,
                                   self.SECTION_NAME,
                                   self.TABS_COUNT.format (nSession),
                                   0).value


        # Прочитаем номер выбранной вкладки
        currentTab = IntegerOption (config,
                                    self.SECTION_NAME,
                                    self.CURRENT_TAB.format (nSession),
                                    0).value

        # Прочитаем список страниц
        for nPage in range (tabsCount):
            link = StringOption (config,
                                 self.SECTION_NAME,
                                 self.SESSION_TAB.format (nSession, nPage),
                                 u"").value

            if len (link) != 0:
                links.append (link)

        sessions[name] = SessionInfo (path, links, currentTab)


    def save (self, session, name):
        self._sessions[name] = session
        self._saveAllSessions()


    def _saveAllSessions (self):
        config = self._application.config
        config.remove_section (self.SECTION_NAME)

        sessionNames = sorted (self._sessions.keys())

        # Сохраняем в конфиг количество сессий
        count = len (self._sessions)
        config.set (self.SECTION_NAME, self.SESSIONS_COUNT, count)

        for name, n in zip (sessionNames, range (count)):
            self._saveSession (name, n, self._sessions[name])


    def _saveSession (self, name, nSession, session):
        """
        Сохранить одну сессию в конфиг.
        config - конфиг из Application.config, куда сохраняется сессия
        name - имя сессии.
        nSession - порядковый номер сессии
        session - экземпляр класса SessionInfo
        """
        config = self._application.config

        config.set (self.SECTION_NAME, self.SESSION_NAME.format(nSession), name)
        config.set (self.SECTION_NAME, self.SESSION_PATH.format(nSession), session.path)
        config.set (self.SECTION_NAME, self.TABS_COUNT.format(nSession), len (session.pages))
        config.set (self.SECTION_NAME, self.CURRENT_TAB.format(nSession), session.currentTab)

        for page, nPage in zip (session.pages, range (len (session.pages))):
            paramTabName = self.SESSION_TAB.format (nSession, nPage)
            config.set (self.SECTION_NAME, paramTabName, page)


    def _deleteSection (self, config):
        """
        Удалить секцию в окне параметров, чтобы начинать заполнять ее заново
        """
        config.remove_section (self.SECTION_NAME)
