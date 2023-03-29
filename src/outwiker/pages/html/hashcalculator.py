# -*- coding: utf-8 -*-

from typing import List

from outwiker.core.hashcalculator import SimpleHashCalculator
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.utilites.textfile import readTextFile


class HtmlHashCalculator(SimpleHashCalculator):
    def __init__(self, application):
        super().__init__(application)
        self._htmlConfig = HtmlRenderConfig(application.config)

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
        self._getHtmlSettingsContent(items)
        return items

    def _getHtmlSettingsContent(self, content: List[str]) -> None:
        content.append(str(self._htmlConfig.fontSize.value))
        content.append(str(self._htmlConfig.fontName.value))
        content.append(str(self._htmlConfig.userStyle.value))
        content.append(str(self._htmlConfig.HTMLImprover.value))

    def _getStyleContent(self, page, content: List[str]) -> None:
        """
        Возвращает содержимое шаблона
        """
        try:
            content.append(readTextFile(Style().getPageStyle(page)))
        except (IOError, UnicodeDecodeError):
            pass
