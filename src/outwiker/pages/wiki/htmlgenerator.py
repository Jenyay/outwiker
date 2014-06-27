# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.config import StringOption
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.application import Application
from outwiker.core.system import readTextFile

from .parserfactory import ParserFactory
from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent
from .wikihashcalculator import WikiHashCalculator


class HtmlGenerator (object):
    """
    Класс, который создает HTML для вики-страницы с учетом кэширования.
    """
    def __init__ (self, page):
        self.page = page
        self.config = WikiConfig (Application.config)

        self.resultName = u"__content.html"
        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"


    def makeHtml (self, stylepath):
        path = self.getResultPath()

        if self.canReadFromCache():
            return readTextFile (path)

        factory = ParserFactory ()
        parser = factory.make(self.page, Application.config)

        content = self.page.content if len (self.page.content) > 0 else self._generateEmptyContent (parser)

        text = HtmlImprover.run (parser.toHtml (content))
        head = parser.head

        tpl = HtmlTemplate (readTextFile (stylepath))

        result = tpl.substitute (content=text, userhead=head)

        try:
            self._getHashOption().value = self.getHash()
        except IOError:
            # Не самая страшная потеря, если не сохранится хэш.
            # Максимум, что грозит пользователю, каждый раз генерить старницу
            pass

        return result


    def _generateEmptyContent (self, parser):
        content = EmptyContent (Application.config)
        return parser.toHtml (content.content)


    def getHash (self):
        hashcalculator = WikiHashCalculator (Application)
        return hashcalculator.getHash (self.page)


    def getResultPath (self):
        return os.path.join (self.page.path, self.resultName)


    def canReadFromCache (self):
        """
        Можно ли прочитать готовый HTML из кеша?
        """
        path = self.getResultPath()
        hash = self.getHash()
        hashoption = self._getHashOption()

        if os.path.exists (path) and (hash == hashoption.value or self.page.readonly):
            return True

        return False


    def resetHash (self):
        self._getHashOption().value = u""


    def _getHashOption (self):
        return StringOption (self.page.params,
                             self._configSection,
                             self._hashKey,
                             u"")
