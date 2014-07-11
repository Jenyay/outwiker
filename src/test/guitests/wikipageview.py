# -*- coding: UTF-8 -*-

import wx

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from test.utils import removeWiki

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiPageViewTest (BaseMainWndTest):
    """
    Тесты вида викистраниц
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)
        Application.onHtmlPostprocessing.clear()

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        WikiPageFactory().create (self.wikiroot, u"Викистраница 2", [])


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        Application.onHtmlPostprocessing.clear()
        removeWiki (self.path)


    def testType (self):
        Application.wikiroot = self.wikiroot
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (WikiPageView, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = self.wikiroot[u"Викистраница 2"]
        self.assertEqual (WikiPageView, type (Application.mainWindow.pagePanel.pageView))

        Application.selectedPage = None
        self.assertEqual (None, Application.mainWindow.pagePanel.pageView)


    def testDefaultSelectedPage (self):
        """
        Тест на выбор вкладок по умолчанию
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)

        self.wikiroot[u"Викистраница 2"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]

        # Т.к. страница НЕ пустая, то по умолчанию выбирается вкладка с просмотром
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)


    def testSelectedPage (self):
        """
        Тест на выбор вкладок
        """
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.HTML_RESULT_PAGE_INDEX)


    def testResultHtmlPage1 (self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = False

        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.selectedPage = None
        config.showHtmlCodeOptions.value = True

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 3)


    def testResultHtmlPage2 (self):
        """
        Тест на наличие / отсутствие вкладки с результирующим HTML-кодом
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = False

        Application.wikiroot = self.wikiroot

        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 2)

        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.HTML_RESULT_PAGE_INDEX)
        self.assertEqual (Application.mainWindow.pagePanel.pageView.pageCount, 3)


    def testInvalidPageIndex (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 100

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.RESULT_PAGE_INDEX

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = 1000

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)


        Application.mainWindow.pagePanel.pageView.selectedPageIndex = -1

        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)


    def testSavePageIndex1 (self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = True

        self.wikiroot[u"Викистраница"].content = u"Бла-бла-бла"
        self.wikiroot[u"Викистраница 2"].content = u"Бла-бла-бла 2"
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        wx.GetApp().Yield()

        # В начале по умолчанию выбирается вкладка с просмотром
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)

        # Переключимся на результирующий HTML
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбана страница с кодом
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.HTML_RESULT_PAGE_INDEX)


    def testSavePageIndex2 (self):
        """
        Тест на сохранение текущей вкладки страницы
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = False

        self.wikiroot[u"Викистраница"].content = u"Бла-бла-бла"
        self.wikiroot[u"Викистраница 2"].content = u"Бла-бла-бла 2"
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)

        # Переключимся на вкладку с кодом
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.RESULT_PAGE_INDEX)

        # Переключимся на результирующий HTML
        Application.mainWindow.pagePanel.pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        # А при возврате на предыдущую страницу, должна быть выбрана страница с кодом
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.CODE_PAGE_INDEX)

        # При переключении на другую страницу, выбиается вкладка с результирующим HTML
        Application.selectedPage = self.wikiroot[u"Викистраница 2"]

        wx.GetApp().Yield()
        self.assertEqual (Application.mainWindow.pagePanel.pageView.selectedPageIndex,
                          WikiPageView.HTML_RESULT_PAGE_INDEX)


    def testCursorPosition_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot[u"Викистраница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self._getCodeEditor().SetSelection (3, 3)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)


    def testCursorPosition_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        self.wikiroot[u"Викистраница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self._getCodeEditor().SetSelection (0, 0)

        Application.selectedPage = None
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 0)


    def testCursorPosition_readonly_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        # В исходном файле установим курсор на 3-ю позицию
        self.wikiroot[u"Викистраница"].content = u"Бла-бла-бла"
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        self._getCodeEditor().SetSelection (3, 3)
        Application.selectedPage = None

        # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
        wikiroot_ro = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = wikiroot_ro
        Application.selectedPage = wikiroot_ro[u"Викистраница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)
        self._getCodeEditor().SetSelection (0, 0)

        # После возвращения на страницу положение курсора не должно поменяться
        Application.selectedPage = None
        Application.selectedPage = wikiroot_ro[u"Викистраница"]
        self.assertEqual (self._getCodeEditor().GetCurrentPosition(), 3)


    def testPostprocessing_01 (self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        Application.onHtmlPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText (u"Абырвалг")

        # Переключимся на результирующий HTML
        pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        Application.onHtmlPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue (result.endswith (u" 111"))


    def testPostprocessing_02 (self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]

        Application.onHtmlPostprocessing += self._onPostProcessing
        Application.onHtmlPostprocessing += self._onPostProcessing2

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText (u"Абырвалг")

        # Переключимся на результирующий HTML
        pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        Application.onHtmlPostprocessing -= self._onPostProcessing
        Application.onHtmlPostprocessing -= self._onPostProcessing2

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue (result.endswith (u" 111 222"))


    def testPostprocessing_03 (self):
        """
        Тест на работу постпроцессинга
        """
        config = WikiConfig (Application.config)
        config.showHtmlCodeOptions.value = True

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница"]
        Application.onHtmlPostprocessing += self._onPostProcessing

        pageView = Application.mainWindow.pagePanel.pageView

        # В начале по умолчанию выбирается вкладка с просмотром
        wx.GetApp().Yield()

        # Переключимся на вкладку с кодом
        pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.codeEditor.SetText (u"Абырвалг")

        # Попереключаемся по вкладкам и проверим, что результат
        # постпроцессинга применен однократно
        pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.selectedPageIndex = WikiPageView.CODE_PAGE_INDEX
        wx.GetApp().Yield()

        pageView.selectedPageIndex = WikiPageView.HTML_RESULT_PAGE_INDEX
        wx.GetApp().Yield()

        Application.onHtmlPostprocessing -= self._onPostProcessing

        result = pageView.htmlCodeWindow.GetText()

        self.assertTrue (result.endswith (u" 111"))
        self.assertFalse (result.endswith (u" 111 111"))


    def _getPageView (self):
        return Application.mainWindow.pagePanel.pageView


    def _getCodeEditor (self):
        return self._getPageView().codeEditor


    def _onPostProcessing (self, page, result):
        result[0] += u" 111"


    def _onPostProcessing2 (self, page, result):
        result[0] += u" 222"
