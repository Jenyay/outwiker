# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeDir


class SourceFilePluginTest (unittest.TestCase):
    """
    Тесты на работу с раскраской прикрепленных файлов
    """
    def setUp(self):
        self.__pluginname = "Source"

        self.__createWiki()

        dirlist = ["../plugins/source"]

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]


    def tearDown(self):
        removeDir (self.path)
        self.loader.clear()


    def testHighlightFile1 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile2 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="Attach:source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile3 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="  source_utf8.py  " lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile4 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="  Attach:source_utf8.py  " lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile5 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py" lang="text":)(:sourceend:)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)


    def testHighlightFile6 (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py" lang="text":)bla-bla-bla(:sourceend:)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("__correctSysPath()" in result)
        self.assertTrue ("Плагин, добавляющий обработку команды (:source:) в википарсер" in result)
        self.assertTrue ("bla-bla-bla" not in result)


    def testHighlightFile7 (self):
        """
        Явное задание языка для раскраски
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py" lang="python":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ('<span class="kn">import</span> <span class="nn">os.path</span>' in result)
        self.assertTrue ('<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' in result)


    def testHighlightFile8 (self):
        """
        Нет явного задания языка
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ('<span class="kn">import</span> <span class="nn">os.path</span>' in result)
        self.assertTrue ('<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' in result)


    def testHighlightFile9 (self):
        """
        Явное задание языка, не соответствующее расширению файла
        """
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ('<span class="kn">import</span> <span class="nn">os.path</span>' not in result)
        self.assertTrue ('import os.path' in result)

        self.assertTrue ('<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' not in result)
        self.assertTrue ("__correctSysPath()" in result)


    def testHighlightFile10 (self):
        """
        Проверка случая, если прикрепленного с заданным именем файла нет
        """
        content = '(:source file="source_utf8111.py" lang="text":)'
        self.testPage.content = content

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ('source_utf8111.py' in result, result)
