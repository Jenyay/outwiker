# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption, StringOption, BooleanOption


class SessionInfo (object):
    """
    Информация о текущей сессии
    """
    def __init__ (self, path, pages, currentTab, readonly):
        """
        path - путь до открытой вики
        pages - список ссылок на страницы, открытые во вкладках. Элментами списка могут быть ссылки вида page://... или путь относительно корня вики
        currentTab - номер текущей открытой вкладки
        """
        self.path = path
        self.pages = pages
        self.currentTab = currentTab
        self.readonly = readonly


class SessionStorage (object):
    # Раздел секции в файле настроек, где хранятся сессии
    SECTION_NAME = u"Plugin_Sessions"

    # Параметр в файле настроек. Количество сессий
    SESSIONS_COUNT = u"SessionsCount"

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

    # Параметр в файле настроек. Открывать вики только для чтения?
    SESSION_READONLY = u"Readonly_{}"


    def __init__ (self, config):
        self._config = config

        # Словарь с сессиями. Ключ - имя сессии, значение - экземпляр класса SessionInfo
        self._sessions = self._loadAllSessions(self._config)


    def getSessions (self):
        return self._sessions


    def _loadAllSessions (self, config):
        """
        Загрузить список сессий из конфига
        """
        result = {}

        sessionsCount = IntegerOption (config, self.SECTION_NAME, self.SESSIONS_COUNT, 0).value
        for n in range (sessionsCount):
            self._loadSession (result, n)

        return result


    def _loadSession (self, sessions, nSession):
        """
        Прочитать сессию с номером nSession из конфига и добавить ее в словарь sessions. Ключ в словаре - имя сессии
        """
        # Прочитаем имя сессии
        name = StringOption (self._config,
                             self.SECTION_NAME,
                             self.SESSION_NAME.format (nSession),
                             u"").value
        if len (name) == 0:
            return

        # Прочитаем путь до вики
        path = StringOption (self._config,
                             self.SECTION_NAME,
                             self.SESSION_PATH.format (nSession),
                             u"").value

        if len (path) == 0:
            return

        links = []

        # Прочитаем количество вкладок
        tabsCount = IntegerOption (self._config,
                                   self.SECTION_NAME,
                                   self.TABS_COUNT.format (nSession),
                                   0).value


        # Прочитаем номер выбранной вкладки
        currentTab = IntegerOption (self._config,
                                    self.SECTION_NAME,
                                    self.CURRENT_TAB.format (nSession),
                                    0).value

        # Открывать вики в режиме "только для чтения"?
        readonly = BooleanOption (self._config,
                                  self.SECTION_NAME,
                                  self.SESSION_READONLY.format (nSession),
                                  False).value

        # Прочитаем список страниц
        for nPage in range (tabsCount):
            link = StringOption (self._config,
                                 self.SECTION_NAME,
                                 self.SESSION_TAB.format (nSession, nPage),
                                 u"").value

            if len (link) != 0:
                links.append (link)

        sessions[name] = SessionInfo (path, links, currentTab, readonly)


    def save (self, session, name):
        self._sessions[name] = session
        self._saveAllSessions()


    def _saveAllSessions (self):
        self._config.remove_section (self.SECTION_NAME)

        sessionNames = sorted (self._sessions.keys())

        # Сохраняем в конфиг количество сессий
        count = len (self._sessions)
        self._config.set (self.SECTION_NAME, self.SESSIONS_COUNT, count)

        for name, n in zip (sessionNames, range (count)):
            self._saveSession (name, n, self._sessions[name])


    def _saveSession (self, name, nSession, session):
        """
        Сохранить одну сессию в конфиг.
        name - имя сессии.
        nSession - порядковый номер сессии
        session - экземпляр класса SessionInfo
        """
        self._config.set (self.SECTION_NAME, self.SESSION_NAME.format(nSession), name)
        self._config.set (self.SECTION_NAME, self.SESSION_PATH.format(nSession), session.path)
        self._config.set (self.SECTION_NAME, self.TABS_COUNT.format(nSession), len (session.pages))
        self._config.set (self.SECTION_NAME, self.CURRENT_TAB.format(nSession), session.currentTab)

        for page, nPage in zip (session.pages, range (len (session.pages))):
            paramTabName = self.SESSION_TAB.format (nSession, nPage)
            self._config.set (self.SECTION_NAME, paramTabName, page)
