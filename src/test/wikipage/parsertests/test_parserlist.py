# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserListTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testUnorderList1 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUnorderList2 (self):
        text = u"бла-бла-бла \n\n*'''Строка 1'''\n* ''Строка 2''\n* Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li><b>Строка 1</b></li><li><i>Строка 2</i></li><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUnorderListStrike (self):
        text = u"бла-бла-бла \n\n*{-Строка 1-}\n* {-Строка 2-}\n* Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li><strike>Строка 1</strike></li><li><strike>Строка 2</strike></li><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testOrderList1 (self):
        text = u"бла-бла-бла \n\n#Строка 1\n# Строка 2\n# Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li>Строка 1</li><li>Строка 2</li><li>Строка 3</li></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testOrderList2 (self):
        text = u"бла-бла-бла \n\n#'''Строка 1'''\n# ''Строка 2''\n# Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li><b>Строка 1</b></li><li><i>Строка 2</i></li><li>Строка 3</li></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testOrderListStrike (self):
        text = u"бла-бла-бла \n\n#{-Строка 1-}\n# {-Строка 2-}\n# Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li><strike>Строка 1</strike></li><li><strike>Строка 2</strike></li><li>Строка 3</li></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testEnclosureUnorderList1 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n** Вложенная строка 1\n**Вложенная строка 2\n* Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li><ul><li>Вложенная строка 1</li><li>Вложенная строка 2</li></ul><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testEnclosureOrderList1 (self):
        text = u"бла-бла-бла \n\n#Строка 1\n# Строка 2\n## Вложенная строка 1\n##Вложенная строка 2\n# Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li>Строка 1</li><li>Строка 2</li><ol><li>Вложенная строка 1</li><li>Вложенная строка 2</li></ol><li>Строка 3</li></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testEnclosureList1 (self):
        text = u"""* Несортированный список. Элемент 1
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

        result = u'<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testEnclosureList2 (self):
        text = u"""* Строка 1
* Строка 2
** Строка 3
# Строка 4
# Строка 5
# Строка 6
# Строка 7"""

        result = u'<ul><li>Строка 1</li><li>Строка 2</li><ul><li>Строка 3</li></ul></ul><ol><li>Строка 4</li><li>Строка 5</li><li>Строка 6</li><li>Строка 7</li></ol>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testManyUnorderList1 (self):
        text = u"""бла-бла-бла

*Строка 1
* Строка 2


* Строка 3

бла-бла-бла"""
        result = u"""бла-бла-бла

<ul><li>Строка 1</li><li>Строка 2</li></ul>\n<ul><li>Строка 3</li></ul>бла-бла-бла"""

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text))



    def testManyOrderList1 (self):
        text = u"""бла-бла-бла

#Строка 1
# Строка 2


# Строка 3

бла-бла-бла"""
        result = u"""бла-бла-бла

<ol><li>Строка 1</li><li>Строка 2</li></ol>\n<ol><li>Строка 3</li></ol>бла-бла-бла"""

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text))


    def testManyUnorderList2 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n\n* Строка 2\n\n\n** Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li></ul>\n<ul><ul><li>Строка 3</li></ul></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testManyOrderList2 (self):
        text = u"бла-бла-бла \n\n#Строка 1\n\n# Строка 2\n\n\n## Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li>Строка 1</li><li>Строка 2</li></ol>\n<ol><ol><li>Строка 3</li></ol></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testManyList1 (self):
        text = u"бла-бла-бла \n\n#Строка 1\n\n# Строка 2\n\n\n** Строка 3\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ol><li>Строка 1</li><li>Строка 2</li></ol>\n<ul><ul><li>Строка 3</li></ul></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSpaces1 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSpaces2 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\n\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li><li>Строка 3</li></ul>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSpaces3 (self):
        text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\n\n\n\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<ul><li>Строка 1</li><li>Строка 2</li><li>Строка 3</li></ul>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin1 (self):
        text = u"""бла-бла-бла

* Строка 1 \\
вторая строка
* Строка 2
* Строка 3
бла-бла-бла"""
        result = u'бла-бла-бла\n\n<ul><li>Строка 1 вторая строка</li><li>Строка 2</li><li>Строка 3</li></ul>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result)


    def testLineJoin2 (self):
        text = u"""бла-бла-бла

# Строка 1 \\
вторая строка
# Строка 2
# Строка 3
бла-бла-бла"""
        result = u'бла-бла-бла\n\n<ol><li>Строка 1 вторая строка</li><li>Строка 2</li><li>Строка 3</li></ol>бла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin3 (self):
        text = u"""* Несортированный список. Элемент 1
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

        result = u'<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin4 (self):
        text = u"""* Несортированный список. Элемент 1
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

        result = u'<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
