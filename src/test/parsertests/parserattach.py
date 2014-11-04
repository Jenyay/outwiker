# -*- coding: UTF-8 -*-

import os
import unittest

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserAttachTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir (self.path)

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]

        files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp",
                 u"файл с пробелами.tmp", u"картинка с пробелами.png",
                 u"image.jpg", u"image.jpeg", u"image.png", u"image.tif", u"image.tiff", u"image.gif",
                 u"image_01.JPG", u"dir", u"dir.xxx", u"dir.png"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.wikiroot[u"Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)


    def tearDown(self):
        removeDir (self.path)


    def testAttach01 (self):
        fname = u"filename.tmp"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach02 (self):
        fname = u"accept.png"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach03 (self):
        fname = u"filename.tmp"
        text = u"бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach04 (self):
        fname = u"файл с пробелами.tmp"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach05 (self):
        fname = u"файл с пробелами.tmp"
        text = u"бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach06 (self):
        fname = u"картинка с пробелами.png"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach07 (self):
        fname = u"accept.png"
        text = u"бла-бла-бла \n[[Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach08 (self):
        fname = u"accept.png"
        text = u"бла-бла-бла \n[[Attach:%s | Комментарий]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach09 (self):
        fname = u"файл с пробелами.tmp"
        text = u"бла-бла-бла \n[[Attach:%s | Комментарий]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach10 (self):
        fname = u"accept.png"
        text = u"бла-бла-бла \n[[Комментарий -> Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach11 (self):
        fname = u"файл с пробелами.tmp"
        text = u"бла-бла-бла \n[[Комментарий -> Attach:%s]] бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">Комментарий</a> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    def testAttach12 (self):
        fname = u"image_01.JPG"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testAttach13 (self):
        fname = u"dir.xxx"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding) + "\n" + result.encode (self.encoding))


    def testAttach14 (self):
        fname = u"dir"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<a href="__attach/%s">%s</a> бла-бла-бла\nбла-бла-бла' % (fname, fname)

        self.assertEqual (self.parser.toHtml (text),
                          result,
                          self.parser.toHtml (text).encode (self.encoding) + "\n" + result.encode (self.encoding))


    def testAttach15 (self):
        fname = u"dir.png"
        text = u"бла-бла-бла \nAttach:%s бла-бла-бла\nбла-бла-бла" % (fname)
        result = u'бла-бла-бла \n<img src="__attach/%s"/> бла-бла-бла\nбла-бла-бла' % (fname)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
