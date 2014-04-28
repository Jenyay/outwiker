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


class ParserUrlTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

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
    

    def testUrlParse1 (self):
        text = u"http://example.com/,"
        result = u'<a href="http://example.com/">http://example.com/</a>,'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testUrlParse2 (self):
        text = u"http://example.com/."
        result = u'<a href="http://example.com/">http://example.com/</a>.'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse3 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz),"
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</a>,'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testUrlParse4 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)."
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</a>.'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testUrlParse5 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/,"
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>,'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testUrlParse6 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/."
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>.'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse7 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testUrlParse8 (self):
        text = u"http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
        result = u'<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testUrlParse9 (self):
        text = u"www.jenyay.net"
        result = u'<a href="http://www.jenyay.net">www.jenyay.net</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testUrlParse10 (self):
        text = u"www.jenyay.net,"
        result = u'<a href="http://www.jenyay.net">www.jenyay.net</a>,'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse11 (self):
        text = u"www.jenyay.net."
        result = u'<a href="http://www.jenyay.net">www.jenyay.net</a>.'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse12 (self):
        text = u"www.jenyay.net/"
        result = u'<a href="http://www.jenyay.net/">www.jenyay.net/</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse13 (self):
        text = u"ftp.jenyay.net"
        result = u'<a href="http://ftp.jenyay.net">ftp.jenyay.net</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testUrlParse14 (self):
        text = u"http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431"
        result = u'<a href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse15 (self):
        text = u"бла-бла-бла http://IP-адрес-apt-proxy:9999/ubuntu/ бла-бла"
        result = u'бла-бла-бла <a href="http://IP-адрес-apt-proxy:9999/ubuntu/">http://IP-адрес-apt-proxy:9999/ubuntu/</a> бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse16 (self):
        text = u"192.168.1.1"
        result = u'<a href="http://192.168.1.1">192.168.1.1</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse17 (self):
        text = u"192.168.100.100"
        result = u'<a href="http://192.168.100.100">192.168.100.100</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse18 (self):
        text = u"999.99.1.1"
        result = u'999.99.1.1'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse19 (self):
        text = u"192.168.100.10010"
        result = u'192.168.100.10010'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse20 (self):
        text = u"Бла бла 192.168.1.1 бла"
        result = u'Бла бла <a href="http://192.168.1.1">192.168.1.1</a> бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    def testUrlParse21 (self):
        text = u"99.99.1.1.20"
        result = u'99.99.1.1.20'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse22 (self):
        text = u"Бла бла 99.99.1.1.20 бла"
        result = u'Бла бла 99.99.1.1.20 бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse23 (self):
        text = u"192.168.100.256"
        result = u'192.168.100.256'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse24 (self):
        text = u"092.168.10.10"
        result = u'<a href="http://092.168.10.10">092.168.10.10</a>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUrlParse25 (self):
        text = u"192.168.100.25абырвалг"
        result = u'192.168.100.25абырвалг'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    def testUrlParse26 (self):
        text = u"абырвалг192.168.100.25"
        result = u'абырвалг192.168.100.25'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
