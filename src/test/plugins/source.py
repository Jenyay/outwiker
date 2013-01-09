#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class SourcePluginTest (unittest.TestCase):
    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        
        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __readFile (self, path):
        with open (path) as fp:
            result = unicode (fp.read(), "utf8")

        return result
    

    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]
        

    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)
        self.assertGreater (len (self.loader[self.__pluginname].url), 0)


    def testEmptyCommand (self):
        text = u'''bla-bla-bla (:source:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"bla-bla-bla" in result)


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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testManySource (self):
        text = u'''(:source lang=python:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)


(:source:)
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
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        innerString4 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString5 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
    
        # Проверка того, что стиль добавился только один раз
        self.assertTrue (result.find (innerString1) == result.rfind (innerString1))

        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)
        self.assertTrue (innerString5 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth(self):
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
        self.config.tabWidth.value = 10

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'          for i in range (10)'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth2(self):
        text = u'''(:source tabwidth=10:)
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
        self.config.tabWidth.value = 4

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'          for i in range (10)'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testHighlightFile1 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile2 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="Attach:source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile3 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="  source_utf8.py  " lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile4 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="  Attach:source_utf8.py  " lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile5 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py" lang="text":)(:sourceend:)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile6 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py" lang="text":)bla-bla-bla(:sourceend:)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"__correctSysPath()" in result)
        self.assertTrue (u"Плагин, добавляющий обработку команды (:source:) в википарсер" in result)
        self.assertTrue (u"bla-bla-bla" not in result)


    def testHighlightFile7 (self):
        """
        Явное задание языка для раскраски
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py" lang="python":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u'<span class="kn">import</span> <span class="nn">os.path</span>' in result)
        self.assertTrue (u'<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' in result)


    def testHighlightFile8 (self):
        """
        Нет явного задания языка
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u'<span class="kn">import</span> <span class="nn">os.path</span>' in result)
        self.assertTrue (u'<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' in result)


    def testHighlightFile9 (self):
        """
        Явное задание языка, не соответствующее расширению файла
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        content = u'(:source file="source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u'<span class="kn">import</span> <span class="nn">os.path</span>' not in result)
        self.assertTrue (u'import os.path' in result)

        self.assertTrue (u'<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' not in result)
        self.assertTrue (u"__correctSysPath()" in result)
