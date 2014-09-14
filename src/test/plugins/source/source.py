# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
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


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        self.config.tabWidth.value = 4
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
        self.assertGreater (len (self.loader[self.__pluginname].url), 0)


    def testEmptyCommand (self):
        text = u'''bla-bla-bla (:source:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue (u"bla-bla-bla" in result)


    def test1S (self):
        text = u'''(:source lang="1s":)
Функция УстановитьФизическиеЛица(Выборка)
    Пока Выборка.Следующий() Цикл
        //УстановитьФизическоеЛицо
        ФизическоеЛицо = Справочники.ФизическиеЛица.НайтиПоНаименованию(Выборка.Ссылка);
        Пользователь = Выборка.Ссылка.ПолучитьОбъект();        
        Пользователь.ФизическоеЛицо = ФизическоеЛицо;
        Пользователь.Записать();
        Сообщить("" + Пользователь + " " + Пользователь.ФизическоеЛицо + "-[ОК!]");
    КонецЦикла;
КонецФункции     
(:sourceend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'<span class="c">//УстановитьФизическоеЛицо</span>', result)
        self.assertIn (u'<span class="k">КонецФункции</span>', result)


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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'

        self.assertTrue (innerString1 in result, result)
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = u'          for i in range (10)'
        innerString3 = u'def hello (count):'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth3(self):
        text = u'''(:source tabwidth="-1":)
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = u'    for i in range (10)'
        innerString3 = u'def hello (count):'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth4(self):
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
        self.config.tabWidth.value = -1

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = u'    for i in range (10)'
        innerString3 = u'def hello (count):'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testLineNum1 (self):
        text = u'''(:source linenum:)
import os
import os.path
import sys

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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u""" 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11"""

        self.assertTrue (innerString1 in result)
