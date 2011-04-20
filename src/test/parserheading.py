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


class ParserHeadingTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "866"

		self.filesPath = u"../test/samplefiles/"

		self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
		self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

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


	def testHeader1 (self):
		text = u"бла-бла-бла \n!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H1>Заголовок бла-бла-бла</H1>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader2 (self):
		text = u"бла-бла-бла \n!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок бла-бла-бла</H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeader3 (self):
		text = u"бла-бла-бла \n!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H3>Заголовок бла-бла-бла</H3>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testHeader4 (self):
		text = u"бла-бла-бла \n!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H4>Заголовок бла-бла-бла</H4>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader5 (self):
		text = u"бла-бла-бла \n!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H5>Заголовок бла-бла-бла</H5>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader6 (self):
		text = u"бла-бла-бла \n!!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \n<H6>Заголовок бла-бла-бла</H6>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testHeader7 (self):
		text = u"бла-бла-бла \nкхм !! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testHeader8 (self):
		text = u"бла-бла-бла \nкхм !!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !!! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader9 (self):
		text = u"бла-бла-бла \nкхм !!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !!!! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader10 (self):
		text = u"бла-бла-бла \nкхм !!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !!!!! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testHeader11 (self):
		text = u"бла-бла-бла \nкхм !!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !!!!!! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeader11 (self):
		text = u"бла-бла-бла \nкхм !!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм !!!!!!! Заголовок бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderItalic1 (self):
		text = u"бла-бла-бла \n!! Заголовок ''бла-бла-бла''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H1>Заголовок <I>бла-бла-бла</I></H1>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderItalic2 (self):
		text = u"бла-бла-бла \n!!! Заголовок ''бла-бла-бла''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <I>бла-бла-бла</I></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBold1 (self):
		text = u"бла-бла-бла \n!! Заголовок '''бла-бла-бла'''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H1>Заголовок <B>бла-бла-бла</B></H1>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBold2 (self):
		text = u"бла-бла-бла \n!!! Заголовок '''бла-бла-бла'''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <B>бла-бла-бла</B></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBoldSubscript (self):
		text = u"бла-бла-бла \n!!! Заголовок ''''_бла-бла-бла_''''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <B><SUB>бла-бла-бла</SUB></B></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBoldSuperscript (self):
		text = u"бла-бла-бла \n!!! Заголовок ''''^бла-бла-бла^''''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <B><SUP>бла-бла-бла</SUP></B></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderItalicSubscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '''_бла-бла-бла_'''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <I><SUB>бла-бла-бла</SUB></I></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderItalicSuperscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '''^бла-бла-бла^'''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <I><SUP>бла-бла-бла</SUP></I></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBoldItalicSubscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '''''_бла-бла-бла_'''''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <B><I><SUB>бла-бла-бла</SUB></I></B></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderBoldItalicSuperscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '''''^бла-бла-бла^'''''\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <B><I><SUP>бла-бла-бла</SUP></I></B></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderSubscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '_бла-бла-бла_'\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <SUB>бла-бла-бла</SUB></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderSuperscript (self):
		text = u"бла-бла-бла \n!!! Заголовок '^бла-бла-бла^'\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <SUP>бла-бла-бла</SUP></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderUnderline (self):
		text = u"бла-бла-бла \n!!! Заголовок {+бла-бла-бла+}\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок <U>бла-бла-бла</U></H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderNoFormat (self):
		text = u"бла-бла-бла \n!!! Заголовок [={+бла-бла-бла+}=]\nбла-бла-бла"
		result = u'бла-бла-бла \n<H2>Заголовок {+бла-бла-бла+}</H2>\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderLjUser (self):
		text = u"бла-бла-бла \n!!! Заголовок (:ljuser jenyay:)\nбла-бла-бла"

		result = u"бла-бла-бла \n<H2>Заголовок <span class='ljuser ljuser-name_jenyay' lj:user='jenyay' style='white-space:nowrap'><a href='http://jenyay.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://jenyay.livejournal.com/'><b>jenyay</b></a></span></H2>\nбла-бла-бла"

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testHeaderTex (self):
		text = u"бла-бла-бла \n!!! Заголовок {$e^x$}\nбла-бла-бла"
		result_parse = self.parser.toHtml (text)

		self.assertTrue (result_parse.startswith (u'бла-бла-бла \n<H2>Заголовок <IMG SRC="__attach/__thumb/eqn_') )
