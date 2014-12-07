# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig

from utils import removeDir


class WikiHtmlGeneratorTest (unittest.TestCase):
    def setUp(self):
        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        files = [u"image.jpg", u"dir"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.wikiroot[u"Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)

        self.wikitext = u"""Бла-бла-бла
        %thumb maxsize=250%Attach:image.jpg%%
        Бла-бла-бла"""

        self.testPage.content = self.wikitext

        self.__htmlconfig = HtmlRenderConfig (Application.config)
        self.__setDefaultConfig()

        self.resultPath = os.path.join (self.testPage.path, u"__content.html")


    def __setDefaultConfig (self):
        # Установим размер превьюшки, не совпадающий с размером по умолчанию
        Application.config.set (WikiConfig.WIKI_SECTION,
                                WikiConfig.THUMB_SIZE_PARAM,
                                WikiConfig.THUMB_SIZE_DEFAULT)

        Application.config.set (HtmlRenderConfig.HTML_SECTION,
                                HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                HtmlRenderConfig.FONT_NAME_DEFAULT)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        self.__setDefaultConfig()
        removeDir (self.path)


    def testEmpty1 (self):
        text = u"бла-бла-бла"

        content = EmptyContent (Application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = u""

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml(Style().getPageStyle (self.testPage))

        self.assertTrue (text in result)


    def testEmpty2 (self):
        text = u"(:attachlist:)"

        content = EmptyContent (Application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = u""

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml(Style().getPageStyle (self.testPage))

        self.assertTrue (u"image.jpg" in result)
