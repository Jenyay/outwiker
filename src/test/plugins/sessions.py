# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class SessionsTest (BaseMainWndTest):
    """Тесты плагина Sessions"""
    def setUp (self):
        super (SessionsTest, self).setUp ()
        self.path = u"../test/testwiki"
        self.path2 = u"../test/testwiki2"

        self.__createWiki()

        dirlist = [u"../plugins/sessions"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        Application.config.remove_section (self.loader[u"Sessions"].SessionStorage.SECTION_NAME)


    def tearDown (self):
        super (SessionsTest, self).tearDown ()
        Application.wikiroot = None
        Application.config.remove_section (self.loader[u"Sessions"].SessionStorage.SECTION_NAME)
        self.loader.clear()
        removeWiki (self.path)
        removeWiki (self.path2)


    def __createWiki (self):
        # Здесь будет создаваться вики
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        TextPageFactory().create (self.wikiroot, u"Страница 1", [])
        TextPageFactory().create (self.wikiroot, u"Страница 2", [])
        TextPageFactory().create (self.wikiroot[u"Страница 1"], u"Страница 3", [])
        TextPageFactory().create (self.wikiroot[u"Страница 1/Страница 3"], u"Страница 4", [])


    def __createWiki2 (self):
        # Здесь будет создаваться вики
        removeWiki (self.path2)

        wiki2 = WikiDocument.create (self.path2)
        TextPageFactory().create (wiki2, u"Page 1", [])
        TextPageFactory().create (wiki2, u"Page 2", [])


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testEmptySessions (self):
        storage = self.loader[u"Sessions"].SessionStorage(Application.config)

        self.assertEqual (storage.getSessions(), {})


    def testSessionSingleTab (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        sessionName = u"Имя сессии"

        controller = self.loader[u"Sessions"].SessionController(Application)
        storage = self.loader[u"Sessions"].SessionStorage(Application.config)

        storage.save (controller.getCurrentSession(), sessionName)
        sessions = storage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 1)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].currentTab, 0)


    def testSaveSession_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        sessionName = u"Имя сессии"

        controller = self.loader[u"Sessions"].SessionController (Application)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (controller.getCurrentSession(), sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 1)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].currentTab, 0)


    def testSaveSession_02 (self):
        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Страница 1"]
        tabsController.openInTab (self.wikiroot[u"Страница 2"], False)

        sessionName = u"Имя сессии"

        controller = self.loader[u"Sessions"].SessionController (Application)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (controller.getCurrentSession(), sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 2)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (sessions[sessionName].currentTab, 0)


    def testSaveSession_03 (self):
        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Страница 1"]
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        sessionName = u"Имя сессии"

        controller = self.loader[u"Sessions"].SessionController (Application)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (controller.getCurrentSession(), sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 2)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (sessions[sessionName].currentTab, 1)


    def testSaveSession_04 (self):
        sessionName1 = u"Имя сессии 1"
        sessionName2 = u"Имя сессии 2"

        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Страница 1"]

        controller = self.loader[u"Sessions"].SessionController (Application)

        # Сохраним сессию с одной страницей
        self.loader[u"Sessions"].SessionStorage(Application.config).save (controller.getCurrentSession(), sessionName1)

        # Сохраним сессию с двумя страницами
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (controller.getCurrentSession(), sessionName2)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 2)

        self.assertEqual (len (sessions[sessionName1].pages), 1)
        self.assertEqual (sessions[sessionName1].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName1].currentTab, 0)

        self.assertEqual (len (sessions[sessionName2].pages), 2)
        self.assertEqual (sessions[sessionName2].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName2].pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (sessions[sessionName2].currentTab, 1)


    def testSaveSession_05 (self):
        tabsController = Application.mainWindow.tabsController
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Страница 1"]
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        sessionName = u"Имя сессии"
        controller = self.loader[u"Sessions"].SessionController (Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 2)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (sessions[sessionName].currentTab, 1)
        self.assertFalse (sessions[sessionName].readonly)


    def testSaveSession_06 (self):
        tabsController = Application.mainWindow.tabsController

        uid1 = self._getPageLink (self.wikiroot[u"Страница 1"])
        uid2 = self._getPageLink (self.wikiroot[u"Страница 2"])

        wiki = WikiDocument.load (self.path, True)
        Application.wikiroot = wiki

        Application.selectedPage = wiki[u"Страница 1"]
        tabsController.openInTab (wiki[u"Страница 2"], True)

        sessionName = u"Имя сессии"
        controller = self.loader[u"Sessions"].SessionController (Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 2)
        self.assertEqual (sessions[sessionName].pages[0], uid1)
        self.assertEqual (sessions[sessionName].pages[1], uid2)
        self.assertEqual (sessions[sessionName].currentTab, 1)
        self.assertTrue (sessions[sessionName].readonly)


    def testSaveSession_07 (self):
        tabsController = Application.mainWindow.tabsController

        # Создадим UID, а потом проверим, что они нормально прочитаются в
        # режиме только для чтения
        self._getPageLink (self.wikiroot[u"Страница 1"])
        self._getPageLink (self.wikiroot[u"Страница 2"])

        wiki = WikiDocument.load (self.path, True)
        Application.wikiroot = wiki

        Application.selectedPage = wiki[u"Страница 1"]
        tabsController.openInTab (wiki[u"Страница 2"], True)

        sessionName = u"Имя сессии"
        controller = self.loader[u"Sessions"].SessionController (Application)
        session = controller.getCurrentSession()

        # Сохраним сессию дважды под одним и тем же именем
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)
        self.loader[u"Sessions"].SessionStorage(Application.config).save (session, sessionName)

        otherStorage = self.loader[u"Sessions"].SessionStorage(Application.config)

        sessions = otherStorage.getSessions()

        self.assertEqual (len (sessions), 1)
        self.assertEqual (len (sessions[sessionName].pages), 2)
        self.assertEqual (sessions[sessionName].pages[0], self._getPageLink (wiki[u"Страница 1"]))
        self.assertEqual (sessions[sessionName].pages[1], self._getPageLink (wiki[u"Страница 2"]))
        self.assertEqual (sessions[sessionName].currentTab, 1)
        self.assertTrue (sessions[sessionName].readonly)


    def testGetSessionInfo_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        controller = self.loader[u"Sessions"].SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 1)
        self.assertEqual (session.pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (session.currentTab, 0)


    def testGetSessionInfo_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], False)

        controller = self.loader[u"Sessions"].SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 2)
        self.assertEqual (session.pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (session.pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (session.currentTab, 0)


    def testGetSessionInfo_03 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        controller = self.loader[u"Sessions"].SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 2)
        self.assertEqual (session.pages[0], self._getPageLink (self.wikiroot[u"Страница 1"]))
        self.assertEqual (session.pages[1], self._getPageLink (self.wikiroot[u"Страница 2"]))
        self.assertEqual (session.currentTab, 1)


    def testGetSessionInfo_04 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        self.wikiroot[u"Страница 1"].readonly = True
        self.wikiroot[u"Страница 2"].readonly = True

        controller = self.loader[u"Sessions"].SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual (session.path, os.path.abspath (self.wikiroot.path))
        self.assertEqual (len (session.pages), 2)
        self.assertEqual (session.pages[0], self.wikiroot[u"Страница 1"].subpath)
        self.assertEqual (session.pages[1], self.wikiroot[u"Страница 2"].subpath)
        self.assertEqual (session.currentTab, 1)


    def testInvalidSession_01 (self):
        """
        Если нет открытых вики
        """
        Application.wikiroot = None
        controller = self.loader[u"Sessions"].SessionController(Application)

        session = controller.getCurrentSession()

        self.assertEqual (session.path, u"")
        self.assertEqual (len (session.pages), 0)
        self.assertEqual (session.currentTab, 0)


    def testRestore_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink (self.wikiroot[u"Страница 1"])
        uid2 = self._getPageLink (self.wikiroot[u"Страница 2"])

        Application.wikiroot = None
        self.assertEqual (tabsController.getTabsCount(), 0)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 2)
        self.assertEqual (tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual (newsession.pages[0], uid1)
        self.assertEqual (newsession.pages[1], uid2)


    def testRestore_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)
        tabsController.openInTab (self.wikiroot[u"Страница 1/Страница 3/Страница 4"], True)
        tabsController.openInTab (self.wikiroot[u"Страница 1/Страница 3"], False)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink (self.wikiroot[u"Страница 1"])
        uid2 = self._getPageLink (self.wikiroot[u"Страница 2"])
        uid3 = self._getPageLink (self.wikiroot[u"Страница 1/Страница 3/Страница 4"])
        uid4 = self._getPageLink (self.wikiroot[u"Страница 1/Страница 3"])

        Application.wikiroot = None
        self.assertEqual (tabsController.getTabsCount(), 0)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 4)
        self.assertEqual (tabsController.getSelection(), 2)

        newsession = controller.getCurrentSession()
        self.assertEqual (newsession.pages[0], uid1)
        self.assertEqual (newsession.pages[1], uid2)
        self.assertEqual (newsession.pages[2], uid3)
        self.assertEqual (newsession.pages[3], uid4)

        self.assertEqual (tabsController.getPage (0).title, u"Страница 1")
        self.assertEqual (tabsController.getPage (1).title, u"Страница 2")
        self.assertEqual (tabsController.getPage (2).title, u"Страница 4")
        self.assertEqual (tabsController.getPage (3).title, u"Страница 3")


    def testRestore_03 (self):
        wiki = WikiDocument.load (self.path, readonly=False)
        Application.wikiroot = wiki
        Application.selectedPage = wiki[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (wiki[u"Страница 2"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3/Страница 4"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3"], False)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        tabsController.closeTab (1)
        tabsController.closeTab (1)
        tabsController.closeTab (1)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertFalse (Application.wikiroot.readonly)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 4)
        self.assertEqual (tabsController.getSelection(), 2)

        self.assertEqual (tabsController.getPage (0).title, u"Страница 1")
        self.assertEqual (tabsController.getPage (1).title, u"Страница 2")
        self.assertEqual (tabsController.getPage (2).title, u"Страница 4")
        self.assertEqual (tabsController.getPage (3).title, u"Страница 3")


    def testRestore_04 (self):
        self.__createWiki2()
        wiki2 = WikiDocument.load (self.path2, False)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink (self.wikiroot[u"Страница 1"])
        uid2 = self._getPageLink (self.wikiroot[u"Страница 2"])

        Application.wikiroot = wiki2
        self.assertEqual (tabsController.getTabsCount(), 1)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 2)
        self.assertEqual (tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual (newsession.pages[0], uid1)
        self.assertEqual (newsession.pages[1], uid2)


    def testRestore_05 (self):
        self.__createWiki2()
        wiki2 = WikiDocument.load (self.path2, True)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (self.wikiroot[u"Страница 2"], True)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        uid1 = self._getPageLink (self.wikiroot[u"Страница 1"])
        uid2 = self._getPageLink (self.wikiroot[u"Страница 2"])

        Application.wikiroot = wiki2
        self.assertEqual (tabsController.getTabsCount(), 1)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 2)
        self.assertEqual (tabsController.getSelection(), 1)

        newsession = controller.getCurrentSession()
        self.assertEqual (newsession.pages[0], uid1)
        self.assertEqual (newsession.pages[1], uid2)


    def testRestoreReadonly_01 (self):
        wiki = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = wiki
        Application.selectedPage = wiki[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (wiki[u"Страница 2"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3/Страница 4"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3"], False)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        Application.wikiroot = None
        self.assertEqual (tabsController.getTabsCount(), 0)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertTrue (Application.wikiroot.readonly)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 4)
        self.assertEqual (tabsController.getSelection(), 2)

        self.assertEqual (tabsController.getPage (0).title, u"Страница 1")
        self.assertEqual (tabsController.getPage (1).title, u"Страница 2")
        self.assertEqual (tabsController.getPage (2).title, u"Страница 4")
        self.assertEqual (tabsController.getPage (3).title, u"Страница 3")


    def testRestoreReadonly_02 (self):
        wiki = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = wiki
        Application.selectedPage = wiki[u"Страница 1"]

        tabsController = Application.mainWindow.tabsController
        tabsController.openInTab (wiki[u"Страница 2"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3/Страница 4"], True)
        tabsController.openInTab (wiki[u"Страница 1/Страница 3"], False)

        controller = self.loader[u"Sessions"].SessionController(Application)
        session = controller.getCurrentSession()

        tabsController.closeTab (1)
        tabsController.closeTab (1)
        tabsController.closeTab (1)

        controller.restore (session)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertTrue (Application.wikiroot.readonly)

        self.assertEqual (os.path.abspath (Application.wikiroot.path), os.path.abspath (self.path))
        self.assertEqual (tabsController.getTabsCount(), 4)
        self.assertEqual (tabsController.getSelection(), 2)

        self.assertEqual (tabsController.getPage (0).title, u"Страница 1")
        self.assertEqual (tabsController.getPage (1).title, u"Страница 2")
        self.assertEqual (tabsController.getPage (2).title, u"Страница 4")
        self.assertEqual (tabsController.getPage (3).title, u"Страница 3")


    def _getPageLink (self, page):
        return u"page://" + Application.pageUidDepot.createUid (page)
