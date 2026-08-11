# -*- coding: utf-8 -*-

from typing import List

from outwiker.core.application import Application
from outwiker.core.hashcalculator import SimpleHashCalculator
from outwiker.core.style import Style
from outwiker.core.tree import WikiPage
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.utilites.textfile import readTextFile


class HtmlHashCalculator(SimpleHashCalculator):
    def __init__(self, application: Application):
        super().__init__(application)
        self._htmlConfig = HtmlRenderConfig(application.config)
        self.addContentFunction(self._getHtmlSettingsContent)
        self.addContentFunction(self._getStyleContent)

    def _getHtmlSettingsContent(self, page: WikiPage, content: List[str]) -> None:
        content.append(str(self._htmlConfig.fontSize.value))
        content.append(str(self._htmlConfig.fontName.value))
        content.append(str(self._htmlConfig.userStyle.value))
        content.append(str(self._htmlConfig.HTMLImprover.value))

    def _getStyleContent(self, page: WikiPage, content: List[str]) -> None:
        """
        Returns the template content
        """
        try:
            content.append(readTextFile(Style().getPageStyle(page)))
        except (IOError, UnicodeDecodeError):
            pass
