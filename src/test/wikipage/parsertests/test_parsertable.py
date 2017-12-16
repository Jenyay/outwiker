# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserTableTest (unittest.TestCase):

    def setUp(self):
        self.encoding = "utf8"
        self.filesPath = "../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testTable1 (self):
        text = """бла-бла-бла
|| border=1
|| Ячейка 1 ||Ячейка 2 || Ячейка 3||
||Ячейка 4||Ячейка 5||Ячейка 6||
"""

        result = '''бла-бла-бла
<table border=1><tr><td align="center">Ячейка 1</td><td align="left">Ячейка 2</td><td align="right">Ячейка 3</td></tr><tr><td>Ячейка 4</td><td>Ячейка 5</td><td>Ячейка 6</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable2 (self):
        text = """|| border=1
|| '''Синтаксис''' || '''Результат''' || '''Комментарий''' ||
||[@http://example.com@]||http://example.com||Ссылка на адрес в интернете||
||[@[[http://example.com]]@]||[[http://example.com]]||Ссылка на адрес в интернете||
||[@[[Пример ссылки -> http://example.com]]@]||[[Пример ссылки -> http://example.com]]||Ссылка на адрес в интернете с заданным текстом||
||[@[[http://example.com | Пример ссылки]]@]||[[http://example.com | Пример ссылки]]||Ссылка на адрес в интернете с заданным текстом||
"""

        result = '''<table border=1><tr><td align="center"><b>Синтаксис</b></td><td align="center"><b>Результат</b></td><td align="center"><b>Комментарий</b></td></tr><tr><td><pre>http://example.com</pre></td><td><a href="http://example.com">http://example.com</a></td><td>Ссылка на адрес в интернете</td></tr><tr><td><pre>[[http://example.com]]</pre></td><td><a href="http://example.com">http://example.com</a></td><td>Ссылка на адрес в интернете</td></tr><tr><td><pre>[[Пример ссылки -&gt; http://example.com]]</pre></td><td><a href="http://example.com">Пример ссылки</a></td><td>Ссылка на адрес в интернете с заданным текстом</td></tr><tr><td><pre>[[http://example.com | Пример ссылки]]</pre></td><td><a href="http://example.com">Пример ссылки</a></td><td>Ссылка на адрес в интернете с заданным текстом</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable3 (self):
        text = """||border=1 width=350
||left aligned \\
sdfsdf || centered || right aligned||
||left aligned [[<<]] dsfsdf || centered || right aligned||
||left aligned [[&lt;&lt;]] dsfsdf || centered || right aligned||
||left aligned [[<<]][[<<]] sdfsdfsdf || centered || right aligned||
"""

        result = '''<table border=1 width=350><tr><td align="left">left aligned sdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/><br/> sdfsdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable4 (self):
        text = """||border=1 width=350
||left aligned \\
sdfsdf || centered || right aligned||
||left aligned [[<<]] dsfsdf || centered || right aligned||
||left aligned [[&lt;&lt;]] dsfsdf || centered || right aligned||
||left aligned [[<<]][[<<]] sdfsdfsdf || centered || right aligned||

Бла-бла-бла

||border=1 width=350
||left aligned \\
sdfsdf || centered || right aligned||
||left aligned [[<<]] dsfsdf || centered || right aligned||
||left aligned [[&lt;&lt;]] dsfsdf || centered || right aligned||
||left aligned [[<<]][[<<]] sdfsdfsdf || centered || right aligned||
"""

        result = '''<table border=1 width=350><tr><td align="left">left aligned sdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/><br/> sdfsdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr></table>
Бла-бла-бла

<table border=1 width=350><tr><td align="left">left aligned sdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/> dsfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr><tr><td align="left">left aligned <br/><br/> sdfsdfsdf</td><td align="center">centered</td><td align="right">right aligned</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable5 (self):
        text = """||border=1
||x01\\
||"""

        result = '''<table border=1><tr><td>x01</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable6 (self):
        text = """||border=1
||x01\\
    ||"""

        result = '''<table border=1><tr><td>x01</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable7 (self):
        """
        Этот пример отличается от предыдущего хитрыми юникодными пробелами в таблице
        """
        text = """||border=1
||x01\\
    ||"""

        result = '''<table border=1><tr><td>x01</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable8 (self):
        text = """||border=1
||x01\\
    \\
    \\
    ||"""

        result = '''<table border=1><tr><td>x01</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTable9 (self):
        text = """бла-бла-бла
|| border=1
|| Ячейка 1 ||Ячейка 2 || Ячейка 3||
||Ячейка 4||\\t||Ячейка 6||
"""

        result = '''бла-бла-бла
<table border=1><tr><td align="center">Ячейка 1</td><td align="left">Ячейка 2</td><td align="right">Ячейка 3</td></tr><tr><td>Ячейка 4</td><td>\\t</td><td>Ячейка 6</td></tr></table>'''

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testTableQuote (self):
        text = """бла-бла-бла
|| border=1
|| Ячейка 1 ||Ячейка 2 || Ячейка 3||
||Ячейка 4||[>Ячейка 5<]||Ячейка 6||
"""

        result = '''бла-бла-бла
<table border=1><tr><td align="center">Ячейка 1</td><td align="left">Ячейка 2</td><td align="right">Ячейка 3</td></tr><tr><td>Ячейка 4</td><td><blockquote>Ячейка 5</blockquote></td><td>Ячейка 6</td></tr></table>'''

        self.assertEqual(self.parser.toHtml(text), result,
                         self.parser.toHtml(text).encode(self.encoding))
