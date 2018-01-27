# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.defines import (PAGE_MODE_TEXT,
                                   PAGE_MODE_PREVIEW,
                                   PAGE_MODE_HTML)
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView
from outwiker.pages.wiki.wikiconfig import WikiConfig

from test.guitests.basemainwnd import BaseMainWndTest


class WikiPageViewTest(BaseMainWndTest):
    """
    Тесты вида викистраниц
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)
        Application.onPostprocessing.clear()
        Application.onPreprocessing.clear()

        WikiConfig(Application.config).showHtmlCodeOptions.value = False

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        WikiPageFactory().create(self.wikiroot, "Викистраница 2", [])

    def tearDown(self):
        BaseMainWndTest.tearDown(self)
        Application.onPostprocessing.clear()
        Application.onPreprocessing.clear()

    def testType(self):
        Application.wikiroot = self.wikiroot
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(WikiPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot["Викистраница 2"]
        self.assertEqual(WikiPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

    def testSwitch(self):
        WikiConfig(Application.config).showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(WikiPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot["Викистраница 2"]
        self.assertEqual(WikiPageView,
                         type(Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual(None, Application.mainWindow.pagePanel.pageView)

    def testDefaultSelectedPage(self):
        """
        Тест на выбор вкладок по умолчанию
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["Викистраница 2"]

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
        Application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_PREVIEW)

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)

        self.assertEqual(
            Application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_HTML)

    def testResultHtmlPage1(self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = False

        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.selectedPage = None
        config.showHtmlCodeOptions.value = True

        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(Application.mainWindow.pagePanel.pageView.pageCount, 3)

    def testResultHtmlPage2(self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)
        self.assertEqual(Application.mainWindow.pagePanel.pageView.pageCount, 3)

    def testInvalidPageIndex(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = 100

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_PREVIEW)

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = 1000

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        Application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

    def testSavePageIndex1(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла 2"
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]
        wx.GetApp().Yield()

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        Application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на результирующий HTML
        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбана страница с кодом
        Application.selectedPage = self.wikiroot["Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        Application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)

    def testSavePageIndex2(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла 2"
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        Application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на результирующий HTML
        Application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбрана страница с кодом
        Application.selectedPage = self.wikiroot["Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        Application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(Application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)

    def testCursorPosition_01(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(3, 3)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testCursorPosition_02(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(0, 0)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 0)

    def testCursorPosition_readonly_01(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        Application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(3, 3)
        Application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
        wikiroot_ro = WikiDocument.load(self.path, readonly=True)
        Application.wikiroot = wikiroot_ro
        Application.selectedPage = wikiroot_ro["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection(0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        Application.selectedPage = None
        Application.selectedPage = wikiroot_ro["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testPostprocessing_01(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]
        Application.onPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        Application.onPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111"))

    def testPostprocessing_02(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]

        Application.onPostprocessing += self._onPostProcessing
        Application.onPostprocessing += self._onPostProcessing2

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        Application.onPostprocessing -= self._onPostProcessing
        Application.onPostprocessing -= self._onPostProcessing2

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111 222"))

    def testPostprocessing_03(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]
        Application.onPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Попереключаемся по вкладкам и проверим, что результат
        # постпроцессинга применен однократно
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        Application.onPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111"))
        self.assertFalse(result.endswith(" 111 111"))

    def testPreprocessing_01(self):
        """
        Тест на работу препроцессинга
        """
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Викистраница"]
        Application.onPreprocessing += self._onPreProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        Application.onPreprocessing -= self._onPreProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertIn("Абырвалг 000", result)

    def testSave_01(self):
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        page = self.wikiroot["Викистраница"]
        page.content = ""

        Application.wikiroot = self.wikiroot
        Application.selectedPage = page

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        self.assertEqual(page.content, "Абырвалг")

    def testSave_02(self):
        config = WikiConfig(Application.config)
        config.showHtmlCodeOptions.value = True

        page = self.wikiroot["Викистраница"]
        page.content = ""

        Application.wikiroot = self.wikiroot
        Application.selectedPage = page

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на просмотр
        pageView.SetPageMode(PAGE_MODE_PREVIEW)
        wx.GetApp().Yield()

        self.assertEqual(page.content, "Абырвалг")

    def _getPageView(self):
        return Application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().codeEditor

    def _onPostProcessing(self, page, params):
        params.result += " 111"

    def _onPostProcessing2(self, page, params):
        params.result += " 222"

    def _onPreProcessing(self, page, params):
        params.result += " 000"
