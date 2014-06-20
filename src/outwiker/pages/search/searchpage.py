# -*- coding: UTF-8 -*-
import os.path

from outwiker.core.tree import WikiPage
from outwiker.core.search import AllTagsSearchStrategy, AnyTagSearchStrategy
from outwiker.core.system import getImagesDir
from outwiker.core.application import Application
from outwiker.core.factory import PageFactory
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.config import StringOption, IntegerOption
from outwiker.core.tagscommands import parseTagsList, getTagsString
from outwiker.core.events import PAGE_UPDATE_CONTENT

from .searchpanel import SearchPanel


class SearchWikiPage (WikiPage):
    """
    Класс HTML-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)

        self.paramsSection = u"Search"
        phraseOption = StringOption (self.params, self.paramsSection, u"phrase", u"")

        # Искомая фраза
        self._phrase = phraseOption.value

        # Теги, по которым осуществляется поиск (не путать с тегами, установленными для данной страницы)
        self._searchTags = self._getSearchTags()

        # Стратегия для поиска
        self._strategy = self._getStrategy()


    @staticmethod
    def getTypeString ():
        return u"search"


    @property
    def phrase (self):
        return self._phrase


    @phrase.setter
    def phrase (self, phrase):
        """
        Устанавливает искомую фразу
        """
        self._phrase = phrase

        phraseOption = StringOption (self.params, self.paramsSection, u"phrase", u"")
        try:
            phraseOption.value = phrase
        except ReadonlyException:
            # Ничего страшного, если поисковая фраза не сохранится
            pass

        Application.onPageUpdate (self, change=PAGE_UPDATE_CONTENT)


    def _getSearchTags (self):
        """
        Загрузить список тегов из настроек страницы
        """
        tagsOption = StringOption (self.params, self.paramsSection, u"tags", u"")
        tags = parseTagsList (tagsOption.value)
        return tags


    @property
    def searchTags (self):
        return self._searchTags


    @searchTags.setter
    def searchTags (self, tags):
        """
        Выбрать теги для поиска
        """
        self._searchTags = tags
        tags_str = getTagsString (tags)

        tagsOption = StringOption (self.params, self.paramsSection, u"tags", u"")

        try:
            tagsOption.value = tags_str
        except ReadonlyException:
            # Ну не сохранятся искомые теги, ничего страшного
            pass

        Application.onPageUpdate (self, change=PAGE_UPDATE_CONTENT)


    def _getStrategy (self):
        strategyOption = IntegerOption (self.params, self.paramsSection, u"strategy", 0)
        return self._strategyByCode (strategyOption.value)


    def _strategyByCode (self, code):
        if code == 0:
            return AnyTagSearchStrategy
        else:
            return AllTagsSearchStrategy


    @property
    def strategy (self):
        return self._strategy


    @strategy.setter
    def strategy (self, strategy):
        if strategy == AllTagsSearchStrategy:
            strategyCode = 1
        else:
            strategyCode = 0

        self._strategy = strategy
        strategyOption = IntegerOption (self.params, self.paramsSection, u"strategy", 0)

        try:
            strategyOption.value = strategyCode
        except ReadonlyException:
            # Ничего страшного
            pass

        Application.onPageUpdate (self, change=PAGE_UPDATE_CONTENT)


class SearchPageFactory (PageFactory):
    """
    Фабрика для создания страниц поиска и их представлений
    """
    def getPageType(self):
        return SearchWikiPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Search Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return SearchPanel (parent)


    def getPrefPanels (self, parent):
        return []



class GlobalSearch (object):
    pageTitle = _(u"# Search")

    @staticmethod
    def create (root, phrase = u"", tags = [], strategy = AllTagsSearchStrategy):
        """
        Создать страницу с поиском. Если страница существует, то сделать ее активной
        """
        title = GlobalSearch.pageTitle
        number = 1
        page = None

        imagesDir = getImagesDir()

        while page is None:
            page = root[title]
            if page is None:
                page = SearchPageFactory().create (root, title, [])
                page.icon = os.path.join (imagesDir, "global_search.png")
            elif page.getTypeString() != SearchWikiPage.getTypeString():
                number += 1
                title = u"%s %d" % (GlobalSearch.pageTitle, number)
                page = None

        page.phrase = phrase
        page.searchTags = [tag for tag in tags]
        page.strategy = strategy

        page.root.selectedPage = page

        return page
