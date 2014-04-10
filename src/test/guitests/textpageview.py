#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from test.utils import removeWiki

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.text.textpanel import TextPanel


class TextPageViewTest (BaseMainWndTest):
    """
    Тесты вида текстовых страниц
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        TextPageFactory.create (self.wikiroot, u"Страница", [])
        TextPageFactory.create (self.wikiroot, u"Страница 2", [])


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testType (self):
        Application.wikiroot = self.wikiroot
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot[u"Страница"]
        self.assertEqual (TextPanel, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot[u"Страница 2"]
        self.assertEqual (TextPanel, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)


    def testCursorPosition_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot[u"Страница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Страница"]
        self._getCodeEditor().SetSelection (3, 3)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot[u"Страница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)


    def testCursorPosition_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot[u"Страница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Страница"]
        self._getCodeEditor().SetSelection (0, 0)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot[u"Страница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 0)


    def testCursorPosition_readonly_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot[u"Страница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Страница"]
        self._getCodeEditor().SetSelection (3, 3)
        Application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
        wikiroot_ro = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = wikiroot_ro
        Application.selectedPage = wikiroot_ro[u"Страница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection (0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        Application.selectedPage = None
        Application.selectedPage = wikiroot_ro[u"Страница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)



    def _getPageView (self):
        return Application.mainWindow.pagePanel.pageView


    def _getCodeEditor (self):
        return self._getPageView().textEditor
