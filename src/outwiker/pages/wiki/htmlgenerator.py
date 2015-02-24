# -*- coding: UTF-8 -*-

from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.application import Application
from outwiker.core.system import readTextFile
from outwiker.gui.guiconfig import HtmlRenderConfig

from .parserfactory import ParserFactory
from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent


class HtmlGenerator (object):
    """
    Класс, который создает HTML для вики-страницы с учетом кэширования.
    """
    def __init__ (self, page):
        self.page = page
        self.config = WikiConfig (Application.config)


    def makeHtml (self, stylepath):
        factory = ParserFactory ()
        parser = factory.make(self.page, Application.config)

        content = self.page.content if len (self.page.content) > 0 else self._generateEmptyContent (parser)

        content = self._runPreprocessing (content)

        config = HtmlRenderConfig (Application.config)
        improverFactory = HtmlImproverFactory (Application)
        text = improverFactory[config.HTMLImprover.value].run (parser.toHtml (content))
        head = parser.head

        tpl = HtmlTemplate (readTextFile (stylepath))

        result = tpl.substitute (content=text, userhead=head)

        return result


    def _generateEmptyContent (self, parser):
        content = EmptyContent (Application.config)
        return parser.toHtml (content.content)


    def _runPreprocessing (self, content):
        """
        Запускает препроцессинг
        """
        # Дадим возможность изменить результат в построцессинге
        result = [content]
        Application.onPreprocessing (self.page, result)
        return result[0]
