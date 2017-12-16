# -*- coding: UTF-8 -*-

import os
import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserAttachTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

        self.pagelinks = ["Страница 1", "/Страница 1", "/Страница 2/Страница 3"]
        self.pageComments = ["Страницо 1", "Страницо 1", "Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["accept.png", "add.png", "anchor.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif", "image.tiff", "image.gif",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)


    def tearDown(self):
        removeDir (self.path)


    def testAttach01 (self):
        fname = "filename.tmp"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach02 (self):
        fname = "accept.png"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach03 (self):
        fname = "filename.tmp"
        text = "бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach04 (self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach05 (self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach06 (self):
        fname = "картинка с пробелами.png"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach07 (self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach08 (self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:%s | Комментарий]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach09 (self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:%s | Комментарий]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach10 (self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Комментарий -> Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach11 (self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Комментарий -> Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    def testAttach12 (self):
        fname = "image_01.JPG"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach13 (self):
        fname = "dir.xxx"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding) + "\n" + result.encode (self.encoding))


    def testAttach14 (self):
        fname = "dir"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding) + "\n" + result.encode (self.encoding))


    def testAttach15 (self):
        fname = "dir.png"
        text = "бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = 'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
