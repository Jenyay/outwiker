#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserImagesTest (unittest.TestCase):
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
        

    def tearDown(self):
        removeWiki (self.path)


    def testImage1 (self):
        url = u"http://jenyay.net/social/feed.png"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage2 (self):
        url = u"http://jenyay.net/social/feed.jpg"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testImage3 (self):
        url = u"http://jenyay.net/social/feed.jpeg"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage4 (self):
        url = u"http://jenyay.net/social/feed.bmp"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage5 (self):
        url = u"http://jenyay.net/social/feed.tif"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage6 (self):
        url = u"http://jenyay.net/social/feed.tiff"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage7 (self):
        url = u"http://jenyay.net/social/feed.gif"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testImage8 (self):
        url = u"http://www.wuala.com/jenyayIlin/Photos/%D0%A1%D0%BC%D0%BE%D0%BB%D0%B5%D0%BD%D1%81%D0%BA.%20%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5/smolensk_animals_01.jpg"

        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testImage9 (self):
        url = u"https://lh5.googleusercontent.com/-IbkA63YQYq0/Ub4Axyf2sNI/AAAAAAAADiY/q8fRG3uXtRY/s700/2013-06-16+09.06.29.jpg"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testImage10 (self):
        url = u"https://lh5.googleusercontent.com/-_StTTaVjYXw/Ub4A0Gz7VaI/AAAAAAAADik/2BP9muKXDWQ/s700/2013-06-16+13.27.27.jpg"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testImage11 (self):
        url = u"https://lh4.googleusercontent.com/-0r9yj2bE02A/UbQcriTO4oI/AAAAAAAADfM/bQAHRmcqr6Y/w617-h822-no/2013-06-08_19-28-28_430.jpg"
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<img src="%s"/> бла-бла-бла\nбла-бла-бла' % (url)

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
