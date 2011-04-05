#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from utils import removeWiki

from core.tree import WikiDocument
from core.attachment import Attachment
from core.application import Application

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory


class ParserUrlTest (unittest.TestCase):
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
	

	def testUrlParse1 (self):
		text = u"http://example.com/,"
		result = u'<A HREF="http://example.com/">http://example.com/</A>,'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUrlParse2 (self):
		text = u"http://example.com/."
		result = u'<A HREF="http://example.com/">http://example.com/</A>.'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUrlParse3 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz),"
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</A>,'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUrlParse4 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)."
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</A>.'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUrlParse5 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/,"
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</A>,'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testUrlParse6 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/."
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</A>.'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUrlParse7 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testUrlParse8 (self):
		text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
		result = u'<A HREF="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUrlParse9 (self):
		text = u"www.jenyay.net"
		result = u'<A HREF="http://www.jenyay.net">www.jenyay.net</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testUrlParse10 (self):
		text = u"www.jenyay.net,"
		result = u'<A HREF="http://www.jenyay.net">www.jenyay.net</A>,'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUrlParse11 (self):
		text = u"www.jenyay.net."
		result = u'<A HREF="http://www.jenyay.net">www.jenyay.net</A>.'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUrlParse12 (self):
		text = u"www.jenyay.net/"
		result = u'<A HREF="http://www.jenyay.net/">www.jenyay.net/</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUrlParse9 (self):
		text = u"ftp.jenyay.net"
		result = u'<A HREF="http://ftp.jenyay.net">ftp.jenyay.net</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testUrlParse10 (self):
		text = u"http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431"
		result = u'<A HREF="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431</A>'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
