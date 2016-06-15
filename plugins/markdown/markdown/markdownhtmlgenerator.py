# -*- coding: UTF-8 -*-

from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.utilites.textfile import readTextFile

from markdownparser.parser import Parser


class MarkdownHtmlGenerator (object):
    """
    Класс, который создает HTML для Markdown-страницы с учетом кэширования.
    """
    def __init__(self, page):
        self.page = page

    def makeHtml(self, stylepath):
        head = u""
        html = Parser().convert(self.page.content)
        tpl = HtmlTemplate(readTextFile(stylepath))
        result = tpl.substitute(content=html, userhead=head)
        return result
