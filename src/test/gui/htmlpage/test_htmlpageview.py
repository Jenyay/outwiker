# -*- coding: utf-8 -*-

import os.path
import unittest

import wx

from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.tree import WikiDocument
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.utilites.textfile import readTextFile
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.html.htmlpageview import HtmlPageView
from test.basetestcases import BaseOutWikerGUIMixin


class HtmlPageViewTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты вида HTML-страниц
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.application.onPostprocessing.clear()
        self.application.onPreprocessing.clear()

        HtmlPageFactory().create(self.wikiroot, "HTML-страница", [])
        HtmlPageFactory().create(self.wikiroot, "HTML-страница 2", [])

    def tearDown(self):
        self.application.onPostprocessing.clear()
        self.application.onPreprocessing.clear()

        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testType(self):
        self.application.wikiroot = self.wikiroot
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(HtmlPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = self.wikiroot["HTML-страница 2"]
        self.assertEqual(HtmlPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = None
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

    def testDefaultSelectedPage(self):
        """
        Тест на выбор вкладок по умолчанию
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.wikiroot["HTML-страница 2"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["HTML-страница 2"]

        # Т.к. страница НЕ пустая, то по умолчанию выбирается
        # вкладка с просмотром
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testSelectedPage(self):
        """
        Тест на выбор вкладок
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

    def testInvalidPageIndex(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = 100

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = 1000

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testSavePageIndex(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        self.wikiroot["HTML-страница 2"].content = "Бла-бла-бла 2"

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        self.application.selectedPage = self.wikiroot["HTML-страница"]
        wx.GetApp().Yield()

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        # Переключимся на другую страницу. Опять должна быть выбрана
        # вкладка с просмотром
        self.application.selectedPage = self.wikiroot["HTML-страница 2"]
        wx.GetApp().Yield()

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            HtmlPageView.RESULT_PAGE_INDEX)

        # А при возврате на предыдущую страницу, должна быть выбрана
        # страница с кодом
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        wx.GetApp().Yield()

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с
        # результирующим HTML
        self.application.selectedPage = self.wikiroot["HTML-страница 2"]
        wx.GetApp().Yield()

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testCursorPosition_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(3, 3)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testCursorPosition_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(0, 0)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 0)

    def testCursorPosition_readonly_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(3, 3)
        self.application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения
        # и поменяем позицию
        wikiroot_ro = WikiDocument.load(self.wikiroot.path, readonly=True)
        self.application.wikiroot = wikiroot_ro
        self.application.selectedPage = wikiroot_ro["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection(0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        self.application.selectedPage = None
        self.application.selectedPage = wikiroot_ro["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testPostprocessing_01(self):
        """
        Тест на работу постпроцессинга
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.application.onPostprocessing += self._onPostProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        self.application.onPostprocessing -= self._onPostProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertTrue(result.endswith(" 111"))

    def testPostprocessing_02(self):
        """
        Тест на работу постпроцессинга
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.application.onPostprocessing += self._onPostProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Попереключаемся между вкладками
        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        self.application.onPostprocessing -= self._onPostProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertTrue(result.endswith(" 111"))
        self.assertFalse(result.endswith(" 111 111"))

    def testPreprocessing_01(self):
        """
        Тест на работу препроцессинга
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML-страница"]
        self.application.onPreprocessing += self._onPreProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

        # Сначала по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        self.application.onPreprocessing -= self._onPreProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertIn("Абырвалг 000", result)

    def _getPageView(self):
        return self.application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().codeEditor

    def _onPostProcessing(self, page, params):
        params.result += " 111"

    def _onPreProcessing(self, page, params):
        params.result += " 000"
