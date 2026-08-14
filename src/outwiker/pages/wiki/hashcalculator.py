# -*- coding: utf-8 -*-

from typing import List

from outwiker.core.application import Application
from outwiker.core.tree import WikiPage
from outwiker.pages.html.hashcalculator import HtmlHashCalculator

from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent


class WikiHashCalculator(HtmlHashCalculator):
    """
    Class for calculating the checksum of a wiki page
    """

    def __init__(self, application: Application):
        super().__init__(application)
        self._wikiConfig = WikiConfig(application.config)
        self.addContentFunction(self._getWikiSettingsContent)
        self.addContentFunction(self._getEmptyContent)

    def _getWikiSettingsContent(self, page: WikiPage, content: List[str]) -> None:
        content.append(str(self._wikiConfig.showAttachInsteadBlankOptions.value))
        content.append(str(self._wikiConfig.thumbSizeOptions.value))

    def _getEmptyContent(self, page: WikiPage, content: List[str]) -> None:
        if len(page.content) == 0:
            # If the page is empty, check the setting responsible for the
            # empty page template
            emptycontent = EmptyContent(self.application.config)
            return content.append(str(emptycontent.content))
