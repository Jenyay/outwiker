# -*- coding: utf-8 -*-

from typing import List

from outwiker.pages.html.hashcalculator import HtmlHashCalculator

from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent


class WikiHashCalculator(HtmlHashCalculator):
    """
    Класс для расчета контрольной суммы викистраницы
    """

    def __init__(self, application):
        super().__init__(application)
        self._wikiConfig = WikiConfig(application.config)

    def getFullContent(self, page) -> List[str]:
        """
        Получить контент для расчета контрольной суммы, по которой определяется,
        нужно ли обновлять страницу
        """
        # Здесь накапливаем список интересующих строк (по которым определяем
        # изменилась страница или нет)
        # Заголовок страницы
        items: List[str] = []

        self._getPageTitleContent(page, items)
        self._getPageContent(page, items)
        self._getDirContent(page, items)
        self._getPluginsListContent(items)
        self._getPageChildrenContent(page, items)
        self._getStyleContent(page, items)
        self._getWikiSettingsContent(items)
        self._getHtmlSettingsContent(items)
        self._getEmptyContent(page, items)
        return items

    def _getEmptyContent(self, page, content: List[str]) -> None:
        if len(page.content) == 0:
            # Если страница пустая, то проверим настройку, отвечающую за шаблон
            # пустой страницы
            emptycontent = EmptyContent(self.application.config)
            return content.append(str(emptycontent.content))

    def _getWikiSettingsContent(self, content: List[str]) -> None:
        content.append(str(self._wikiConfig.showAttachInsteadBlankOptions.value))
        content.append(str(self._wikiConfig.thumbSizeOptions.value))
