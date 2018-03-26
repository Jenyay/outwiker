# -*- coding: utf-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class LightboxPluginTest(unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.__createWiki()

        dirlist = ["../plugins/lightbox"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testContentParse1(self):
        text = """Бла-бла-бла (:lightbox:) бла-бла-бла"""

        validResult = """$("a[href$='.jpg']"""

        result = self.parser.toHtml(text)
        self.assertTrue(validResult in result)

    def testHeaders(self):
        text = """Бла-бла-бла (:lightbox:) бла-бла-бла"""

        self.parser.toHtml(text)

        self.assertTrue(
            '<script type="text/javascript" src="./__attach/__thumb/jquery-1.7.2.min.js"></script>' in self.parser.head)

        self.assertTrue(
            '<link rel="stylesheet" href="./__attach/__thumb/jquery.fancybox.css" type="text/css" media="screen" />' in self.parser.head)

        self.assertTrue(
            '<script type="text/javascript" src="./__attach/__thumb/jquery.fancybox.pack.js"></script>' in self.parser.head)

    def testSingleHeaders(self):
        """
        Проверка, что заголовки добавляются только один раз
        """
        text = """Бла-бла-бла (:lightbox:) бла-бла-бла (:lightbox:)"""

        self.parser.toHtml(text)

        header = '<script type="text/javascript" src="./__attach/__thumb/jquery-1.7.2.min.js"></script>'

        posfirst = self.parser.head.find(header)
        poslast = self.parser.head.rfind(header)

        self.assertEqual(posfirst, poslast)

    def testFiles(self):
        text = """Бла-бла-бла (:lightbox:) бла-бла-бла"""

        self.parser.toHtml(text)

        dirname = "__attach/__thumb"
        files = ["jquery.fancybox.css",
                 "blank.gif",
                 "fancybox_loading.gif",
                 "jquery-1.7.2.min.js",
                 "jquery.fancybox.pack.js",
                 "fancybox_sprite.png"
                 ]

        for fname in files:
            fullpath = os.path.join(self.testPage.path, dirname, fname)
            self.assertTrue(os.path.exists(fullpath))
