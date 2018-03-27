# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.style import Style
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.basetestcases import BaseOutWikerGUITest


class SourceStyleTest (BaseOutWikerGUITest):
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

        # Пример программы
        self.pythonSource = '''import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
'''

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        self.application.config.remove_section(self.config.section)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self.application.config)

    def tearDown(self):
        self.config.tabWidth.value = 4
        self.application.config.remove_section(self.config.section)
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefaultStyle(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testDefaultInvalidStyle(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "invalid_blablabla"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testDefaultEmptyStyle(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = ""

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testDefaultStyleVim(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim .c"
        innerString2 = ".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testInvalidStyle(self):
        text = '(:source lang="python" tabwidth=4 style="invalid_bla-bla-bla":){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testStyleVim(self):
        text = '(:source lang="python" tabwidth=4 style="vim":){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim .c"
        innerString2 = ".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)

    def testSeveralStyles(self):
        text = '''(:source lang="python" tabwidth=4 style="vim":){0}(:sourceend:)

(:source lang="python" tabwidth=4:){0}(:sourceend:)'''.format(self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim .c"
        innerString2 = ".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = '        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = '<span class="kn">import</span> <span class="nn">os</span>'
        innerString5 = ".highlight-default .c"
        innerString6 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString7 = '<div class="highlight-default">'
        innerString8 = '<div class="highlight-vim">'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 in result)
        self.assertTrue(innerString5 in result)
        self.assertTrue(innerString6 in result)
        self.assertTrue(innerString7 in result)
        self.assertTrue(innerString8 in result)

    def testDefaultStyleFile(self):
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        text = '(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)

    def testDefaultInvalidStyleFile(self):
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        text = '(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "invalid_blablabla"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)

    def testDefaultEmptyStyleFile(self):
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        text = '(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = ""

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-default .c"
        innerString2 = ".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)

    def testDefaultStyleVimFile(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim .c"
        innerString2 = ".highlight-vim .c { color: #000080 } /* Comment */"

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)

    def testParentBg1(self):
        text = '(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = ".highlight-vim {color: inherit; background-color: inherit }"

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 not in result)

    def testParentBg2(self):
        text = '(:source lang="python" tabwidth=4 parentbg:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = ".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = '<div class="highlight-vim-parentbg">'
        innerString4 = ".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = '<div class="highlight-vim">'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 not in result)
        self.assertTrue(innerString5 not in result)

    def testParentBg3(self):
        text = '(:source lang="python" parentbg tabwidth=4:){0}(:sourceend:)'.format(
            self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = ".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = '<div class="highlight-vim-parentbg">'
        innerString4 = ".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = '<div class="highlight-vim">'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 not in result)
        self.assertTrue(innerString5 not in result)

    def testParentBg4(self):
        text = '''(:source lang="python" tabwidth=4:){0}(:sourceend:)

        (:source lang="python" tabwidth=4 parentbg:){0}(:sourceend:)'''.format(self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        innerString1 = ".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = ".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = '<div class="highlight-vim-parentbg">'
        innerString4 = ".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = '<div class="highlight-vim">'

        self.assertTrue(innerString1 in result)
        self.assertTrue(innerString2 in result)
        self.assertTrue(innerString3 in result)
        self.assertTrue(innerString4 not in result)
        self.assertTrue(innerString5 in result)
