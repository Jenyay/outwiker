# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeDir


class SpoilerPluginTest(unittest.TestCase):
    def setUp(self):
        self.__pluginname = "Spoiler"

        self.__createWiki()

        dirlist = ["../plugins/spoiler"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

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

    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)

    def testInterface (self):
        """
        Тест на то, что в интерфейсе классов outwiker не пропали нужные публичные свойства и методы
        """
        from outwiker.core.pluginbase import Plugin
        from outwiker.core.system import getOS
        from outwiker.core.commands import getCurrentVersion
        from outwiker.core.version import Version, StatusSet
        from outwiker.pages.wiki.parser.command import Command

        StatusSet.DEV
        Command.parseParams

    def testEmptyCommand (self):
        text = '''bla-bla-bla (:spoiler:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("bla-bla-bla" in result)

    def testSimple (self):
        text = "бла-бла-бла (:spoiler:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertTrue ("Текст</div></div></div>" in result)

    def testSimpleNumbers (self):
        for index in range (10):
            text = "бла-бла-бла (:spoiler{index}:)Текст(:spoiler{index}end:)".format (index=index)

            self.testPage.content = text

            generator = HtmlGenerator (self.testPage)
            result = generator.makeHtml (Style().getPageStyle (self.testPage))

            self.assertTrue ("бла-бла-бла" in result)
            self.assertTrue ("Текст</div></div></div>" in result)

    def testWikiBoldContent (self):
        text = "бла-бла-бла (:spoiler:)'''Текст'''(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertTrue ("<b>Текст</b></div></div></div>" in result)

    def testExpandText (self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertTrue ("Текст</div></div></div>" in result)
        self.assertTrue ("Раскукожить</a></span></div>" in result)

    def testCollapseText (self):
        text = """бла-бла-бла (:spoiler collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertTrue ("Текст</div></div></div>" in result)
        self.assertTrue ("Скукожить</a>" in result)

    def testExpandCollapseText (self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить" collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertTrue ("Текст</div></div></div>" in result)
        self.assertTrue ("Раскукожить</a></span></div>" in result)
        self.assertTrue ("Скукожить</a>" in result)

    def testInline (self):
        text = "бла-бла-бла (:spoiler inline:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertFalse ("Текст</div></div></div>" in result)
        self.assertTrue ("<span><span" in result)

    def testInlineExpandText (self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить" inline:)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue ("бла-бла-бла" in result)
        self.assertFalse ("Текст</div></div></div>" in result)
        self.assertTrue ("<span><span" in result)
        self.assertTrue ("""<a href="#">Раскукожить</a>""" in result)
