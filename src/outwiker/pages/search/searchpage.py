# -*- coding: utf-8 -*-

from outwiker.core.tree import PageAdapter
from outwiker.core.search import AllTagsSearchStrategy, AnyTagSearchStrategy
from outwiker.core.system import getBuiltinImagePath
from outwiker.core.application import Application
from outwiker.core.factory import PageFactory
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.config import StringOption, IntegerOption
from outwiker.core.tagscommands import parseTagsList, getTagsString
from outwiker.core.events import PAGE_UPDATE_CONTENT
from outwiker.pages.search.defines import PAGE_TYPE_STRING

from .searchpanel import SearchPanel


class SearchPageAdapter(PageAdapter):
    """
    Класс HTML-страниц
    """

    def __init__(self, page):
        super().__init__(page)

        self.paramsSection = "Search"
        phraseOption = StringOption(self.params, self.paramsSection, "phrase", "")

        # Искомая фраза
        self._phrase = phraseOption.value

        # Теги, по которым осуществляется поиск
        # (не путать с тегами, установленными для данной страницы)
        self._searchTags = self._getSearchTags()

        # Стратегия для поиска
        self._strategy = self._getStrategy()

    @property
    def phrase(self):
        return self._phrase

    @phrase.setter
    def phrase(self, phrase):
        """
        Устанавливает искомую фразу
        """
        self._phrase = phrase

        phraseOption = StringOption(self.params, self.paramsSection, "phrase", "")
        try:
            phraseOption.value = phrase
        except ReadonlyException:
            # Ничего страшного, если поисковая фраза не сохранится
            pass

        Application.onPageUpdate(self.page, change=PAGE_UPDATE_CONTENT)

    def _getSearchTags(self):
        """
        Загрузить список тегов из настроек страницы
        """
        tagsOption = StringOption(self.params, self.paramsSection, "tags", "")
        tags = parseTagsList(tagsOption.value)
        return tags

    @property
    def searchTags(self):
        return self._searchTags

    @searchTags.setter
    def searchTags(self, tags):
        """
        Выбрать теги для поиска
        """
        self._searchTags = tags
        tags_str = getTagsString(tags)

        tagsOption = StringOption(self.params, self.paramsSection, "tags", "")

        try:
            tagsOption.value = tags_str
        except ReadonlyException:
            # Ну не сохранятся искомые теги, ничего страшного
            pass

        Application.onPageUpdate(self.page, change=PAGE_UPDATE_CONTENT)

    def _getStrategy(self):
        strategyOption = IntegerOption(self.params, self.paramsSection, "strategy", 0)
        return self._strategyByCode(strategyOption.value)

    def _strategyByCode(self, code):
        if code == 0:
            return AnyTagSearchStrategy
        else:
            return AllTagsSearchStrategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if strategy == AllTagsSearchStrategy:
            strategyCode = 1
        else:
            strategyCode = 0

        self._strategy = strategy
        strategyOption = IntegerOption(self.params, self.paramsSection, "strategy", 0)

        try:
            strategyOption.value = strategyCode
        except ReadonlyException:
            # Ничего страшного
            pass

        Application.onPageUpdate(self, change=PAGE_UPDATE_CONTENT)


class SearchPageFactory(PageFactory):
    """
    Фабрика для создания страниц поиска и их представлений
    """
    @property
    def title(self):
        """
        Название страницы, показываемое пользователю
        """
        return _("Search Page")

    def getPageTypeString(self):
        return PAGE_TYPE_STRING

    def getPageView(self, parent, application):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return SearchPanel(parent, application)

    def createPageAdapter(self, page):
        return SearchPageAdapter(page)


class GlobalSearch:
    @staticmethod
    def create(root, phrase="", tags=[], strategy=AllTagsSearchStrategy):
        """
        Создать страницу с поиском. Если страница существует,
        то сделать ее активной
        """
        searchAlias = _("# Search")
        page = None

        for child_page in root.children:
            if child_page.getTypeString() == PAGE_TYPE_STRING:
                page = child_page
                break

        factory = SearchPageFactory()
        if page is None:
            page = factory.create(root, searchAlias, [])
            page.icon = getBuiltinImagePath("global_search.svg")

        page_adapter = factory.createPageAdapter(page)
        page_adapter.phrase = phrase
        page_adapter.searchTags = [tag for tag in tags]
        page_adapter.strategy = strategy

        page.root.selectedPage = page
        return page
