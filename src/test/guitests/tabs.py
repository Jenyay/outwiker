#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.gui.mainwindow import MainWindow
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest
from test.utils import removeWiki

class TabsTest(BaseMainWndTest):
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


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testInit (self):
        # Пока нет откытых вики, нет и вкладок
        self.assertEqual (self._tabsController.getTabsCount(), 0)


    def testOpenWiki (self):
        # Откываем вики, где нет сохраненных вкладок
        Application.wikiroot = self.wikiroot

        # Должна быть одна вкладка
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual (self._tabsController.getSelection(), 0)

        # Выбранной страницы нет
        self.assertEqual (self._tabsController.getPage(0), None)

        # Так как нет выбранной страницы, то заголовок вкладки содержит имя папки с вики
        self.assertEqual (self._tabsController.getTabTitle (0), u"testwiki")


    def testSelection (self):
        # Откываем вики, где нет сохраненных вкладок
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        # Должна быть одна вкладка
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual (self._tabsController.getSelection(), 0)

        # Выбранная страница должна быть отражена на текущей вкладке
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot[u"Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), u"Страница 1")

        # Выберем более вложенную страницу
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot[u"Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getTabTitle (0), u"Страница 3")

        # Выберем более вложенную страницу
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3/Страница 4"]
        self.assertEqual (self._tabsController.getPage(0), 
                self.wikiroot[u"Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getTabTitle (0), u"Страница 4")
