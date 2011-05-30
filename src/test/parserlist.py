#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from utils import removeWiki

from core.tree import WikiDocument
from core.application import Application

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory


class ParserListTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"

		self.__createWiki()
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)
		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		self.testPage = self.rootwiki[u"Страница 2"]
		

	def tearDown(self):
		removeWiki (self.path)
	

	def testUnorderList1 (self):
		text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n* Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<UL><LI>Строка 1</LI><LI>Строка 2</LI><LI>Строка 3</LI></UL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUnorderList2 (self):
		text = u"бла-бла-бла \n\n*'''Строка 1'''\n* ''Строка 2''\n* Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<UL><LI><B>Строка 1</B></LI><LI><I>Строка 2</I></LI><LI>Строка 3</LI></UL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUnorderListStrike (self):
		text = u"бла-бла-бла \n\n*{-Строка 1-}\n* {-Строка 2-}\n* Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<UL><LI><STRIKE>Строка 1</STRIKE></LI><LI><STRIKE>Строка 2</STRIKE></LI><LI>Строка 3</LI></UL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testOrderList1 (self):
		text = u"бла-бла-бла \n\n#Строка 1\n# Строка 2\n# Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<OL><LI>Строка 1</LI><LI>Строка 2</LI><LI>Строка 3</LI></OL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testOrderList2 (self):
		text = u"бла-бла-бла \n\n#'''Строка 1'''\n# ''Строка 2''\n# Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<OL><LI><B>Строка 1</B></LI><LI><I>Строка 2</I></LI><LI>Строка 3</LI></OL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testOrderListStrike (self):
		text = u"бла-бла-бла \n\n#{-Строка 1-}\n# {-Строка 2-}\n# Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<OL><LI><STRIKE>Строка 1</STRIKE></LI><LI><STRIKE>Строка 2</STRIKE></LI><LI>Строка 3</LI></OL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testEnclosureUnorderList1 (self):
		text = u"бла-бла-бла \n\n*Строка 1\n* Строка 2\n** Вложенная строка 1\n**Вложенная строка 2\n* Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<UL><LI>Строка 1</LI><LI>Строка 2</LI><UL><LI>Вложенная строка 1</LI><LI>Вложенная строка 2</LI></UL><LI>Строка 3</LI></UL>бла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testEnclosureOrderList1 (self):
		text = u"бла-бла-бла \n\n#Строка 1\n# Строка 2\n## Вложенная строка 1\n##Вложенная строка 2\n# Строка 3\nбла-бла-бла"
		result = u'бла-бла-бла \n\n<OL><LI>Строка 1</LI><LI>Строка 2</LI><OL><LI>Вложенная строка 1</LI><LI>Вложенная строка 2</LI></OL><LI>Строка 3</LI></OL>бла-бла-бла'

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

		result = u'<UL><LI>Несортированный список. Элемент 1</LI><LI>Несортированный список. Элемент 2</LI><LI>Несортированный список. Элемент 3</LI><OL><LI>Вложенный сортированный список. Элемент 1</LI><LI>Вложенный сортированный список. Элемент 2</LI><LI>Вложенный сортированный список. Элемент 3</LI><LI>Вложенный сортированный список. Элемент 4</LI><UL><LI>Совсем вложенный сортированный список. Элемент 1</LI><LI>Совсем вложенный сортированный список. Элемент 2</LI></UL><LI>Вложенный сортированный список. Элемент 5</LI></OL><UL><LI>Вложенный несортированный список. Элемент 1</LI></UL></UL>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testEnclosureList2 (self):
		text = u"""* Строка 1
* Строка 2
** Строка 3
# Строка 4
# Строка 5
# Строка 6
# Строка 7"""

		result = u'<UL><LI>Строка 1</LI><LI>Строка 2</LI><UL><LI>Строка 3</LI></UL></UL><OL><LI>Строка 4</LI><LI>Строка 5</LI><LI>Строка 6</LI><LI>Строка 7</LI></OL>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
