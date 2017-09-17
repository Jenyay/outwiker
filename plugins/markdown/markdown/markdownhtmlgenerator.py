# -*- coding: UTF-8 -*-

import outwiker.core
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.utilites.textfile import readTextFile
from outwiker.core.version import Version

from markdownparser.parser import Parser


class MarkdownHtmlGenerator (object):
    """
    Class to convert Markdown to HTML code.
    """
    def __init__(self, page):
        self.page = page

    def makeHtml(self, stylepath):
        parser = Parser()
        css = parser.getCSS()
        head = u'<style>\n{}\n</style>'.format(css)

        html = parser.convert(self.page.content)
        tpl = HtmlTemplate(readTextFile(stylepath))
        if Version(*outwiker.core.__version__) >= Version(1, 5):
            result = tpl.substitute(content=html,
                                    userhead=head,
                                    title=self.page.display_title)
        else:
            result = tpl.substitute(content=html, userhead=head)
        return result
