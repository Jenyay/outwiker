# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption

from .wikihashcalculator import WikiHashCalculator


class HtmlCache (object):
    """
    Класс для проверки того, можно ли использовать уже созданный HTML-файл для викистраницы или надо его создавать заново
    """
    def __init__ (self, page, application):
        self._page = page
        self._application = application

        self._hashKey = u"md5_hash"
        self._configSection = u"wiki"


    def getHash (self, page):
        return WikiHashCalculator (self._application).getHash (page)


    def canReadFromCache (self):
        """
        Можно ли прочитать готовый HTML, или его надо создавать заново?
        """
        hashoption = self._getHashOption()

        if self.getHash (self._page) == hashoption.value or self._page.readonly:
            return True

        return False


    def resetHash (self):
        self._getHashOption().value = u""


    def _getHashOption (self):
        return StringOption (self._page.params,
                             self._configSection,
                             self._hashKey,
                             u"")


    def saveHash (self):
        try:
            self._getHashOption().value = self.getHash (self._page)
        except IOError:
            # Не самая страшная потеря, если не сохранится хэш.
            # Максимум, что грозит пользователю, каждый раз генерить старницу
            pass
