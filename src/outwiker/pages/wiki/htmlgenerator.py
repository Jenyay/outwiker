# -*- coding: UTF-8 -*-

from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.application import Application
from outwiker.utilites.textfile import readTextFile
from outwiker.core.events import (PreprocessingParams,
                                  PreHtmlImprovingParams,
                                  PostprocessingParams
                                  )
from outwiker.gui.guiconfig import HtmlRenderConfig

from .parserfactory import ParserFactory
from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent


class HtmlGenerator(object):
    """
    Class creates HTML file for wiki page taking into account caching
    """
    def __init__(self, page):
        self.page = page
        self.config = WikiConfig(Application.config)

    def makeHtml(self, stylepath):
        # Get content
        content = (self.page.content
                   if self.page.content
                   else EmptyContent(Application.config).content)

        content = self._changeContentByEvent(self.page,
                                             PreprocessingParams(content),
                                             Application.onPreprocessing)

        # Create parser
        factory = ParserFactory()
        parser = factory.make(self.page, Application.config)

        config = HtmlRenderConfig(Application.config)

        # Parse wiki content
        html = parser.toHtml(content)
        if parser.footer:
            html += u'\n' + parser.footer

        # Improve HTML
        html = self._changeContentByEvent(self.page,
                                          PreHtmlImprovingParams(html),
                                          Application.onPreHtmlImproving)

        improverFactory = HtmlImproverFactory(Application)
        text = improverFactory[config.HTMLImprover.value].run(html)
        head = parser.head

        # Create final HTML file
        tpl = HtmlTemplate(readTextFile(stylepath))
        result = tpl.substitute(content=text,
                                userhead=head,
                                title=self.page.display_title)

        result = self._changeContentByEvent(self.page,
                                            PostprocessingParams(result),
                                            Application.onPostprocessing)

        return result

    def _changeContentByEvent(self, page, params, event):
        event(page, params)
        return params.result
