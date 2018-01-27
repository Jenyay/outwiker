# -*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.application import Application
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.tree import WikiDocument
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.utilites.textfile import readTextFile
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.html.htmlpageview import HtmlPageView

from test.guitests.basemainwnd import BaseMainWndTest


class HtmlPageViewTest(BaseMainWndTest):
    """
    Тесты вида HTML-страниц
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)
        Application.onPostprocessing.clear()
        Application.onPreprocessing.clear()

        HtmlPageFactory().create(self.wikiroot, "HTML-страница", [])
        HtmlPageFactory().create(self.wikiroot, "HTML-страница 2", [])

    def tearDown(self):
        BaseMainWndTest.tearDown(self)
        Application.onPostprocessing.clear()
        Application.onPreprocessing.clear()

    def testType(self):
        Application.wikiroot = self.wikiroot
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(HtmlPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot["HTML-страница 2"]
        self.assertEqual(HtmlPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

    def testDefaultSelectedPage(self):
        """
        Тест на выбор вкладок по умолчанию
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.wikiroot["HTML-страница 2"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["HTML-страница 2"]

        # Т.к. страница НЕ пустая, то по умолчанию выбирается
        # вкладка с просмотром
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testSelectedPage(self):
        """
        Тест на выбор вкладок
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

    def testInvalidPageIndex(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = 100

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = 1000

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testSavePageIndex(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        self.wikiroot["HTML-страница 2"].content = "Бла-бла-бла 2"

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX

        Application.selectedPage = self.wikiroot["HTML-страница"]
        wx.GetApp().Yield()

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        # Переключимся на другую страницу. Опять должна быть выбрана
        # вкладка с просмотром
        Application.selectedPage = self.wikiroot["HTML-страница 2"]
        wx.GetApp().Yield()

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            HtmlPageView.RESULT_PAGE_INDEX)

        # А при возврате на предыдущую страницу, должна быть выбрана
        # страница с кодом
        Application.selectedPage = self.wikiroot["HTML-страница"]
        wx.GetApp().Yield()

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с
        # результирующим HTML
        Application.selectedPage = self.wikiroot["HTML-страница 2"]
        wx.GetApp().Yield()

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

    def testCursorPosition_01(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(3, 3)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testCursorPosition_02(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(0, 0)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 0)

    def testCursorPosition_readonly_01(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot["HTML-страница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["HTML-страница"]
        self._getCodeEditor().SetSelection(3, 3)
        Application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения
        # и поменяем позицию
        wikiroot_ro = WikiDocument.load(self.path, readonly=True)
        Application.wikiroot = wikiroot_ro
        Application.selectedPage = wikiroot_ro["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection(0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        Application.selectedPage = None
        Application.selectedPage = wikiroot_ro["HTML-страница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testPostprocessing_01(self):
        """
        Тест на работу постпроцессинга
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]
        Application.onPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        Application.onPostprocessing -= self._onPostProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertTrue(result.endswith(" 111"))

    def testPostprocessing_02(self):
        """
        Тест на работу постпроцессинга
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]
        Application.onPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

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

        Application.onPostprocessing -= self._onPostProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertTrue(result.endswith(" 111"))
        self.assertFalse(result.endswith(" 111 111"))

    def testPreprocessing_01(self):
        """
        Тест на работу препроцессинга
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["HTML-страница"]
        Application.onPreprocessing += self._onPreProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # Сначала по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView._selectedPageIndex = HtmlPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView._selectedPageIndex = HtmlPageView.RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        Application.onPreprocessing -= self._onPreProcessing

        result = readTextFile(os.path.join(self.wikiroot["HTML-страница"].path,
                                           PAGE_RESULT_HTML))

        self.assertIn("Абырвалг 000", result)

    def _getPageView(self):
        return Application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().codeEditor

    def _onPostProcessing(self, page, params):
        params.result += " 111"

    def _onPreProcessing(self, page, params):
        params.result += " 000"
