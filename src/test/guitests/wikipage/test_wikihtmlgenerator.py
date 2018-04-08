# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.style import Style
from outwiker.core.tree import WikiDocument
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.pages.wiki.parser.command import Command

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig

from test.utils import removeDir
from test.basetestcases import BaseOutWikerMixin


class ExampleFooterWikiCommand(Command):
    def execute(self, params, content):
        self.parser.appendToFooter(content)
        return ''

    @property
    def name(self):
        return "footer"


class ExampleHeadWikiCommand(Command):
    def execute(self, params, content):
        self.parser.appendToHead(content)
        return ''

    @property
    def name(self):
        return "head"


class WikiHtmlGeneratorTest(BaseOutWikerMixin):
    def setUp(self):
        self.initApplication()
        self.filesPath = "../test/samplefiles/"
        self.__createWiki()

        files = ["image.jpg", "dir"]
        self.wikicommands = [ExampleFooterWikiCommand,
                             ExampleHeadWikiCommand,
                             ]

        fullFilesPath = [os.path.join(self.filesPath, fname)
                         for fname
                         in files]

        self.attach_page2 = Attachment(self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

        self.wikitext = """Бла-бла-бла
        %thumb maxsize=250%Attach:image.jpg%%
        Бла-бла-бла"""

        self.testPage.content = self.wikitext

        self.__htmlconfig = HtmlRenderConfig(self.application.config)
        self.__setDefaultConfig()

        self.resultPath = os.path.join(self.testPage.path, PAGE_RESULT_HTML)

        self.application.onWikiParserPrepare += self.__onWikiParserPrepare

    def __setDefaultConfig(self):
        # Установим размер превьюшки, не совпадающий с размером по умолчанию
        self.application.config.set(WikiConfig.WIKI_SECTION,
                                    WikiConfig.THUMB_SIZE_PARAM,
                                    WikiConfig.THUMB_SIZE_DEFAULT)

        self.application.config.set(HtmlRenderConfig.HTML_SECTION,
                                    HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                    HtmlRenderConfig.FONT_NAME_DEFAULT)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def __onWikiParserPrepare(self, parser):
        list([parser.addCommand(command(parser))
              for command in self.wikicommands])

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testEmpty1(self):
        text = "бла-бла-бла"

        content = EmptyContent(self.application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = ""

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue(text in result)

    def testEmpty2(self):
        text = "(:attachlist:)"

        content = EmptyContent(self.application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = ""

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("image.jpg" in result)

    def testFooter_01(self):
        text = 'Бла-бла-бла(:footer:)Подвал 1(:footerend:)'
        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('Бла-бла-бла<br/>\nПодвал 1\n</body>',
                      result.replace('\r\n', '\n'))

    def testFooter_02(self):
        text = 'Бла-бла-бла(:footer:)Подвал 1(:footerend:)(:footer:)Подвал 2(:footerend:)11111'
        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('Бла-бла-бла11111<br/>\nПодвал 1Подвал 2\n</body>',
                      result.replace('\r\n', '\n'))

    def testHead_01(self):
        text = 'Бла-бла-бла(:head:)Заголовок 1(:headend:)'
        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('Заголовок 1\n</head>',
                      result.replace('\r\n', '\n'))

    def testHead_02(self):
        text = '''Бла-бла-бла
(:head:)Заголовок 1(:headend:)
(:head:)Заголовок 2(:headend:)
'''
        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('Заголовок 1Заголовок 2\n</head>',
                      result.replace('\r\n', '\n'))
