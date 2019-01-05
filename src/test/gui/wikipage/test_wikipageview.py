# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.defines import (PAGE_MODE_TEXT,
                                   PAGE_MODE_PREVIEW,
                                   PAGE_MODE_HTML)
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.listautocomplete import listComplete_wiki
from test.basetestcases import BaseOutWikerGUIMixin


class WikiPageViewTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты вида викистраниц
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.application.onPostprocessing.clear()
        self.application.onPreprocessing.clear()

        WikiConfig(self.application.config).showHtmlCodeOptions.value = False

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        WikiPageFactory().create(self.wikiroot, "Викистраница 2", [])

    def tearDown(self):
        self.application.onPostprocessing.clear()
        self.application.onPreprocessing.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testType(self):
        self.application.wikiroot = self.wikiroot
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(WikiPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = self.wikiroot["Викистраница 2"]
        self.assertEqual(WikiPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = None
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

    def testSwitch(self):
        WikiConfig(self.application.config).showHtmlCodeOptions.value = True

        self.application.wikiroot = self.wikiroot
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(WikiPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = self.wikiroot["Викистраница 2"]
        self.assertEqual(WikiPageView,
                         type(self.application.mainWindow.pagePanel.pageView))

        self.application.selectedPage = None
        self.assertEqual(None, self.application.mainWindow.pagePanel.pageView)

    def testDefaultSelectedPage(self):
        """
        Тест на выбор вкладок по умолчанию
        """
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Викистраница 2"]

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
        self.application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_PREVIEW)

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)

        self.assertEqual(
            self.application.mainWindow.pagePanel.pageView.GetPageMode(),
            PAGE_MODE_HTML)

    def testResultHtmlPage1(self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = False

        self.application.wikiroot = self.wikiroot

        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.pageCount, 2)

        self.application.selectedPage = None
        config.showHtmlCodeOptions.value = True

        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.pageCount, 3)

    def testResultHtmlPage2(self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        self.application.wikiroot = self.wikiroot

        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.pageCount, 2)

        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.pageCount, 3)

    def testInvalidPageIndex(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = 100

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_PREVIEW)

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = 1000

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        self.application.mainWindow.pagePanel.pageView._selectedPageIndex = -1

        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

    def testSavePageIndex1(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла 2"
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        wx.GetApp().Yield()

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        self.application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на результирующий HTML
        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбана страница с кодом
        self.application.selectedPage = self.wikiroot["Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        self.application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)

    def testSavePageIndex2(self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.wikiroot["Викистраница 2"].content = "Бла-бла-бла 2"
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на вкладку с кодом
        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        self.application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_PREVIEW)

        # Переключимся на результирующий HTML
        self.application.mainWindow.pagePanel.pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбрана страница с кодом
        self.application.selectedPage = self.wikiroot["Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_TEXT)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        self.application.selectedPage = self.wikiroot["Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual(self.application.mainWindow.pagePanel.pageView.GetPageMode(),
                         PAGE_MODE_HTML)

    def testCursorPosition_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(3, 3)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testCursorPosition_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(0, 0)

        self.application.selectedPage = None
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 0)

    def testCursorPosition_readonly_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot["Викистраница"].content = "Бла-бла-бла"
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self._getCodeEditor().SetSelection(3, 3)
        self.application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
        wikiroot_ro = WikiDocument.load(self.wikiroot.path, readonly=True)
        self.application.wikiroot = wikiroot_ro
        self.application.selectedPage = wikiroot_ro["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection(0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        self.application.selectedPage = None
        self.application.selectedPage = wikiroot_ro["Викистраница"]
        self.assertEqual(self._getCodeEditor().GetCurrentPosition(), 3)

    def testPostprocessing_01(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.application.onPostprocessing += self._onPostProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        self.application.onPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111"))

    def testPostprocessing_02(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]

        self.application.onPostprocessing += self._onPostProcessing
        self.application.onPostprocessing += self._onPostProcessing2

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        self.application.onPostprocessing -= self._onPostProcessing
        self.application.onPostprocessing -= self._onPostProcessing2

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111 222"))

    def testPostprocessing_03(self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.application.onPostprocessing += self._onPostProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

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

        self.application.onPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue(result.endswith(" 111"))
        self.assertFalse(result.endswith(" 111 111"))

    def testPreprocessing_01(self):
        """
        Тест на работу препроцессинга
        """
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.application.onPreprocessing += self._onPreProcessing

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.SetPageMode(PAGE_MODE_TEXT)
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        self.application.onPreprocessing -= self._onPreProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertIn("Абырвалг 000", result)

    def testSave_01(self):
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        page = self.wikiroot["Викистраница"]
        page.content = ""

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на результирующий HTML
        pageView.SetPageMode(PAGE_MODE_HTML)
        wx.GetApp().Yield()

        self.assertEqual(page.content, "Абырвалг")

    def testSave_02(self):
        config = WikiConfig(self.application.config)
        config.showHtmlCodeOptions.value = True

        page = self.wikiroot["Викистраница"]
        page.content = ""

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        pageView = self.application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        pageView.codeEditor.SetText("Абырвалг")

        # Переключимся на просмотр
        pageView.SetPageMode(PAGE_MODE_PREVIEW)
        wx.GetApp().Yield()

        self.assertEqual(page.content, "Абырвалг")

    def test_list_autocomplete_none_01(self):
        text = ''
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        result = listComplete_wiki(editor)
        self.assertFalse(result)
        self.assertEqual(editor.GetText(), text)

    def test_list_autocomplete_none_02(self):
        text = '** бла-бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(1)

        result = listComplete_wiki(editor)
        self.assertFalse(result)
        self.assertEqual(editor.GetText(), text)

    def test_list_autocomplete_none_03(self):
        text = '** бла-бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.SetSelection(5, 8)

        result = listComplete_wiki(editor)
        self.assertFalse(result)
        self.assertEqual(editor.GetText(), text)

    def test_list_autocomplete_none_04(self):
        text = '** бла-бла-бла\n** бла-бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(16)

        result = listComplete_wiki(editor)
        self.assertFalse(result)
        self.assertEqual(editor.GetText(), text)

    def test_list_autocomplete_01(self):
        text = '* бла-бла-бла'
        text_result = '* бла-бла-бла\n* '
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(len(text))

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), len(text_result))

    def test_list_autocomplete_02(self):
        text = '* бла-бла-бла'
        text_result = '* бла\n* -бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(5)

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), 8)

    def test_list_autocomplete_03(self):
        text = '** бла-бла-бла'
        text_result = '** бла-бла-бла\n** '
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(len(text))

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), len(text_result))

    def test_list_autocomplete_04(self):
        text = '** бла-бла-бла'
        text_result = '** бла\n** -бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(6)

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), 10)

    def test_list_autocomplete_05(self):
        text = '# бла-бла-бла'
        text_result = '# бла-бла-бла\n# '
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(len(text))

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), len(text_result))

    def test_list_autocomplete_06(self):
        text = '## бла-бла-бла'
        text_result = '## бла-бла-бла\n## '
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(len(text))

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), len(text_result))

    def test_list_autocomplete_07(self):
        text = '* бла-бла-бла'
        text_result = '*\n*  бла-бла-бла'
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(1)

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), 4)

    def test_list_autocomplete_remove_01(self):
        text = '* '
        text_result = ''
        page = self.wikiroot["Викистраница"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = page

        editor = self._getCodeEditor()
        editor.SetText(text)
        editor.GotoPos(len(text))

        result = listComplete_wiki(editor)
        self.assertTrue(result)
        self.assertEqual(editor.GetText(), text_result)
        self.assertEqual(editor.GetSelectionStart(), len(text_result))

    def _getPageView(self):
        return self.application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().codeEditor

    def _onPostProcessing(self, page, params):
        params.result += " 111"

    def _onPostProcessing2(self, page, params):
        params.result += " 222"

    def _onPreProcessing(self, page, params):
        params.result += " 000"
