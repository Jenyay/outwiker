# -*- coding: utf-8 -*-

from outwiker.core.pagecontentcache import PageContentCache
from .hashcalculator import WikiHashCalculator


class HtmlCache:
    """
    Класс для проверки того, можно ли использовать уже созданный HTML-файл
    для викистраницы или надо его создавать заново
    """

    def __init__(self, page, application):
        hashCalculator = WikiHashCalculator(application)
        self._pageContentCache = PageContentCache(page, hashCalculator, application)

    def getHash(self, page) -> str:
        return self._pageContentCache.getHash(page)

    def canReadFromCache(self):
        """
        Можно ли прочитать готовый HTML, или его надо создавать заново?
        """
        return self._pageContentCache.canReadFromCache()

    def resetHash(self):
        self._pageContentCache.resetHash()

    def saveHash(self):
        self._pageContentCache.saveHash()
