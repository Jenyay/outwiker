# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.basetestcases import BaseOutWikerGUIMixin


class SourcePluginTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.__pluginname = "Source"
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])

        dirlist = ["../plugins/source"]

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self.application.config)

    def tearDown(self):
        self.config.tabWidth.value = 4
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
        self.assertGreater(len(self.loader[self.__pluginname].url), 0)

    def testEmptyCommand(self):
        text = '''bla-bla-bla (:source:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("bla-bla-bla" in result)

    def test1S(self):
        text = '''(:source lang="1s":)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn(
            '<span class="c">//УстановитьФизическоеЛицо</span>', result)
        self.assertIn('<span class="k">КонецФункции</span>', result)

    def testFullHtmlPython(self):
        text = '''(:source lang="python" tabwidth=5:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '          <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString3 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)

    def testFullHtmlPython2(self):
        text = '''(:source lang="python":)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '       <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString3 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)

    def testFullHtmlPython3(self):
        # Неправильный размер табуляции
        text = '''(:source lang="python" tabwidth="qqqqq":)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '       <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString3 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)

    def testFullHtmlInvalidLang(self):
        text = '''(:source lang="qqq" tabwidth=4:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '        print &quot;Hello world!!!&quot;'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result, result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testFullHtmlText(self):
        text = '''(:source lang="text" tabwidth=4:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '        print &quot;Hello world!!!&quot;'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testFullHtmlText2(self):
        text = '''(:source:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '        print &quot;Hello world!!!&quot;'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testManySource(self):
        text = '''(:source lang=python:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '        print &quot;Hello world!!!&quot;'
        innerString3 = 'def hello (count):'
        innerString4 = '       <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString5 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)

        # Проверка того, что стиль добавился только один раз
        self.assertTrue(result.find(innerString1) ==
                        result.rfind(innerString1))

        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)
        self.assertTrue(innerString5 in result)
        self.assertFalse("(:source" in result)

    def testConfigTabWidth(self):
        text = '''(:source:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '          for i in range (10)'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testConfigTabWidth2(self):
        text = '''(:source tabwidth=10:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '          for i in range (10)'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testConfigTabWidth3(self):
        text = '''(:source tabwidth="-1":)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '    for i in range (10)'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testConfigTabWidth4(self):
        text = '''(:source:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .go { color: #888888 } /* Generic.Output */"
        innerString2 = '    for i in range (10)'
        innerString3 = 'def hello (count):'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertFalse("(:source" in result)

    def testLineNum1(self):
        text = '''(:source linenum:)
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

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = """ 1
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

        self.assertTrue(innerString1 in result)
