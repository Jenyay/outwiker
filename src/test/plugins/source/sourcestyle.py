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


class SourceStyleTest (unittest.TestCase):
    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"

        # Пример программы
        self.pythonSource = u'''import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
'''

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
        self.config.tabWidth.value = 4
        removeWiki (self.path)
        self.loader.clear()


    def testDefaultStyle (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testInvalidStyle (self):
        text = u'(:source lang="python" tabwidth=4 style="invalid_bla-bla-bla":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testStyleVim (self):
        text = u'(:source lang="python" tabwidth=4 style="vim":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testSeveralStyles (self):
        text = u'''(:source lang="python" tabwidth=4 style="vim":){0}(:sourceend:)
        
(:source lang="python" tabwidth=4:){0}(:sourceend:)'''.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'
        innerString5 = u".highlight-default .c"
        innerString6 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString7 = u'<div class="highlight-default">'
        innerString8 = u'<div class="highlight-vim">'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)
        self.assertTrue (innerString5 in result)
        self.assertTrue (innerString6 in result)
        self.assertTrue (innerString7 in result)
        self.assertTrue (innerString8 in result)
