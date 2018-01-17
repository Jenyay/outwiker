# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir


class SessionsTest(BaseMainWndTest):
    """Тесты плагина Sessions"""
    def setUp(self):
        super(SessionsTest, self).setUp()
        self.path2 = mkdtemp(prefix='Абырвалг абырвалг')

        self.__createWiki()

        dirlist = ["../plugins/sessions"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        from sessions.sessionstorage import SessionStorage
        Application.config.remove_section(SessionStorage.SECTION_NAME)

    def tearDown(self):
        from sessions.sessionstorage import SessionStorage
        Application.wikiroot = None
        Application.config.remove_section(SessionStorage.SECTION_NAME)
        self.loader.clear()
        removeDir(self.path2)
        super().tearDown()

    def __createWiki(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot["Страница 1"], "Страница 3", [])
        TextPageFactory().create(self.wikiroot["Страница 1/Страница 3"],
                                 "Страница 4", [])

    def __createWiki2(self):
        # Здесь будет создаваться вики
        wiki2 = WikiDocument.create(self.path2)
        TextPageFactory().create(wiki2, "Page 1", [])
        TextPageFactory().create(wiki2, "Page 2", [])

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testEmptySessions(self):
        from sessions.sessionstorage import SessionStorage
        storage = SessionStorage(Application.config)

        self.assertEqual(storage.getSessions(), {})

    def testSessionSingleTab(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        sessionName = "Имя сессии"

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), sessionName)
        sessions = storage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 1)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName].currentTab, 0)

    def testSaveSession_01(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        sessionName = "Имя сессии"

        controller = SessionController(Application)
        SessionStorage(Application.config).save(controller.getCurrentSession(),
                                                sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 1)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName].currentTab, 0)

    def testSaveSession_02(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Страница 1"]
        tabsController.openInTab(self.wikiroot["Страница 2"], False)

        sessionName = "Имя сессии"

        controller = SessionController(Application)
        SessionStorage(Application.config).save(controller.getCurrentSession(),
                                                sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 2)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName].pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(sessions[sessionName].currentTab, 0)

    def testSaveSession_03(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Страница 1"]
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        sessionName = "Имя сессии"

        controller = SessionController(Application)
        SessionStorage(Application.config).save(controller.getCurrentSession(),
                                                sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 2)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName].pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(sessions[sessionName].currentTab, 1)

    def testSaveSession_04(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        sessionName1 = "Имя сессии 1"
        sessionName2 = "Имя сессии 2"

        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)

        # Сохраним сессию с одной страницей
        SessionStorage(Application.config).save(controller.getCurrentSession(),
                                                sessionName1)

        # Сохраним сессию с двумя страницами
        tabsController.openInTab(self.wikiroot["Страница 2"], True)
        SessionStorage(Application.config).save(controller.getCurrentSession(),
                                                sessionName2)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 2)

        self.assertEqual(len(sessions[sessionName1].pages), 1)
        self.assertEqual(sessions[sessionName1].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName1].currentTab, 0)

        self.assertEqual(len(sessions[sessionName2].pages), 2)
        self.assertEqual(sessions[sessionName2].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName2].pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(sessions[sessionName2].currentTab, 1)

    def testSaveSession_05(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Страница 1"]
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        sessionName = "Имя сессии"
        controller = SessionController(Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        SessionStorage(Application.config).save(session, sessionName)
        SessionStorage(Application.config).save(session, sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 2)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions[sessionName].pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(sessions[sessionName].currentTab, 1)
        self.assertFalse(sessions[sessionName].readonly)

    def testSaveSession_06(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        tabsController = Application.mainWindow.tabsController

        uid1 = self._getPageLink(self.wikiroot["Страница 1"])
        uid2 = self._getPageLink(self.wikiroot["Страница 2"])

        wiki = WikiDocument.load(self.path, True)
        Application.wikiroot = wiki

        Application.selectedPage = wiki["Страница 1"]
        tabsController.openInTab(wiki["Страница 2"], True)

        sessionName = "Имя сессии"
        controller = SessionController(Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        SessionStorage(Application.config).save(session, sessionName)
        SessionStorage(Application.config).save(session, sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 2)
        self.assertEqual(sessions[sessionName].pages[0], uid1)
        self.assertEqual(sessions[sessionName].pages[1], uid2)
        self.assertEqual(sessions[sessionName].currentTab, 1)
        self.assertTrue(sessions[sessionName].readonly)

    def testSaveSession_07(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        tabsController = Application.mainWindow.tabsController

        # Создадим UID, а потом проверим, что они нормально прочитаются в
        # режиме только для чтения
        self._getPageLink(self.wikiroot["Страница 1"])
        self._getPageLink(self.wikiroot["Страница 2"])

        wiki = WikiDocument.load(self.path, True)
        Application.wikiroot = wiki

        Application.selectedPage = wiki["Страница 1"]
        tabsController.openInTab(wiki["Страница 2"], True)

        sessionName = "Имя сессии"
        controller = SessionController(Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        storage = SessionStorage(Application.config)

        storage.save(session, sessionName)
        storage.save(session, sessionName)

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 1)
        self.assertEqual(len(sessions[sessionName].pages), 2)
        self.assertEqual(sessions[sessionName].pages[0],
                         self._getPageLink(wiki["Страница 1"]))
        self.assertEqual(sessions[sessionName].pages[1],
                         self._getPageLink(wiki["Страница 2"]))
        self.assertEqual(sessions[sessionName].currentTab, 1)
        self.assertTrue(sessions[sessionName].readonly)

    def testSaveSession_08(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 2)

        self.assertEqual(len(sessions["session1"].pages), 1)
        self.assertEqual(sessions["session1"].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions["session1"].currentTab, 0)

        self.assertEqual(len(sessions["session2"].pages), 1)
        self.assertEqual(sessions["session2"].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions["session2"].currentTab, 0)

    def testSaveSession_09(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)
        storage.save(controller.getCurrentSession(), "session2")

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual(len(sessions), 2)

        self.assertEqual(len(sessions["session1"].pages), 1)
        self.assertEqual(sessions["session1"].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions["session1"].currentTab, 0)

        self.assertEqual(len(sessions["session2"].pages), 2)
        self.assertEqual(sessions["session2"].pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(sessions["session2"].pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(sessions["session2"].currentTab, 1)

    def testRemoveSession_01(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        otherStorage = SessionStorage(Application.config)
        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)

        # Удалим несуществующую сессию. При этом ничего не должно происходить
        storage.remove("session_invalid")

        otherStorage = SessionStorage(Application.config)
        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)

    def testRemoveSession_02(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        otherStorage = SessionStorage(Application.config)
        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)

        # Удалим несуществующую сессию. При этом ничего не должно происходить
        storage.remove("session1")

        otherStorage = SessionStorage(Application.config)
        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(list(sessions.keys())[0], "session2")

        sessions = storage.getSessions()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(list(sessions.keys())[0], "session2")

    def testRename_01(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        self.assertRaises(KeyError, storage.rename, "invalid", "Абырвалг")

    def testRename_02(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")
        storage.rename("session1", "Абырвалг")

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session2")
        self.assertEqual(sorted(sessions.keys())[1], "Абырвалг")

        sessions = storage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session2")
        self.assertEqual(sorted(sessions.keys())[1], "Абырвалг")

    def testRename_03(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")
        storage.rename("session1", "session1")

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session1")
        self.assertEqual(sorted(sessions.keys())[1], "session2")

        sessions = storage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session1")
        self.assertEqual(sorted(sessions.keys())[1], "session2")

    def testRename_04(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        self.assertRaises(ValueError, storage.rename, "session1", "session2")

    def testRename_05(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        self.assertRaises(ValueError,
                          storage.rename,
                          "session1", "session2   ")

    def testRename_06(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        self.assertRaises(ValueError, storage.rename, "session1", "")

    def testRename_07(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")

        self.assertRaises(ValueError, storage.rename, "session1", "   ")

    def testRename_08(self):
        from sessions.sessionstorage import SessionStorage
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)
        storage = SessionStorage(Application.config)

        storage.save(controller.getCurrentSession(), "session1")
        storage.save(controller.getCurrentSession(), "session2")
        storage.rename("session1", "Абырвалг   ")

        otherStorage = SessionStorage(Application.config)

        sessions = otherStorage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session2")
        self.assertEqual(sorted(sessions.keys())[1], "Абырвалг")

        sessions = storage.getSessions()
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sorted(sessions.keys())[0], "session2")
        self.assertEqual(sorted(sessions.keys())[1], "Абырвалг")

    def testGetSessionInfo_01(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        controller = SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual(session.path, os.path.abspath(self.wikiroot.path))
        self.assertEqual(len(session.pages), 1)
        self.assertEqual(session.pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(session.currentTab, 0)

    def testGetSessionInfo_02(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], False)

        controller = SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual(session.path, os.path.abspath(self.wikiroot.path))
        self.assertEqual(len(session.pages), 2)
        self.assertEqual(session.pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(session.pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(session.currentTab, 0)

    def testGetSessionInfo_03(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        controller = SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual(session.path, os.path.abspath(self.wikiroot.path))
        self.assertEqual(len(session.pages), 2)
        self.assertEqual(session.pages[0],
                         self._getPageLink(self.wikiroot["Страница 1"]))
        self.assertEqual(session.pages[1],
                         self._getPageLink(self.wikiroot["Страница 2"]))
        self.assertEqual(session.currentTab, 1)

    def testGetSessionInfo_04(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot["Страница 2"].readonly = True

        controller = SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual(session.path, os.path.abspath(self.wikiroot.path))
        self.assertEqual(len(session.pages), 2)
        self.assertEqual(session.pages[0], self.wikiroot["Страница 1"].subpath)
        self.assertEqual(session.pages[1], self.wikiroot["Страница 2"].subpath)
        self.assertEqual(session.currentTab, 1)

    def testInvalidSession_01(self):
        """
        Если нет открытых вики
        """
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = None
        controller = SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual(session.path, "")
        self.assertEqual(len(session.pages), 0)
        self.assertEqual(session.currentTab, 0)

    def testRestore_01(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink(self.wikiroot["Страница 1"])
        uid2 = self._getPageLink(self.wikiroot["Страница 2"])

        Application.wikiroot = None
        self.assertEqual(tabsController.getTabsCount(), 0)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 2)
        self.assertEqual(tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual(newsession.pages[0], uid1)
        self.assertEqual(newsession.pages[1], uid2)

    def testRestore_02(self):
        from sessions.sessioncontroller import SessionController

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)
        tabsController.openInTab(self.wikiroot["Страница 1/Страница 3/Страница 4"], True)
        tabsController.openInTab(self.wikiroot["Страница 1/Страница 3"], False)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink(self.wikiroot["Страница 1"])
        uid2 = self._getPageLink(self.wikiroot["Страница 2"])
        uid3 = self._getPageLink(self.wikiroot["Страница 1/Страница 3/Страница 4"])
        uid4 = self._getPageLink(self.wikiroot["Страница 1/Страница 3"])

        Application.wikiroot = None
        self.assertEqual(tabsController.getTabsCount(), 0)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 4)
        self.assertEqual(tabsController.getSelection(), 2)

        newsession = controller.getCurrentSession()
        self.assertEqual(newsession.pages[0], uid1)
        self.assertEqual(newsession.pages[1], uid2)
        self.assertEqual(newsession.pages[2], uid3)
        self.assertEqual(newsession.pages[3], uid4)

        self.assertEqual(tabsController.getPage(0).title, "Страница 1")
        self.assertEqual(tabsController.getPage(1).title, "Страница 2")
        self.assertEqual(tabsController.getPage(2).title, "Страница 4")
        self.assertEqual(tabsController.getPage(3).title, "Страница 3")

    def testRestore_03(self):
        from sessions.sessioncontroller import SessionController

        wiki = WikiDocument.load(self.path, readonly=False)
        Application.wikiroot = wiki
        Application.selectedPage = wiki["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(wiki["Страница 2"], True)
        tabsController.openInTab(wiki["Страница 1/Страница 3/Страница 4"],
                                 True)
        tabsController.openInTab(wiki["Страница 1/Страница 3"], False)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        tabsController.closeTab(1)
        tabsController.closeTab(1)
        tabsController.closeTab(1)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertFalse(Application.wikiroot.readonly)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 4)
        self.assertEqual(tabsController.getSelection(), 2)

        self.assertEqual(tabsController.getPage(0).title, "Страница 1")
        self.assertEqual(tabsController.getPage(1).title, "Страница 2")
        self.assertEqual(tabsController.getPage(2).title, "Страница 4")
        self.assertEqual(tabsController.getPage(3).title, "Страница 3")

    def testRestore_04(self):
        from sessions.sessioncontroller import SessionController

        self.__createWiki2()
        wiki2 = WikiDocument.load(self.path2, False)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink(self.wikiroot["Страница 1"])
        uid2 = self._getPageLink(self.wikiroot["Страница 2"])

        Application.wikiroot = wiki2
        self.assertEqual(tabsController.getTabsCount(), 1)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 2)
        self.assertEqual(tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual(newsession.pages[0], uid1)
        self.assertEqual(newsession.pages[1], uid2)

    def testRestore_05(self):
        from sessions.sessioncontroller import SessionController

        self.__createWiki2()
        wiki2 = WikiDocument.load(self.path2, True)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(self.wikiroot["Страница 2"], True)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink(self.wikiroot["Страница 1"])
        uid2 = self._getPageLink(self.wikiroot["Страница 2"])

        Application.wikiroot = wiki2
        self.assertEqual(tabsController.getTabsCount(), 1)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 2)
        self.assertEqual(tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual(newsession.pages[0], uid1)
        self.assertEqual(newsession.pages[1], uid2)

    def testRestoreReadonly_01(self):
        from sessions.sessioncontroller import SessionController

        wiki = WikiDocument.load(self.path, readonly=True)
        Application.wikiroot = wiki
        Application.selectedPage = wiki["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(wiki["Страница 2"], True)
        tabsController.openInTab(wiki["Страница 1/Страница 3/Страница 4"],
                                 True)
        tabsController.openInTab(wiki["Страница 1/Страница 3"], False)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        Application.wikiroot = None
        self.assertEqual(tabsController.getTabsCount(), 0)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertTrue(Application.wikiroot.readonly)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 4)
        self.assertEqual(tabsController.getSelection(), 2)

        self.assertEqual(tabsController.getPage(0).title, "Страница 1")
        self.assertEqual(tabsController.getPage(1).title, "Страница 2")
        self.assertEqual(tabsController.getPage(2).title, "Страница 4")
        self.assertEqual(tabsController.getPage(3).title, "Страница 3")

    def testRestoreReadonly_02(self):
        from sessions.sessioncontroller import SessionController

        wiki = WikiDocument.load(self.path, readonly=True)
        Application.wikiroot = wiki
        Application.selectedPage = wiki["Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab(wiki["Страница 2"], True)
        tabsController.openInTab(wiki["Страница 1/Страница 3/Страница 4"],
                                 True)
        tabsController.openInTab(wiki["Страница 1/Страница 3"], False)

        controller = SessionController(Application)
        session = controller.getCurrentSession()

        tabsController.closeTab(1)
        tabsController.closeTab(1)
        tabsController.closeTab(1)

        controller.restore(session)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertTrue(Application.wikiroot.readonly)

        self.assertEqual(os.path.abspath(Application.wikiroot.path),
                         os.path.abspath(self.path))
        self.assertEqual(tabsController.getTabsCount(), 4)
        self.assertEqual(tabsController.getSelection(), 2)

        self.assertEqual(tabsController.getPage(0).title, "Страница 1")
        self.assertEqual(tabsController.getPage(1).title, "Страница 2")
        self.assertEqual(tabsController.getPage(2).title, "Страница 4")
        self.assertEqual(tabsController.getPage(3).title, "Страница 3")

    def _getPageLink(self, page):
        return "page://" + Application.pageUidDepot.createUid(page)
