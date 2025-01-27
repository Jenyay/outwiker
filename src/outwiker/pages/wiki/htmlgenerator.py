# -*- coding: utf-8 -*-

from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.utilites.textfile import readTextFile
from outwiker.core.events import (
    PreprocessingParams,
    PreHtmlImprovingParams,
    PostprocessingParams,
)
from outwiker.gui.guiconfig import HtmlRenderConfig

from .parserfactory import ParserFactory
from .emptycontent import EmptyContent


class HtmlGenerator:
    """
    Class creates HTML file for wiki page taking into account caching
    """

    def __init__(self, page, application):
        self._page = page
        self._application = application

    def makeHtml(self, stylepath):
        # Get content
        content = (
            self._page.content
            if self._page.content
            else EmptyContent(self._application.config).content
        )

        content = self._changeContentByEvent(
            self._page, PreprocessingParams(content), self._application.onPreprocessing
        )

        # Create parser
        factory = ParserFactory()
        parser = factory.make(self._page, self._application)

        config = HtmlRenderConfig(self._application.config)

        # Parse wiki content
        html = parser.toHtml(content)
        if parser.footer:
            html += "\n" + parser.footer

        # Improve HTML
        html = self._changeContentByEvent(
            self._page,
            PreHtmlImprovingParams(html),
            self._application.onPreHtmlImproving,
        )

        improverFactory = HtmlImproverFactory(self._application)
        text = improverFactory[config.HTMLImprover.value].run(html)
        head = parser.head

        # Create final HTML file
        tpl = HtmlTemplate(self._application, readTextFile(stylepath))
        result = tpl.substitute(
            content=text, userhead=head, title=self._page.display_title
        )

        result = self._changeContentByEvent(
            self._page, PostprocessingParams(result), self._application.onPostprocessing
        )

        return result

    def _changeContentByEvent(self, page, params, event):
        event(page, params)
        return params.result
