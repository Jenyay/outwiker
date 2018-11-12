# -*- coding: utf-8 -*-

import unittest

from outwiker.core.tree import WikiDocument

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.text.textpanel import TextPanel
from test.basetestcases import BaseOutWikerGUIMixin


class TextPageViewTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты вида текстовых страниц
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница", [])
        factory.create(self.wikiroot, "Страница 2", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testType(self):
        self.application.wikiroot = self.wikiroot
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

        self.application.selectedPage = self.wikiroot["Страница"]
        self.assertEqual(TextPanel, type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = self.wikiroot["Страница 2"]
        self.assertEqual(TextPanel, type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = None
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

    def testCursorPosition_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["Страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Страница"]
        self._getCodeEditor().SetSelection(3, 3)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["Страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testCursorPosition_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["Страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Страница"]
        self._getCodeEditor().SetSelection(0, 0)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["Страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 0)

    def testCursorPosition_readonly_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot["Страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Страница"]
        self._getCodeEditor().SetSelection(3, 3)
        self.application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
        wikiroot_ro = WikiDocument.load(self.wikiroot.path, readonly=True)
        self.application.wikiroot = wikiroot_ro
        self.application.selectedPage = wikiroot_ro["Страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection(0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        self.application.selectedPage = None
        self.application.selectedPage = wikiroot_ro["Страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def _getPageView(self):
        return self.application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().textEditor
