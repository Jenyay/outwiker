# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.pages.wiki.parser.tokenfonts import FontsFactory
from outwiker.pages.wiki.parser.tokenquote import QuoteFactory
from outwiker.pages.wiki.parser.tokennoformat import NoFormatFactory
from outwiker.pages.wiki.parser.tokenpreformat import PreFormatFactory
from outwiker.pages.wiki.parser.tokenthumbnail import ThumbnailFactory
from outwiker.pages.wiki.parser.tokenheading import HeadingFactory
from outwiker.pages.wiki.parser.tokenadhoc import AdHocFactory
from outwiker.pages.wiki.parser.tokenhorline import HorLineFactory
from outwiker.pages.wiki.parser.tokenlink import LinkFactory
from outwiker.pages.wiki.parser.tokenalign import AlignFactory
from outwiker.pages.wiki.parser.tokentable import TableFactory
from outwiker.pages.wiki.parser.tokenurl import UrlFactory
from outwiker.pages.wiki.parser.tokenurlimage import UrlImageFactory
from outwiker.pages.wiki.parser.tokenattach import (AttachFactory,
                                                    AttachImagesFactory)
from outwiker.pages.wiki.parser.tokenlist import ListFactory
from outwiker.pages.wiki.parser.tokenlinebreak import LineBreakFactory
from outwiker.pages.wiki.parser.tokenlinejoin import LineJoinFactory
from outwiker.pages.wiki.parser.tokencommand import CommandFactory

from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class FakeParser:
    """
    Фальшивый парсер-заглушка
    """

    def __init__(self):
        pass

    def parseWikiMarkup(self, text):
        return ""

    def parseTextLevelMarkup(self, text):
        return ""


class TokenNamesTest(unittest.TestCase):
    """
    Тесты токенов википарсера на правильность имен
    """

    def setUp(self):
        self._application = Application()
        self.path = mkdtemp(prefix='Абырвалг абыр')

    def tearDown(self):
        removeDir(self.path)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.filesPath = "testdata/samplefiles/"

        self.wikiroot = createNotesTree(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["accept.png", "add.png", "anchor.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif",
                 "image.tiff", "image.gif",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png"]

        fullFilesPath = [os.path.join(self.filesPath, fname)
                         for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application)

    def _checkToken(self, testtoken, text, validname):
        tokens_result = testtoken.scanString(text)

        isOk = False
        for token in tokens_result:
            tokenname = token[0].getName()
            self.assertEqual(tokenname, validname)
            isOk = True

        self.assertTrue(isOk)

    def testLinkName1(self):
        testtoken = LinkFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[[бла-бла-бла -> http://jenyay.net]]"
        validname = "link"

        self._checkToken(testtoken, text, validname)

    def testLinkName2(self):
        testtoken = LinkFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[[http://jenyay.net | бла-бла-бла]]"
        validname = "link"

        self._checkToken(testtoken, text, validname)

    def testLinkName3(self):
        testtoken = LinkFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[[http://jenyay.net]]"
        validname = "link"

        self._checkToken(testtoken, text, validname)

    def testFontItalic(self):
        testtoken = FontsFactory.makeItalic(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "''Бла-бла-бла''"
        validname = "italic"

        self._checkToken(testtoken, text, validname)

    def testFontBold(self):
        testtoken = FontsFactory.makeBold(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'''Бла-бла-бла'''"
        validname = "bold"

        self._checkToken(testtoken, text, validname)

    def testFontBoldItalic(self):
        testtoken = FontsFactory.makeBoldItalic(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "''''Бла-бла-бла''''"
        validname = "bold_italic"

        self._checkToken(testtoken, text, validname)

    def testFontUnderline(self):
        testtoken = FontsFactory.makeUnderline(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "{+Бла-бла-бла+}"
        validname = "underline"

        self._checkToken(testtoken, text, validname)

    def testFontStrike(self):
        testtoken = FontsFactory.makeStrike(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "{-Бла-бла-бла-}"
        validname = "strike"

        self._checkToken(testtoken, text, validname)

    def testFontSubscript(self):
        testtoken = FontsFactory.makeSubscript(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'_Бла-бла-бла_'"
        validname = "subscript"

        self._checkToken(testtoken, text, validname)

    def testFontSuperscript(self):
        testtoken = FontsFactory.makeSuperscript(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'^Бла-бла-бла^'"
        validname = "superscript"

        self._checkToken(testtoken, text, validname)

    def testFontCode(self):
        testtoken = FontsFactory.makeCode(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "@@Бла-бла-бла@@"
        validname = "code"

        self._checkToken(testtoken, text, validname)

    def testFontSmall(self):
        testtoken = FontsFactory.makeSmall(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[-Бла-бла-бла-]"
        validname = "small"

        self._checkToken(testtoken, text, validname)

    def testFontBig(self):
        testtoken = FontsFactory.makeBig(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[+Бла-бла-бла+]"
        validname = "big"

        self._checkToken(testtoken, text, validname)

    def testQuote(self):
        testtoken = QuoteFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[>Бла-бла-бла<]"
        validname = "quote"

        self._checkToken(testtoken, text, validname)

    def testHeading(self):
        testtoken = HeadingFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "!! Бла-бла-бла"
        validname = "heading"

        self._checkToken(testtoken, text, validname)

    def testNoFormat(self):
        testtoken = NoFormatFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[=Бла-бла-бла=]"
        validname = "noformat"

        self._checkToken(testtoken, text, validname)

    def testPreFormat(self):
        testtoken = PreFormatFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "[@Бла-бла-бла@]"
        validname = "preformat"

        self._checkToken(testtoken, text, validname)

    def testHorline(self):
        testtoken = HorLineFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = """Бла-бла-бла
----"""
        validname = "horline"

        self._checkToken(testtoken, text, validname)

    def testAlignCenter(self):
        testtoken = AlignFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = """%center% Бла-бла-бла"""
        validname = "alignment"

        self._checkToken(testtoken, text, validname)

    def testAlignLeft(self):
        testtoken = AlignFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "%left% Бла-бла-бла"
        validname = "alignment"

        self._checkToken(testtoken, text, validname)

    def testAlignRight(self):
        testtoken = AlignFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "%right% Бла-бла-бла"
        validname = "alignment"

        self._checkToken(testtoken, text, validname)

    def testUrl(self):
        testtoken = UrlFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "http://jenyay.net"
        validname = "url"

        self._checkToken(testtoken, text, validname)

    def testUrlImage(self):
        testtoken = UrlImageFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "http://jenyay.net/image.png"
        validname = "image"

        self._checkToken(testtoken, text, validname)

    def testBoldSubscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "''''_Бла-бла-бла_''''"
        validname = "bold_subscript"

        self._checkToken(testtoken, text, validname)

    def testBoldSuperscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "''''^Бла-бла-бла^''''"
        validname = "bold_superscript"

        self._checkToken(testtoken, text, validname)

    def testItalicSubscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'''_Бла-бла-бла_'''"
        validname = "italic_subscript"

        self._checkToken(testtoken, text, validname)

    def testItalicSuperscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'''^Бла-бла-бла^'''"
        validname = "italic_superscript"

        self._checkToken(testtoken, text, validname)

    def testBoldItalicSubscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'''''_Бла-бла-бла_'''''"
        validname = "bold_italic_subscript"

        self._checkToken(testtoken, text, validname)

    def testBoldItalicSuperscript(self):
        testtoken = AdHocFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "'''''^Бла-бла-бла^'''''"
        validname = "bold_italic_superscript"

        self._checkToken(testtoken, text, validname)

    def testList1(self):
        testtoken = ListFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = """* Бла-бла-бла
** фвывфаыва
"""
        validname = "list"

        self._checkToken(testtoken, text, validname)

    def testList2(self):
        testtoken = ListFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = """# Бла-бла-бла
## фвывфаыва
"""
        validname = "list"

        self._checkToken(testtoken, text, validname)

    def testTable(self):
        testtoken = TableFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = """||border=1
||Бла-бла-бла || asdfasdfsdaf ||
||Бла-бла-бла || asdfasdfsdaf ||"""
        validname = "table"

        self._checkToken(testtoken, text, validname)

    def testLineBreak1(self):
        testtoken = LineBreakFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "Бла-бла-бла [[<<]]"
        validname = "linebreak"

        self._checkToken(testtoken, text, validname)

    def testLineBreak2(self):
        testtoken = LineBreakFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "Бла-бла-бла [[&lt;&lt;]]"
        validname = "linebreak"

        self._checkToken(testtoken, text, validname)

    def testLineJoin(self):
        testtoken = LineJoinFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "Бла-бла-бла \\\ndfaadsfdasf"
        validname = "linejoin"

        self._checkToken(testtoken, text, validname)

    def testCommand(self):
        testtoken = CommandFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "(:command:)Бла-бла-бла(:commandend:)"
        validname = "command"

        self._checkToken(testtoken, text, validname)

    def testThumbnail(self):
        testtoken = ThumbnailFactory.make(FakeParser()).setParseAction(
            lambda s, l, t: None)
        text = "%thumb%Attach:fname.png%%"
        validname = "thumbnail"

        self._checkToken(testtoken, text, validname)

    def testAttachmentSimple(self):
        self.__createWiki()
        testtoken = AttachFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = "бла-бла-бла Attach:xxx.tmp ыфваыфвафв"
        validname = "attach"

        self._checkToken(testtoken, text, validname)

    def testAttachmentSingleQuotes(self):
        self.__createWiki()
        testtoken = AttachFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = "бла-бла-бла Attach:'xxx.tmp' ыфваыфвафв"
        validname = "attach"

        self._checkToken(testtoken, text, validname)

    def testAttachmentDoubleQuotes(self):
        self.__createWiki()
        testtoken = AttachFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = 'бла-бла-бла Attach:"xxx.tmp" ыфваыфвафв'
        validname = "attach"

        self._checkToken(testtoken, text, validname)

    def testAttachmentWithSpace(self):
        self.__createWiki()
        testtoken = AttachFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = "бла-бла-бла Attach:'файл с пробелами.tmp' ыфваыфвафв"
        validname = "attach"

        self._checkToken(testtoken, text, validname)

    def testImageAttachmentSimple(self):
        self.__createWiki()
        testtoken = AttachImagesFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = "бла-бла-бла Attach:image.jpg ыфваыфвафв"
        validname = "attachImage"

        self._checkToken(testtoken, text, validname)

    def testImageAttachmentSingleQuotes(self):
        self.__createWiki()
        testtoken = AttachImagesFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = "бла-бла-бла Attach:'image.jpg' ыфваыфвафв"
        validname = "attachImage"

        self._checkToken(testtoken, text, validname)

    def testImageAttachmentDoubleQuotes(self):
        self.__createWiki()
        testtoken = AttachImagesFactory.make(self.parser).setParseAction(
            lambda s, l, t: None)
        text = 'бла-бла-бла Attach:"image.jpg" ыфваыфвафв'
        validname = "attachImage"

        self._checkToken(testtoken, text, validname)
