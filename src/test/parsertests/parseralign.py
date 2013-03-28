#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserAlignTest (unittest.TestCase):
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
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        self.testPage = self.rootwiki[u"Страница 2"]
        
        files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp", 
                u"файл с пробелами.tmp", u"картинка с пробелами.png", 
                u"image.jpg", u"image.jpeg", u"image.png", u"image.tif", u"image.tiff", u"image.gif",
                u"image_01.JPG", u"dir", u"dir.xxx", u"dir.png"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.rootwiki[u"Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)
    

    def tearDown(self):
        removeWiki (self.path)


    def testCenter1 (self):
        text = u"бла-бла-бла \n%center%кхм бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<DIV ALIGN="CENTER">кхм бла-бла-бла\nбла-бла-бла</DIV>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testCenter2 (self):
        text = u"бла-бла-бла \n%center%кхм бла-бла-бла\n\nбла-бла-бла"
        result = u'бла-бла-бла \n<DIV ALIGN="CENTER">кхм бла-бла-бла</DIV>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testCenter3 (self):
        text = u"%center%бла-бла-бла \nкхм бла-бла-бла\n\nбла-бла-бла"
        result = u'<DIV ALIGN="CENTER">бла-бла-бла \nкхм бла-бла-бла</DIV>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testCenter4 (self):
        text = u"%center%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'<DIV ALIGN="CENTER">бла-бла-бла \n<B>кхм</B> бла-бла-бла</DIV>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testCenter5 (self):
        text = u"бла-бла-бла \n\n% center %Attach:accept.png\n\nбла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n\n<DIV ALIGN="CENTER"><IMG SRC="__attach/accept.png"/></DIV>\n\nбла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testRight1 (self):
        text = u"бла-бла-бла \n% right %кхм бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<DIV ALIGN="RIGHT">кхм бла-бла-бла\nбла-бла-бла</DIV>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLeft1 (self):
        text = u"%left%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'<DIV ALIGN="LEFT">бла-бла-бла \n<B>кхм</B> бла-бла-бла</DIV>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testJustify1 (self):
        text = u"%justify%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'<DIV ALIGN="JUSTIFY">бла-бла-бла \n<B>кхм</B> бла-бла-бла</DIV>\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testInvalidAlign1 (self):
        text = u"%invalid%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'%invalid%бла-бла-бла \n<B>кхм</B> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testInvalidAlign2 (self):
        text = u"%invalid center%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'%invalid center%бла-бла-бла \n<B>кхм</B> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testInvalidAlign3 (self):
        text = u"%center invalid%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = u'%center invalid%бла-бла-бла \n<B>кхм</B> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
