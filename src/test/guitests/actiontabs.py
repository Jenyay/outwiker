#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.actions.tabs import AddTabAction, CloseTabAction, PreviousTabAction, NextTabAction
from outwiker.core.application import Application
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest
from test.utils import removeWiki

class ActionTabsTest(BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        TextPageFactory.create (self.wikiroot, u"Страница 1", [])
        TextPageFactory.create (self.wikiroot, u"Страница 2", [])
        TextPageFactory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        TextPageFactory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        TextPageFactory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])

        self._tabsController = Application.mainWindow.tabsController
        self._actionController = Application.actionController


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testCloneEmpty2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        self._actionController.getAction (AddTabAction.stringId).run(None)

        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getPage(0), None)
        self.assertEqual (self._tabsController.getPage(1), None)



    def testCloneTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        self._actionController.getAction (AddTabAction.stringId).run(None)
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1), self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (1), u"Страница 1")

        self._actionController.getAction (AddTabAction.stringId).run(None)
        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (self._tabsController.getSelection(), 2)


    def testCloneTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        self._actionController.getAction (AddTabAction.stringId).run(None)
        Application.selectedPage = self.wikiroot[u"Страница 2"]

        self._actionController.getAction (AddTabAction.stringId).run(None)

        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3/Страница 4"]

        self.assertEqual (self._tabsController.getPage(0), self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), u"Страница 1")

        self.assertEqual (self._tabsController.getPage(1), self.wikiroot[u"Страница 2"])
        self.assertEqual (self._tabsController.getTabTitle (1), u"Страница 2")

        self.assertEqual (self._tabsController.getPage(2), 
                self.wikiroot[u"Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getTabTitle (2), u"Страница 4")


    def testCloseLastTab (self):
        """
        Тест на попытку закрыть единственную вкладку
        """
        Application.wikiroot = self.wikiroot
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        
        self._actionController.getAction (CloseTabAction.stringId).run(None)
        self.assertEqual (self._tabsController.getTabsCount(), 1)


    def testCloseTab (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]
        self._tabsController.openInTab (self.wikiroot[u"Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot[u"Страница 2/Страница 3"], True)

        self.assertEqual (self._tabsController.getTabsCount(), 3) 

        self._actionController.getAction (CloseTabAction.stringId).run(None)

        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getPage (1), self.wikiroot[u"Страница 2"])
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 2"])

        self._actionController.getAction (CloseTabAction.stringId).run(None)
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot[u"Страница 1"])
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])

        self._actionController.getAction (CloseTabAction.stringId).run(None)
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot[u"Страница 1"])
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])


    def testNextTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]
        self._tabsController.openInTab (self.wikiroot[u"Страница 2/Страница 3"], False)
        self._tabsController.openInTab (self.wikiroot[u"Страница 2"], False)

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._actionController.getAction (NextTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 2"])
        self.assertEqual (self._tabsController.getSelection(), 1)

        self._actionController.getAction (NextTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getSelection(), 2)

        self._actionController.getAction (NextTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testNextTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._actionController.getAction (NextTabAction.stringId).run(None)

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testPrevTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]
        self._tabsController.openInTab (self.wikiroot[u"Страница 2/Страница 3"], False)
        self._tabsController.openInTab (self.wikiroot[u"Страница 2"], False)

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._actionController.getAction (PreviousTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getSelection(), 2)

        self._actionController.getAction (PreviousTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 2"])
        self.assertEqual (self._tabsController.getSelection(), 1)

        self._actionController.getAction (PreviousTabAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testPrevTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._actionController.getAction (PreviousTabAction.stringId).run(None)

        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)
