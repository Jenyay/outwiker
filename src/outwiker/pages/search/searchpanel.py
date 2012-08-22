#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ConfigParser

import wx

from outwiker.core.application import Application
from outwiker.core.search import Searcher, AllTagsSearchStrategy, AnyTagSearchStrategy
from outwiker.core.tagslist import TagsList
from .htmlreport import HtmlReport
from outwiker.gui.htmlrenderfactory import getHtmlRender
from outwiker.gui.basepagepanel import BasePagePanel
from outwiker.core.commands import pageExists
from outwiker.gui.tagscloud import TagsCloud
from outwiker.gui.taglabel import EVT_TAG_LEFT_CLICK


class SearchPanel(BasePagePanel):
    def __init__(self, parent, *args, **kwds):
        BasePagePanel.__init__ (self, parent, *args, **kwds)

        self._allTags = None

        # Секция для хранения найденных результатов (кэш)
        self._resultsSection = u"SearchResults"

        self._resultOptionTemplate = u"page_%d"

        self._strategyList = [AnyTagSearchStrategy, AllTagsSearchStrategy]

        self.wordsLabel = wx.StaticText(self, -1, _(u"Search words: "))
        self.wordsTextCtrl = wx.TextCtrl(self, -1, "")
        self.tagsLabel = wx.StaticText(self, -1, _(u"Tags: "))
        self.tagsList = TagsCloud (self)
        self.tagsStrategy = wx.RadioBox(self, -1, _(u"Tags"), choices=[_(u"Any tag"), _(u"All tags")], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.clearTagsBtn = wx.Button(self, -1, _(u"Clear all tags"))
        self.searchBtn = wx.Button(self, -1, _(u"Find"))
        self.resultWindow = getHtmlRender (self)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onClear, self.clearTagsBtn)
        self.Bind(wx.EVT_BUTTON, self.onFind, self.searchBtn)
        self.tagsList.Bind (EVT_TAG_LEFT_CLICK, self.__onTagLeftClick)


    def __onTagLeftClick (self, event):
        tag = event.text
        self.tagsList.mark (tag, not self.tagsList.isMarked(tag))


    def Print (self):
        self.resultWindow.Print()
    

    def Clear (self):
        pass


    def updatePageInfo (self):
        """
        Обновить интерфейс, чтобы он соответствовал настройкам страницы
        """
        assert self.page != None

        self.updateSearchPhrase()
        self.updateTagsList()
    

    def updateTagsList (self):
        """
        Обновить список тегов
        """
        assert self.page != None

        # заполним список тегов
        list_items = TagsList (Application.wikiroot)
        self.tagsList.setTags (list_items)

        tags = self.page.searchTags

        # Поставим галки, где нужно
        for tag in self._allTags:
            if tag in tags:
                self.tagsList.mark (tag)

        # Установим стратегию поиска по тегам
        strategyIndex = self._strategyList.index (self.page.strategy)

        self.tagsStrategy.SetSelection(strategyIndex)

        
    def updateSearchPhrase (self):
        self.wordsTextCtrl.SetValue (self.page.phrase)
    

    def Save (self):
        """
        Сохранить настройки страницы
        """
        if (self.page != None and 
                not self.page.isRemoved and
                pageExists (self.page) ):
            self._saveSearchPhrase()
            self._saveSearchTags()
            self._saveSearchTagsStrategy()
    

    def _saveSearchPhrase (self):
        """
        Сохранить искомую фразу в настройки страницы
        """
        self.page.phrase = self.wordsTextCtrl.GetValue()
    

    def _saveSearchTags (self):
        """
        Сохранить искомые теги в настройке страницы
        """
        self.page.searchTags = self._getSearchTags()
    

    def _saveSearchTagsStrategy (self):
        """
        Сохранить стратегию поиска по тегам (все теги или любой тег)
        """
        strategyIndex = self.tagsStrategy.GetSelection()
        self.page.strategy = self._strategyList[strategyIndex]


    def UpdateView (self, page):
        self.resultWindow.page = page
        self._allTags = TagsList (self.page.root)

        self.updatePageInfo()

        resultPages = self._loadResults ()
        self._showResults (resultPages)


    def __set_properties(self):
        self.tagsList.SetMinSize((250, 150))
        self.tagsStrategy.SetSelection(0)

    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(4, 1, 0, 0)
        tagsSizer = wx.FlexGridSizer(1, 3, 0, 0)
        rightSizer = wx.FlexGridSizer(2, 1, 0, 0)
        phraseSizer = wx.FlexGridSizer(1, 2, 0, 0)
        phraseSizer.Add(self.wordsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        phraseSizer.Add(self.wordsTextCtrl, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        phraseSizer.AddGrowableCol(1)
        mainSizer.Add(phraseSizer, 1, wx.EXPAND, 0)
        tagsSizer.Add(self.tagsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        tagsSizer.Add(self.tagsList, 0, wx.ALL|wx.EXPAND, 2)
        rightSizer.Add(self.tagsStrategy, 0, wx.EXPAND, 0)
        rightSizer.Add(self.clearTagsBtn, 0, wx.ALL|wx.EXPAND, 2)
        rightSizer.Add(self.searchBtn, 0, wx.ALL|wx.EXPAND, 2)
        rightSizer.AddGrowableRow(0)
        rightSizer.AddGrowableCol(0)
        tagsSizer.Add(rightSizer, 1, wx.EXPAND, 0)
        tagsSizer.AddGrowableCol(1)
        mainSizer.Add(tagsSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.resultWindow, 1, wx.EXPAND | wx.ALL, border=2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(2)
        mainSizer.AddGrowableCol(0)


    def onFind(self, event):
        assert self.page != None
        
        self.Save()

        phrase = self._getSearchPhrase()
        tags = self._getSearchTags()

        searcher = Searcher (phrase, tags, self.page.strategy)
        resultPages = searcher.find (self.page.root)

        self._saveResults (resultPages)
        self._showResults (resultPages)
    

    def _getSearchTags (self):
        """
        Получить список искомых тегов
        """
        tags = []

        for tag in self._allTags:
            if self.tagsList.isMarked (tag):
                tags.append (tag)

        return tags


    def _getSearchPhrase (self):
        """
        Получить искомую фразу
        """
        return self.wordsTextCtrl.GetValue ()
    

    def _showResults (self, resultPages):
        """
        Показать результат
        """
        report = HtmlReport (resultPages, self._getSearchPhrase(), self._getSearchTags())
        htmltext = report.generate ()
        self.resultWindow.SetPage (htmltext, self.page.path)
    

    def _saveResults (self, resultPages):
        assert self.page != None

        self.page.params.remove_section (self._resultsSection)

        for n in range (len (resultPages)):
            option = self._resultOptionTemplate % n
            self.page.params.set (self._resultsSection, option, resultPages[n].subpath)

    
    def _loadResults (self):
        assert self.page != None

        n = 0
        resultPages = []

        try:
            while True:
                option = self._resultOptionTemplate % n
                subpath = self.page.params.get (self._resultsSection, option)

                page = self.page.root[subpath]
                if page != None:
                    resultPages.append (page)

                n += 1
        except:
            pass

        return resultPages


    def onClear(self, event):
        self.tagsList.clearMarks()
