# -*- coding: UTF-8 -*-

from outwiker.core.htmlimprover import BrHtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import readTextFile

from latex2html.parser import Parser


class LatexHtmlGenerator (object):
    """
    Класс, который создает HTML для викистраницы с учетом кэширования.
    """
    def __init__ (self, page):
        self.page = page


    def makeHtml (self, stylepath):
        parser = Parser()
        content = parser.convert (self.page.content)

        text = BrHtmlImprover().run (content)
        head = u""

        tpl = HtmlTemplate (readTextFile (stylepath))

        result = tpl.substitute (content=text, userhead=head)

        return result
