# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir
import outwiker.core.cssclasses as css


class ParserListTest (unittest.TestCase):
    def setUp(self):
        self._application = Application()
        self.encoding = "utf8"

        self.filesPath = "testdata/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        removeDir(self.path)

    def testUnorderList1(self):
        text = "бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUnorderClasses(self):
        unorderListCSS = [
            ('[]', css.CSS_LIST_ITEM_EMPTY),
            ('[ ]', css.CSS_LIST_ITEM_TODO),
            ('[/]', css.CSS_LIST_ITEM_INCOMPLETE),
            ('[\\]', css.CSS_LIST_ITEM_INCOMPLETE),
            ('[x]', css.CSS_LIST_ITEM_COMPLETE),
            ('[X]', css.CSS_LIST_ITEM_COMPLETE),
            ('[*]', css.CSS_LIST_ITEM_STAR),
            ('[+]', css.CSS_LIST_ITEM_PLUS),
            ('[-]', css.CSS_LIST_ITEM_MINUS),
            ('[o]', css.CSS_LIST_ITEM_CIRCLE),
            ('[O]', css.CSS_LIST_ITEM_CIRCLE),
            ('[v]', css.CSS_LIST_ITEM_CHECK),
            ('[V]', css.CSS_LIST_ITEM_CHECK),
            ('[<]', css.CSS_LIST_ITEM_LT),
            ('[>]', css.CSS_LIST_ITEM_GT),
            ]

        for prefix, other_css in unorderListCSS:
            text = f"бла-бла-бла \n\n* {prefix} Строка 1\nбла-бла-бла"
            result_expected = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI} {other_css}">Строка 1</li></ul>бла-бла-бла'

            result = self.parser.toHtml(text)
            self.assertEqual(result, result_expected, result)

    def testUnorderList2(self):
        text = "бла-бла-бла \n\n*'''Строка 1'''\n* ''Строка 2''\n* Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><b>Строка 1</b></li><li class="{css.CSS_WIKI}"><i>Строка 2</i></li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testUnorderList_multiline_no_spaces(self):
        text = '''бла-бла-бла

*[{Строка 1}]
*[{Строка 2}]
*[{Строка 3}]
бла-бла-бла'''

        result = f'''бла-бла-бла

<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testUnorderList_multiline_spaces(self):
        text = '''бла-бла-бла
* [{Строка 1}]
* [{Строка 2}]
* [{Строка 3}]
бла-бла-бла'''

        result = f'''бла-бла-бла
<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testUnorderMultilineList4(self):
        text = '''бла-бла-бла

* [{Строка 1


тест
}]
* [{блабла


''Строка 2''}]
* Строка 3
бла-бла-бла'''

        result = f'''бла-бла-бла

<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1


тест</li><li class="{css.CSS_WIKI}">блабла


<i>Строка 2</i></li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testUnorderList_multiline_format_01(self):
        text = '''бла-бла-бла
* [{''Строка 1''}]
* [{[[https://jenyay.net]]

{-Строка 2-}
}]
* [{Строка 3}]
бла-бла-бла'''

        result = f'''бла-бла-бла
<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><i>Строка 1</i></li><li class="{css.CSS_WIKI}"><a class="{css.CSS_WIKI}" href="https://jenyay.net">https://jenyay.net</a>

<strike>Строка 2</strike></li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testOrderList_multiline_spaces(self):
        text = '''бла-бла-бла
# [{Строка 1}]
# [{Строка 2}]
# [{Строка 3}]
бла-бла-бла'''

        result = f'''бла-бла-бла
<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testOrderMultilineList4(self):
        text = '''бла-бла-бла

# [{Строка 1


тест
}]
# [{блабла


''Строка 2''}]
# Строка 3
бла-бла-бла'''

        result = f'''бла-бла-бла

<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1


тест</li><li class="{css.CSS_WIKI}">блабла


<i>Строка 2</i></li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testOrderList_multiline_format_01(self):
        text = '''бла-бла-бла
# [{''Строка 1''}]
# [{[[https://jenyay.net]]

{-Строка 2-}
}]
# [{Строка 3}]
бла-бла-бла'''

        result = f'''бла-бла-бла
<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><i>Строка 1</i></li><li class="{css.CSS_WIKI}"><a class="{css.CSS_WIKI}" href="https://jenyay.net">https://jenyay.net</a>

<strike>Строка 2</strike></li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'''

        self.assertEqual(self.parser.toHtml(text), result)

    def testUnorderListStrike(self):
        text = '''бла-бла-бла
*{-Строка 1-}
* {-Строка 2-}
* Строка 3
бла-бла-бла'''
        result = f'''бла-бла-бла
<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><strike>Строка 1</strike></li><li class="{css.CSS_WIKI}"><strike>Строка 2</strike></li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'''

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testOrderList1(self):
        text = "бла-бла-бла \n\n#Строка 1\n# Строка 2\n# Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testOrderList2(self):
        text = "бла-бла-бла \n\n#'''Строка 1'''\n# ''Строка 2''\n# Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><b>Строка 1</b></li><li class="{css.CSS_WIKI}"><i>Строка 2</i></li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testOrderListStrike(self):
        text = "бла-бла-бла \n\n#{-Строка 1-}\n# {-Строка 2-}\n# Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}"><strike>Строка 1</strike></li><li class="{css.CSS_WIKI}"><strike>Строка 2</strike></li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testEnclosureUnorderList1(self):
        text = "бла-бла-бла \n\n*Строка 1\n* Строка 2\n** Вложенная строка 1\n**Вложенная строка 2\n* Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенная строка 1</li><li class="{css.CSS_WIKI}">Вложенная строка 2</li></ul><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testEnclosureOrderList1(self):
        text = "бла-бла-бла \n\n#Строка 1\n# Строка 2\n## Вложенная строка 1\n##Вложенная строка 2\n# Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенная строка 1</li><li class="{css.CSS_WIKI}">Вложенная строка 2</li></ol><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testEnclosureList1(self):
        text = """* Несортированный список. Элемент 1
* Несортированный список. Элемент 2
* Несортированный список. Элемент 3
## Вложенный сортированный список. Элемент 1
## Вложенный сортированный список. Элемент 2
## Вложенный сортированный список. Элемент 3
## Вложенный сортированный список. Элемент 4
*** Совсем вложенный сортированный список. Элемент 1
*** Совсем вложенный сортированный список. Элемент 2
## Вложенный сортированный список. Элемент 5
** Вложенный несортированный список. Элемент 1"""

        result = f'<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Несортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 3</li><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 3</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 4</li><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 2</li></ul><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 5</li></ol><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testEnclosureList2(self):
        text = """* Строка 1
* Строка 2
** Строка 3
# Строка 4
# Строка 5
# Строка 6
# Строка 7"""

        result = f'<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ul></ul><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 4</li><li class="{css.CSS_WIKI}">Строка 5</li><li class="{css.CSS_WIKI}">Строка 6</li><li class="{css.CSS_WIKI}">Строка 7</li></ol>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testManyUnorderList1(self):
        text = """бла-бла-бла

*Строка 1
* Строка 2


* Строка 3

бла-бла-бла"""
        result = f"""бла-бла-бла

<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li></ul>\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла"""

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text))

    def testManyOrderList1(self):
        text = """бла-бла-бла

#Строка 1
# Строка 2


# Строка 3

бла-бла-бла"""
        result = f"""бла-бла-бла

<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li></ol>\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла"""

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text))

    def testManyUnorderList2(self):
        text = "бла-бла-бла \n\n*Строка 1\n\n* Строка 2\n\n\n** Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li></ul>\n<ul class="{css.CSS_WIKI}"><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ul></ul>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testManyOrderList2(self):
        text = "бла-бла-бла \n\n#Строка 1\n\n# Строка 2\n\n\n## Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li></ol>\n<ol class="{css.CSS_WIKI}"><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ol></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testManyList1(self):
        text = "бла-бла-бла \n\n#Строка 1\n\n# Строка 2\n\n\n** Строка 3\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li></ol>\n<ul class="{css.CSS_WIKI}"><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 3</li></ul></ul>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result)

    def testSpaces1(self):
        text = "бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testSpaces2(self):
        text = "бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\n\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testSpaces3(self):
        text = "бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\n\n\nбла-бла-бла"
        result = f'бла-бла-бла \n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testLineJoin1(self):
        text = """бла-бла-бла

* Строка 1 \\
вторая строка
* Строка 2
* Строка 3
бла-бла-бла"""
        result = f'бла-бла-бла\n\n<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1 вторая строка</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ul>бла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLineJoin2(self):
        text = """бла-бла-бла

# Строка 1 \\
вторая строка
# Строка 2
# Строка 3
бла-бла-бла"""
        result = f'бла-бла-бла\n\n<ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Строка 1 вторая строка</li><li class="{css.CSS_WIKI}">Строка 2</li><li class="{css.CSS_WIKI}">Строка 3</li></ol>бла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testLineJoin3(self):
        text = """* Несортированный список. Элемент 1
* Несортированный список. \\
Элемент 2
* Несортированный список. Элемент 3
## Вложенный сортированный список. \\
Элемент 1
## Вложенный сортированный список. Элемент 2
## Вложенный сортированный список. \\
Элемент 3
## Вложенный сортированный список. Элемент 4
*** Совсем вложенный сортированный список. \\
Элемент 1
*** Совсем вложенный сортированный список. \\
Элемент 2
## Вложенный сортированный список. Элемент 5
** Вложенный несортированный список. Элемент 1"""

        result = f'<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Несортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 3</li><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 3</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 4</li><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 2</li></ul><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 5</li></ol><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testLineJoin4(self):
        text = """* Несортированный список. Элемент 1
* Несортированный список. \\
Элемент 2
* Несортированный список. Элемент 3
## Вложенный сортированный список. \\
\\
Элемент 1
## Вложенный сортированный список. Элемент 2
## Вложенный сортированный список. \\
\\
Элемент 3
## Вложенный сортированный список. Элемент 4
*** Совсем вложенный сортированный список. \\
Элемент 1
*** Совсем вложенный сортированный список. \\
\\
\\
\\
Элемент 2
## Вложенный сортированный список. Элемент 5
** Вложенный несортированный список. Элемент 1"""

        result = f'<ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Несортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Несортированный список. Элемент 3</li><ol class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 2</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 3</li><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 4</li><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 1</li><li class="{css.CSS_WIKI}">Совсем вложенный сортированный список. Элемент 2</li></ul><li class="{css.CSS_WIKI}">Вложенный сортированный список. Элемент 5</li></ol><ul class="{css.CSS_WIKI}"><li class="{css.CSS_WIKI}">Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))
