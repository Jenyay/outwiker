# -*- coding: utf-8 -*-

from .defines import REGISTRY_PAGE_HASH
from .wikihashcalculator import WikiHashCalculator


class HtmlCache (object):
    """
    Класс для проверки того, можно ли использовать уже созданный HTML-файл
    для викистраницы или надо его создавать заново
    """

    def __init__(self, page, application):
        self._page = page
        self._application = application

        self._configSection = u"wiki"

    def getHash(self, page):
        return WikiHashCalculator(self._application).getHash(page)

    def canReadFromCache(self):
        """
        Можно ли прочитать готовый HTML, или его надо создавать заново?
        """
        reg = self._page.root.registry.get_page_registry(self._page)
        try:
            old_hash = reg.getstr(REGISTRY_PAGE_HASH, default='')
        except KeyError:
            old_hash = ''

        return (self.getHash(self._page) == old_hash)

    def resetHash(self):
        self._setHash('')

    def _setHash(self, value):
        reg = self._page.root.registry.get_page_registry(self._page)
        try:
            reg.set(REGISTRY_PAGE_HASH, value)
        except KeyError:
            pass

    def saveHash(self):
        self._setHash(self.getHash(self._page))
