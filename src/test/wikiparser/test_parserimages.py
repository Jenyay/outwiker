# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserImagesTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

        self.pagelinks = [
            "Страница 1",
            "/Страница 1",
            "/Страница 2/Страница 3"]
        self.pageComments = ["Страницо 1", "Страницо 1", "Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        removeDir(self.path)

    def testImage1(self):
        url = "http://jenyay.net/social/feed.png"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage2(self):
        url = "http://jenyay.net/social/feed.jpg"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage3(self):
        url = "http://jenyay.net/social/feed.jpeg"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage4(self):
        url = "http://jenyay.net/social/feed.bmp"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage5(self):
        url = "http://jenyay.net/social/feed.tif"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage6(self):
        url = "http://jenyay.net/social/feed.tiff"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage7(self):
        url = "http://jenyay.net/social/feed.gif"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage8(self):
        url = "http://www.wuala.com/jenyayIlin/Photos/%D0%A1%D0%BC%D0%BE%D0%BB%D0%B5%D0%BD%D1%81%D0%BA.%20%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5/smolensk_animals_01.jpg"

        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage9(self):
        url = "https://lh5.googleusercontent.com/-IbkA63YQYq0/Ub4Axyf2sNI/AAAAAAAADiY/q8fRG3uXtRY/s700/2013-06-16+09.06.29.jpg"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage10(self):
        url = "https://lh5.googleusercontent.com/-_StTTaVjYXw/Ub4A0Gz7VaI/AAAAAAAADik/2BP9muKXDWQ/s700/2013-06-16+13.27.27.jpg"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testImage11(self):
        url = "https://lh4.googleusercontent.com/-0r9yj2bE02A/UbQcriTO4oI/AAAAAAAADfM/bQAHRmcqr6Y/w617-h822-no/2013-06-08_19-28-28_430.jpg"
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (
            url)

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))
