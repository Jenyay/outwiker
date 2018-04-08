# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserUrlTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

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

    def testUrlParse1(self):
        text = "http://example.com/,"
        result = '<a href="http://example.com/">http://example.com/</a>,'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse2(self):
        text = "http://example.com/."
        result = '<a href="http://example.com/">http://example.com/</a>.'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse3(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz),"
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</a>,'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse4(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)."
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)</a>.'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse5(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/,"
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>,'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse6(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/."
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>.'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse7(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse8(self):
        text = "http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/"
        result = '<a href="http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/">http://ru.wikipedia.org/wiki/xxx,_yyy_(zzz)/</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse9(self):
        text = "www.jenyay.net"
        result = '<a href="http://www.jenyay.net">www.jenyay.net</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse10(self):
        text = "www.jenyay.net,"
        result = '<a href="http://www.jenyay.net">www.jenyay.net</a>,'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse11(self):
        text = "www.jenyay.net."
        result = '<a href="http://www.jenyay.net">www.jenyay.net</a>.'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse12(self):
        text = "www.jenyay.net/"
        result = '<a href="http://www.jenyay.net/">www.jenyay.net/</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse13(self):
        text = "ftp.jenyay.net"
        result = '<a href="http://ftp.jenyay.net">ftp.jenyay.net</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse14(self):
        text = "http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431"
        result = '<a href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse15(self):
        text = "бла-бла-бла http://IP-адрес-apt-proxy:9999/ubuntu/ бла-бла"
        result = 'бла-бла-бла <a href="http://IP-адрес-apt-proxy:9999/ubuntu/">http://IP-адрес-apt-proxy:9999/ubuntu/</a> бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse16(self):
        text = "192.168.1.1"
        result = '<a href="http://192.168.1.1">192.168.1.1</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse17(self):
        text = "192.168.100.100"
        result = '<a href="http://192.168.100.100">192.168.100.100</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse18(self):
        text = "999.99.1.1"
        result = '999.99.1.1'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse19(self):
        text = "192.168.100.10010"
        result = '192.168.100.10010'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse20(self):
        text = "Бла бла 192.168.1.1 бла"
        result = 'Бла бла <a href="http://192.168.1.1">192.168.1.1</a> бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse21(self):
        text = "99.99.1.1.20"
        result = '99.99.1.1.20'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse22(self):
        text = "Бла бла 99.99.1.1.20 бла"
        result = 'Бла бла 99.99.1.1.20 бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse23(self):
        text = "192.168.100.256"
        result = '192.168.100.256'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse24(self):
        text = "092.168.10.10"
        result = '<a href="http://092.168.10.10">092.168.10.10</a>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse25(self):
        text = "192.168.100.25абырвалг"
        result = '192.168.100.25абырвалг'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse26(self):
        text = "абырвалг192.168.100.25"
        result = 'абырвалг192.168.100.25'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse27(self):
        text = "0.168.100.100"
        result = '0.168.100.100'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testUrlParse28(self):
        text = "page://__adsfasdfaf"
        result = '<a href="page://__adsfasdfaf">page://__adsfasdfaf</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlParse29(self):
        text = "page://__абырвалг-ффф"
        result = '<a href="page://__абырвалг-ффф">page://__абырвалг-ффф</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlParse30(self):
        text = "page://__adsfasdfaf/"
        result = '<a href="page://__adsfasdfaf/">page://__adsfasdfaf/</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlParse31(self):
        text = "page://__абырвалг-ффф/"
        result = '<a href="page://__абырвалг-ффф/">page://__абырвалг-ффф/</a>'

        self.assertEqual(self.parser.toHtml(text), result)
