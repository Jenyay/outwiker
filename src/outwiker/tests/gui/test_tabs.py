# -*- coding: utf-8 -*-

from os.path import basename
import unittest

from outwiker.api.core.tree import loadNotesTree
from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.app.gui.tabscontroller import TabsController
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class TabsTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication(enableActionsGui=True)
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        self._page_1 = factory.create(self.wikiroot, "Страница 1", [])
        self._page_2 = factory.create(self.wikiroot, "Страница 2", [])
        self._page_3 = factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        self._page_4 = factory.create(
            self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        self._page_5 = factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self._tabsController: TabsController = self.application.mainWindow.tabsController

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testInit(self):
        # Пока нет откытых вики, нет и вкладок
        self.assertEqual(self._tabsController.getTabsCount(), 0)

    def testCloneEmpty1(self):
        # Пока нет откытых вики, нет и вкладок
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        self._tabsController.cloneTab()
        self.assertEqual(self._tabsController.getTabsCount(), 0)

    def testCloneEmpty2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        self._tabsController.cloneTab()
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getPage(0), None)
        self.assertEqual(self._tabsController.getPage(1), None)

    def testOpenWiki(self):
        # Откываем вики, где нет сохраненных вкладок
        self.application.wikiroot = self.wikiroot

        # Должна быть одна вкладка
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual(self._tabsController.getSelection(), 0)

        # Выбранной страницы нет
        self.assertEqual(self._tabsController.getPage(0), None)

        # Так как нет выбранной страницы, то заголовок вкладки содержит имя папки с вики
        self.assertEqual(self._tabsController.getTabTitle(0),
                         basename(self.wikiroot.path))

    def testSelection(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        # Должна быть одна вкладка
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual(self._tabsController.getSelection(), 0)

        # Выбранная страница должна быть отражена на текущей вкладке
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

        # Выберем более вложенную страницу
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 3")

        # Выберем более вложенную страницу
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.assertEqual(self._tabsController.getPage(0),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 4")

    def testCloneTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self._tabsController.cloneTab()
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 1")

        self._tabsController.cloneTab()
        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getSelection(), 2)

    def testCloneTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self._tabsController.cloneTab()
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.cloneTab()

        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 2")

        self.assertEqual(self._tabsController.getPage(2),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getTabTitle(2), "Страница 4")

    def testRemoveSelection(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.wikiroot["Страница 1"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), None)
        self.assertEqual(self._tabsController.getTabTitle(0), basename(self.wikiroot.path))

    def testRemoveSelection2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.wikiroot["Страница 2"].remove()

        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1), None)
        self.assertEqual(self._tabsController.getTabTitle(1), basename(self.wikiroot.path))

    def testRemoveSelection3(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self.wikiroot["Страница 2"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1), None)
        self.assertEqual(self._tabsController.getTabTitle(1), basename(self.wikiroot.path))

    def testRenameSelection(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.wikiroot["Страница 1"].title = "Бла-бла-бла"

        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Бла-бла-бла"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Бла-бла-бла")

    def testRename(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self.wikiroot["Страница 1"].title = "Бла-бла-бла"

        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Бла-бла-бла"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Бла-бла-бла")

        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Бла-бла-бла"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Бла-бла-бла")

        self.assertEqual(self._tabsController.getPage(2), self.wikiroot["Бла-бла-бла"])
        self.assertEqual(self._tabsController.getTabTitle(2), "Бла-бла-бла")

    def testRemove1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self.wikiroot["Страница 1"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), None)
        self.assertEqual(self._tabsController.getTabTitle(0), basename(self.wikiroot.path))

    def testRemove2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)

        self.wikiroot["Страница 1"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 2")

    def testRemove3(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.wikiroot["Страница 1"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getSelection(), 0)

        self.assertEqual(self._tabsController.getPage(0), None)
        self.assertEqual(self._tabsController.getTabTitle(0), basename(self.wikiroot.path))

        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 2")

    def testRemove4(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.wikiroot["Страница 2"].remove()
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getSelection(), 0)

        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

    def testOpenInTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], True)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(self._tabsController.getSelection(), 1)

        self.assertEqual(self._tabsController.getPage(1),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 4")

    def testOpenInTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

        self.assertEqual(self._tabsController.getPage(1),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 4")

    def testOpenInTab3(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self._tabsController.setSelection(0)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], True)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual(self._tabsController.getTabTitle(1), "Страница 4")

    def testSetSelection(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

        self._tabsController.setSelection(2)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getSelection(), 2)
        self.assertEqual(self._tabsController.getPage(2), self.wikiroot["Страница 2"])

        self._tabsController.setSelection(1)
        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getSelection(), 1)
        self.assertEqual(self._tabsController.getPage(1),
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

    def testCloseWiki(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.wikiroot = None
        self.assertEqual(self._tabsController.getTabsCount(), 0)

    def testSaveTabs1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.wikiroot = None
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getSelection(), 0)
        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")

    def testSaveTabs2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        self.application.wikiroot = None
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki

        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getSelection(), 0)

        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")
        self.assertEqual(self._tabsController.getPage(1),
                         otherwiki["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getPage(2), otherwiki["Страница 2"])

    def testSaveTabs3(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], False)
        self._tabsController.setSelection(1)

        self.application.wikiroot = None
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki

        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getSelection(), 1)

        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")
        self.assertEqual(self._tabsController.getPage(1),
                         otherwiki["Страница 2/Страница 3/Страница 4"])
        self.assertEqual(self._tabsController.getPage(2), otherwiki["Страница 2"])

    def testSaveTabs4(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3/Страница 4"], False)
        self._tabsController.setSelection(1)
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        self.application.wikiroot = None
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki

        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getSelection(), 1)

        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual(self._tabsController.getTabTitle(0), "Страница 1")
        self.assertEqual(self._tabsController.getPage(1),
                         otherwiki["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getPage(2), otherwiki["Страница 2"])

    def testSaveTabs5(self):
        wiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = wiki

        self.application.selectedPage = wiki["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab(wiki["Страница 2"], True)
        self.assertEqual(self._tabsController.getTabsCount(), 3)

        # Загрузим вики еще раз, чтобы убедиться, что состояние вкладок мы не поменяли
        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki
        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self.application.selectedPage, otherwiki["Страница 2"])

    def testSaveAfterRemove(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self._tabsController.cloneTab()
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self.wikiroot["Страница 1"].remove()

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki

        self.assertEqual(self._tabsController.getTabsCount(), 4)
        self.assertEqual(self._tabsController.getSelection(), 3)
        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 2"])
        self.assertEqual(self._tabsController.getPage(3), otherwiki["Страница 2"])

    def testSaveAfterMove(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)

        self.wikiroot["Страница 1"].moveTo(self.wikiroot["Страница 2"])

        otherwiki = loadNotesTree(self.wikiroot.path)
        self.application.wikiroot = otherwiki
        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self._tabsController.getPage(0), otherwiki["Страница 2/Страница 1"])
        self.assertEqual(self._tabsController.getPage(1), otherwiki["Страница 2/Страница 1"])
        self.assertEqual(self._tabsController.getPage(2), otherwiki["Страница 2"])

    def testMove(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.setSelection(2)

        self.wikiroot["Страница 1"].moveTo(self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot["Страница 2/Страница 1"], self._tabsController.getPage(0))
        self.assertEqual(self.wikiroot["Страница 2/Страница 1"], self._tabsController.getPage(1))

        self._tabsController.setSelection(0)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 1"])

    def testReadOnly(self):
        wikiReadOnly = loadNotesTree(self.wikiroot.path, readonly=True)
        self.application.wikiroot = wikiReadOnly

        self.application.selectedPage = wikiReadOnly["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab(wikiReadOnly["Страница 2"], True)
        self.assertEqual(self._tabsController.getTabsCount(), 3)

        # Загрузим вики еще раз, чтобы убедиться, что состояние вкладок мы не поменяли
        otherwiki = loadNotesTree(self.wikiroot.path, readonly=True)
        self.application.wikiroot = otherwiki
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self.application.selectedPage, None)

    def testCloseLastTab(self):
        """
        Тест на попытку закрыть единственную вкладку
        """
        self.application.wikiroot = self.wikiroot
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        self._tabsController.closeTab(0)
        self.assertEqual(self._tabsController.getTabsCount(), 0)

    def testCloseTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertEqual(self._tabsController.getTabsCount(), 3)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])

        self._tabsController.closeTab(0)
        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])

        self._tabsController.closeTab(0)
        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])

    def testCloseTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertEqual(self._tabsController.getTabsCount(), 3)

        self._tabsController.closeTab(2)

        self.assertEqual(self._tabsController.getTabsCount(), 2)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])

        self._tabsController.closeTab(1)

        self.assertEqual(self._tabsController.getTabsCount(), 1)
        self.assertEqual(self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

    def testCloseLastTabAndSelectPage(self):
        self.application.wikiroot = self.wikiroot
        self.assertEqual(self._tabsController.getTabsCount(), 1)

        self._tabsController.closeTab(0)
        self.assertEqual(self._tabsController.getTabsCount(), 0)

        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self._tabsController.getTabsCount(), 1)

    def testNextTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._tabsController.nextTab()

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getSelection(), 1)

        self._tabsController.nextTab()

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getSelection(), 2)

        self._tabsController.nextTab()

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testNextTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._tabsController.nextTab()

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testPrevTab1(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._tabsController.previousTab()
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual(self._tabsController.getSelection(), 2)

        self._tabsController.previousTab()
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual(self._tabsController.getSelection(), 1)

        self._tabsController.previousTab()
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testPrevTab2(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

        self._tabsController.previousTab()

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual(self._tabsController.getSelection(), 0)

    def testCloseTabInvalid(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises(ValueError, self._tabsController.closeTab, -1)
        self.assertRaises(ValueError, self._tabsController.closeTab, 3)
        self.assertRaises(ValueError, self._tabsController.closeTab, 5)

    def testTabTitleInvalid(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises(ValueError, self._tabsController.getTabTitle, -1)
        self.assertRaises(ValueError, self._tabsController.getTabTitle, 3)
        self.assertRaises(ValueError, self._tabsController.getTabTitle, 5)

    def testSetSelectionInvalid(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises(ValueError, self._tabsController.setSelection, -1)
        self.assertRaises(ValueError, self._tabsController.setSelection, 3)
        self.assertRaises(ValueError, self._tabsController.setSelection, 5)

    def testGetPageInvalid(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab(self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises(ValueError, self._tabsController.getPage, -1)
        self.assertRaises(ValueError, self._tabsController.getPage, 3)
        self.assertRaises(ValueError, self._tabsController.getPage, 5)

    def testHistoryEmpty(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryBackAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistoryGoto(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistoryCloseWiki(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self.application.wikiroot = None
        self.application.wikiroot = self.wikiroot

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistorySeveralTabs_01(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

        self.application.selectedPage = self.wikiroot["Страница 1"]

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistorySeveralTabs_02(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab(self.wikiroot["Страница 2"], True)
        self._tabsController.setSelection(0)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistorySeveralTabs_03(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab(self.wikiroot["Страница 2"], False)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistoryBack_01(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertTrue(info_forward.menuItem.IsEnabled())

    def testHistoryBack_02(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = None

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertTrue(info_forward.menuItem.IsEnabled())

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistoryBackForward_01(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.application.selectedPage = None

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3"])

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2"])

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertTrue(info_forward.menuItem.IsEnabled())

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2"])

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3"])

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, None)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def testHistoryBackForward_02(self):
        actionController = self.application.actionController
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.selectedPage = self.wikiroot["Страница 2"]
        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.application.selectedPage = None

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, None)

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2"])

        self.application.actionController.getAction(HistoryBackAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertFalse(info_back.menuItem.IsEnabled())
        self.assertTrue(info_forward.menuItem.IsEnabled())

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2"])

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, None)

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.application.actionController.getAction(HistoryForwardAction.stringId).run(None)

        self.assertEqual(self.application.selectedPage, None)

        info_back = actionController.getActionInfo(HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

        self.assertTrue(info_back.menuItem.IsEnabled())
        self.assertFalse(info_forward.menuItem.IsEnabled())

    def test_MoveTab_NotChange(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(0, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getSelection(), 0)

    def test_MoveTab_MoveFirstSelectedToNeighboring(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(0, 1)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getSelection(), 1)

    def test_MoveTab_MoveFirstSelected_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(0, 2)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getSelection(), 2)

    def test_MoveTab_FirstSelectedToLastPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(0, 4)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getSelection(), 4)

    def test_MoveTab_SecondSelectedToFirstPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(1)

        self._tabsController.movePage(1, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getSelection(), 0)

    def test_MoveTab_SecondSelectedToLastPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(1)

        self._tabsController.movePage(1, 4)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getSelection(), 4)

    def test_MoveTab_SecondTabToFirstPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(1, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getSelection(), 1)

    def test_MoveTab_SecondTabToLastPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(1, 4)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getSelection(), 0)

    def test_MoveTab_LastTabToFirstPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)

        self._tabsController.movePage(4, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getSelection(), 1)

    def test_MoveTab_LastSelectedTabToFirstPosition(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(4)

        self._tabsController.movePage(4, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getSelection(), 0)

    def test_MoveTab_FirstTabToLastPositionSelectedLast(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(4)

        self._tabsController.movePage(0, 4)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getSelection(), 3)

    def test_MoveTab_LastTabToBeforeSelection_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(2)

        self._tabsController.movePage(4, 2)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getSelection(), 3)

    def test_MoveTab_LastTabToBeforeSelection_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._page_1
        self._tabsController.addNewTab(self._page_2, False)
        self._tabsController.addNewTab(self._page_3, False)
        self._tabsController.addNewTab(self._page_4, False)
        self._tabsController.addNewTab(self._page_5, False)
        self._tabsController.setSelection(2)

        self._tabsController.movePage(4, 0)
        self.assertEqual(self._tabsController.getPage(0).subpath, self._page_5.subpath)
        self.assertEqual(self._tabsController.getPage(1).subpath, self._page_1.subpath)
        self.assertEqual(self._tabsController.getPage(2).subpath, self._page_2.subpath)
        self.assertEqual(self._tabsController.getPage(3).subpath, self._page_3.subpath)
        self.assertEqual(self._tabsController.getPage(4).subpath, self._page_4.subpath)
        self.assertEqual(self._tabsController.getSelection(), 3)
