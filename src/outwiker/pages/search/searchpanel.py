# -*- coding: UTF-8 -*-

import wx
from functools import cmp_to_key

from outwiker.core.search import Searcher, AllTagsSearchStrategy, AnyTagSearchStrategy
from outwiker.core.tagslist import TagsList
from outwiker.core.commands import pageExists
from outwiker.core.config import IntegerOption
from outwiker.core.system import getOS
from outwiker.gui.basepagepanel import BasePagePanel
from outwiker.gui.tagscloud import TagsCloud
from outwiker.gui.taglabel import EVT_TAG_LEFT_CLICK
from outwiker.gui.longprocessrunner import LongProcessRunner
from .htmlreport import HtmlReport
from .sortstrategies import getSortStrategies


class SearchPanel(BasePagePanel):
    def __init__(self, parent, application):
        BasePagePanel.__init__ (self, parent, application)

        self._allTags = None

        # Текущий результат поиска (список страниц)
        self._currentResultPages = []

        # Секция для хранения найденных результатов (кэш)
        self._resultsSection = u"SearchResults"
        self.sortStrategySection = u"Sort"

        self._resultOptionTemplate = u"page_%d"

        self._strategyList = [AnyTagSearchStrategy, AllTagsSearchStrategy]
        self._sortStrategies = getSortStrategies()

        self.wordsTextCtrl = wx.SearchCtrl(self,
                                           -1,
                                           "",
                                           style=wx.TE_PROCESS_ENTER)
        self.wordsTextCtrl.ShowCancelButton (True)
        self.wordsTextCtrl.SetDescriptiveText (_(u"Search"))

        self.tagsLabel = wx.StaticText(self, -1, _(u"Tags: "))
        self.tagsList = TagsCloud (self)
        self.tagsList.SetMinSize((250, 150))

        strategies = [_(u"Any tag"), _(u"All tags")]
        self.tagsStrategy = wx.RadioBox(self,
                                        -1,
                                        _(u"Tags"),
                                        choices=strategies,
                                        majorDimension=0,
                                        style=wx.RA_SPECIFY_ROWS)
        self.tagsStrategy.SetSelection(0)

        self.clearTagsBtn = wx.Button(self, -1, _(u"Clear all tags"))
        self.searchBtn = wx.Button(self, -1, _(u"Find"))
        self.resultWindow = getOS().getHtmlRender (self)

        self.sortLabel = wx.StaticText(self, -1, _(u"Sort by "))
        self.sortStrategy = wx.ComboBox (self,
                                         -1,
                                         style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.sortStrategy.SetMinSize ((200, -1))
        for sortStrategy in self._sortStrategies:
            self.sortStrategy.Append (sortStrategy.title)
            self.sortStrategy.SetSelection (0)

        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.__onClear, self.clearTagsBtn)

        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
                  lambda event: self.wordsTextCtrl.SetValue (u""),
                  self.wordsTextCtrl)

        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN,
                  self.__onFind,
                  self.wordsTextCtrl)

        self.Bind(wx.EVT_TEXT_ENTER,
                  self.__onFind,
                  self.wordsTextCtrl)

        self.Bind(wx.EVT_BUTTON,
                  self.__onFind,
                  self.searchBtn)

        self.Bind(wx.EVT_COMBOBOX,
                  self.__onChangeSortStrategy,
                  self.sortStrategy)

        self.tagsList.Bind (EVT_TAG_LEFT_CLICK,
                            self.__onTagLeftClick)


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(4, 1, 0, 0)
        mainSizer.AddGrowableRow(3)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(self.wordsTextCtrl, 1, wx.EXPAND, 0)

        rightSizer = wx.FlexGridSizer(cols=1)
        rightSizer.Add(self.tagsStrategy, 0, wx.EXPAND, 0)
        rightSizer.Add(self.clearTagsBtn, 0, wx.ALL | wx.EXPAND, 2)
        rightSizer.Add(self.searchBtn, 0, wx.ALL | wx.EXPAND, 2)
        rightSizer.AddGrowableRow(0)
        rightSizer.AddGrowableCol(0)

        tagsSizer = wx.FlexGridSizer(1, 3, 0, 0)
        tagsSizer.Add(self.tagsLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        tagsSizer.Add(self.tagsList, 0, wx.ALL | wx.EXPAND, 2)
        tagsSizer.Add(rightSizer, 1, wx.EXPAND, 0)
        tagsSizer.AddGrowableCol(1)

        mainSizer.Add(tagsSizer, 1, wx.EXPAND, 0)

        sortSizer = wx.BoxSizer (wx.HORIZONTAL)
        sortSizer.Add (self.sortLabel,
                       1,
                       wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                       border=2)

        sortSizer.Add (self.sortStrategy,
                       1,
                       wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx. EXPAND,
                       border=2)

        mainSizer.Add (sortSizer, 1, wx.EXPAND, 0)

        mainSizer.Add(self.resultWindow, 1, wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(mainSizer)
        self.Layout()


    def __onChangeSortStrategy (self, event):
        """
        Изменение способа сортировки
        """
        self.Save ()
        if self.page is not None:
            self.__showResults (self._currentResultPages)


    def __getCurrentSortStrategy (self):
        """
        Получить стратегию для выбранного типа сортировки
        """
        return self._sortStrategies[self.sortStrategy.GetSelection()]


    def __onTagLeftClick (self, event):
        """
        Обработчик события при клике по метке
        """
        tag = event.text
        self.tagsList.mark (tag, not self.tagsList.isMarked(tag))


    def Print (self):
        """
        Печать страницы (на принтер)
        """
        self.resultWindow.Print()


    def Clear (self):
        pass


    def __updatePageInfo (self):
        """
        Обновить интерфейс, чтобы он соответствовал настройкам страницы
        """
        assert self.page is not None

        self.__updateSearchPhrase()
        self.__updateTagsList()


    def __updateTagsList (self):
        """
        Обновить список тегов
        """
        assert self.page is not None

        # заполним список тегов
        list_items = TagsList (self._application.wikiroot)
        self.tagsList.setTags (list_items)

        tags = self.page.searchTags

        # Поставим галки, где нужно
        for tag in self._allTags:
            if tag in tags:
                self.tagsList.mark (tag)

        # Установим стратегию поиска по тегам
        strategyIndex = self._strategyList.index (self.page.strategy)

        self.tagsStrategy.SetSelection(strategyIndex)


    def __updateSearchPhrase (self):
        """
        Записать искомую фразу из текущей страницы в интерфейс
        """
        self.wordsTextCtrl.SetValue (self.page.phrase)


    def Save (self):
        """
        Сохранить настройки страницы
        """
        if (self.page is not None and
                not self.page.isRemoved and
                pageExists (self.page)):
            self.__saveSearchPhrase()
            self.__saveSearchTags()
            self.__saveSearchTagsStrategy()
            self.__saveSortStrategy ()


    def __saveSearchPhrase (self):
        """
        Сохранить искомую фразу в настройки страницы
        """
        self.page.phrase = self.wordsTextCtrl.GetValue()


    def __saveSearchTags (self):
        """
        Сохранить искомые теги в настройке страницы
        """
        self.page.searchTags = self.__getSearchTags()


    def __saveSearchTagsStrategy (self):
        """
        Сохранить стратегию поиска по тегам (все теги или любой тег)
        """
        strategyIndex = self.tagsStrategy.GetSelection()
        self.page.strategy = self._strategyList[strategyIndex]


    def UpdateView (self, page):
        """
        Обновить внешний вид страницы и отобразить найденные результаты
        """
        self.resultWindow.page = page
        self._allTags = TagsList (self.page.root)
        self.__updatePageInfo()

        self._currentResultPages = self.__loadResults ()

        self.__showResults (self._currentResultPages)
        self.__loadSortStrategy ()


    def __loadSortStrategy (self):
        assert self.page is not None

        sortOption = IntegerOption (self.page.params,
                                    self.page.paramsSection,
                                    self.sortStrategySection,
                                    0)

        sort = sortOption.value
        if sort < 0 or sort >= len (self._sortStrategies):
            sort = 0
            self.sortStrategy.SetSelection (sort)


    def __saveSortStrategy (self):
        assert self.page is not None

        sortOption = IntegerOption (self.page.params,
                                    self.page.paramsSection,
                                    self.sortStrategySection,
                                    0)
        sortOption.value = self.sortStrategy.GetSelection()


    def __onFind (self, event):
        """
        Обработчик события кнопки "Найти"
        """
        assert self.page is not None

        self.page.updateDateTime()
        self.Save()

        phrase = self.__getSearchPhrase()
        tags = self.__getSearchTags()

        searcher = Searcher (phrase, tags, self.page.strategy)

        runner = LongProcessRunner (searcher.find,
                                    self._application.mainWindow,
                                    _(u"Search"),
                                    _(u"Search pages..."))

        self._currentResultPages = runner.run(self.page.root)

        self.__saveResults (self._currentResultPages)
        self.__showResults (self._currentResultPages)


    def __getSearchTags (self):
        """
        Получить список искомых тегов
        """
        tags = []

        for tag in self._allTags:
            if self.tagsList.isMarked (tag):
                tags.append (tag)

        return tags


    def __getSearchPhrase (self):
        """
        Получить искомую фразу
        """
        return self.wordsTextCtrl.GetValue ()


    def __showResults (self, resultPages):
        """
        Показать результат
        """
        sortStrategy = self.__getCurrentSortStrategy()

        resultPages_sorted = resultPages[:]
        resultPages_sorted.sort (key=cmp_to_key(sortStrategy.sort))

        report = HtmlReport (resultPages_sorted,
                             self.__getSearchPhrase(),
                             self.__getSearchTags(),
                             self._application)

        htmltext = report.generate ()
        self.resultWindow.SetPage (htmltext, self.page.path)


    def __saveResults (self, resultPages):
        """
        Сохранить найденные страницы в конфиг
        """
        assert self.page is not None

        self.page.params.remove_section (self._resultsSection)

        for n in range (len (resultPages)):
            option = self._resultOptionTemplate % n
            self.page.params.set (self._resultsSection,
                                  option,
                                  resultPages[n].subpath)


    def __loadResults (self):
        """
        Загрузить найденные страницы из конфига
        """
        assert self.page is not None

        n = 0
        resultPages = []

        try:
            while True:
                option = self._resultOptionTemplate % n
                subpath = self.page.params.get (self._resultsSection, option)

                page = self.page.root[subpath]
                if page is not None:
                    resultPages.append (page)

                n += 1
        except:
            pass

        return resultPages


    def __onClear (self, event):
        """
        Очистка выбранных тегов
        """
        self.tagsList.clearMarks()
