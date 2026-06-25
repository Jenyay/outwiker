# -*- coding: utf-8 -*-

from .defines import REGISTRY_PAGE_HASH
from .hashcalculator import BaseHashCalculator


class PageContentCache:
    """
    Class to check if an already created HTML file can be used
    for the wiki page or if it needs to be recreated
    """

    def __init__(self, page, hashCalculator: BaseHashCalculator, application):
        self._page = page
        self._application = application
        self._hashCalculator = hashCalculator

    def getHash(self, page) -> str:
        return self._hashCalculator.getHash(page)

    def canReadFromCache(self):
        """
        Can we read the ready HTML, or does it need to be recreated?
        """
        reg = self._page.root.registry.get_page_registry(self._page)
        try:
            old_hash = reg.getstr(REGISTRY_PAGE_HASH, default="")
        except KeyError:
            old_hash = ""

        return self.getHash(self._page) == old_hash

    def resetHash(self):
        self._setHash("")

    def _setHash(self, value):
        reg = self._page.root.registry.get_page_registry(self._page)
        try:
            reg.set(REGISTRY_PAGE_HASH, value)
        except KeyError:
            pass

    def saveHash(self):
        self._setHash(self.getHash(self._page))
