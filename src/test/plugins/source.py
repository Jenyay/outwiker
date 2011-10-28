#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class SourcePluginTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "866"
		self.maxDiff = None

		self.filesPath = u"../test/samplefiles/"
		self.__createWiki()

		dirlist = [u"../plugins/source"]

		self.loader = PluginsLoader(Application)
		self.loader.load (dirlist)
		
		self.factory = ParserFactory()
		self.parser = self.factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
		self.testPage = self.rootwiki[u"Страница 1"]
		

	def tearDown(self):
		removeWiki (self.path)


	def testPluginLoad (self):
		self.assertEqual ( len (self.loader), 1)


	def testFullHtmlPython (self):
		text = u'''(:source lang="python" tabwidth=5:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'          <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
		innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)


	def testFullHtmlPython2 (self):
		text = u'''(:source lang="python":)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
		innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)


	def testFullHtmlPython3 (self):
		# Неправильный размер табуляции
		text = u'''(:source lang="python" tabwidth="qqqqq":)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
		innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)


	def testFullHtmlInvalidLang (self):
		text = u'''(:source lang="qqq" tabwidth=4:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'        print &quot;Hello world!!!&quot;'
		innerString3 = u'def hello (count):'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)
		self.assertFalse (u"(:source" in result)


	def testFullHtmlText (self):
		text = u'''(:source lang="text" tabwidth=4:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'        print &quot;Hello world!!!&quot;'
		innerString3 = u'def hello (count):'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)
		self.assertFalse (u"(:source" in result)


	def testFullHtmlText2 (self):
		text = u'''(:source:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

		self.testPage.content = text

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()
		result = self.__readFile (htmlpath)

		innerString1 = u".go { color: #808080 } /* Generic.Output */"
		innerString2 = u'        print &quot;Hello world!!!&quot;'
		innerString3 = u'def hello (count):'
		
		self.assertTrue (innerString1 in result)
		self.assertTrue (innerString2 in result)
		self.assertTrue (innerString3 in result)
		self.assertFalse (u"(:source" in result)


	def __readFile (self, path):
		with open (path) as fp:
			result = unicode (fp.read(), "utf8")

		return result
