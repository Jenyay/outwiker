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
        Application.config.remove_section (self.config.section)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        self.config.tabWidth.value = 4
        Application.config.remove_section (self.config.section)
        removeDir (self.path)
        self.loader.clear()


    def testDefaultStyle (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testDefaultInvalidStyle (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "invalid_blablabla"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testDefaultEmptyStyle (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = ""

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testDefaultStyleVim (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testInvalidStyle (self):
        text = u'(:source lang="python" tabwidth=4 style="invalid_bla-bla-bla":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
        innerString4 = u'<span class="kn">import</span> <span class="nn">os</span>'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)


    def testStyleVim (self):
        text = u'(:source lang="python" tabwidth=4 style="vim":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
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
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"
        innerString3 = u'        <span class="k">print</span> <span class="s2">&quot;Hello world!!!&quot;</span>'
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


    def testDefaultStyleFile (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        text = u'(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)


    def testDefaultInvalidStyleFile (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        text = u'(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "invalid_blablabla"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)


    def testDefaultEmptyStyleFile (self):
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        text = u'(:source lang="python" tabwidth=4 file="source_utf8.py":){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = ""

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-default .c"
        innerString2 = u".highlight-default .c { color: #408080; font-style: italic } /* Comment */"

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)


    def testDefaultStyleVimFile (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text

        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim .c"
        innerString2 = u".highlight-vim .c { color: #000080 } /* Comment */"

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)


    def testParentBg1 (self):
        text = u'(:source lang="python" tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = u".highlight-vim {color: inherit; background-color: inherit }"

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 not in result)


    def testParentBg2 (self):
        text = u'(:source lang="python" tabwidth=4 parentbg:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = u".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = u'<div class="highlight-vim-parentbg">'
        innerString4 = u".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = u'<div class="highlight-vim">'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 not in result)
        self.assertTrue (innerString5 not in result)


    def testParentBg3 (self):
        text = u'(:source lang="python" parentbg tabwidth=4:){0}(:sourceend:)'.format (self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = u".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = u'<div class="highlight-vim-parentbg">'
        innerString4 = u".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = u'<div class="highlight-vim">'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 not in result)
        self.assertTrue (innerString5 not in result)


    def testParentBg4 (self):
        text = u'''(:source lang="python" tabwidth=4:){0}(:sourceend:)

        (:source lang="python" tabwidth=4 parentbg:){0}(:sourceend:)'''.format (self.pythonSource)

        self.testPage.content = text
        self.config.defaultStyle.value = "vim"

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        innerString1 = u".highlight-vim-parentbg pre {padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }"
        innerString2 = u".highlight-vim-parentbg {color: inherit; background-color: inherit }"
        innerString3 = u'<div class="highlight-vim-parentbg">'
        innerString4 = u".highlight-vim {color: inherit; background-color: inherit }"
        innerString5 = u'<div class="highlight-vim">'

        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 not in result)
        self.assertTrue (innerString5 in result)
