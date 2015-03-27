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
        content = self.page.content if self.page.content else EmptyContent (Application.config).content
        content = self._runPreprocessing (content)

        factory = ParserFactory ()
        parser = factory.make(self.page, Application.config)

        config = HtmlRenderConfig (Application.config)

        html = parser.toHtml (content)

        improverFactory = HtmlImproverFactory (Application)
        text = improverFactory[config.HTMLImprover.value].run (html)
        head = parser.head

        tpl = HtmlTemplate (readTextFile (stylepath))

        result = tpl.substitute (content=text, userhead=head)

        return result


    def _runPreprocessing (self, content):
        """
        Запускает препроцессинг
        """
        # Дадим возможность изменить результат в препроцессинге
        result = [content]
        Application.onPreprocessing (self.page, result)
        return result[0]
