# -*- coding: UTF-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.pages.wiki.parser.tokenfonts import FontsFactory
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
from outwiker.pages.wiki.parser.tokenattach import AttachFactory, AttachImagesFactory
from outwiker.pages.wiki.parser.tokenlist import ListFactory
from outwiker.pages.wiki.parser.tokenlinebreak import LineBreakFactory
from outwiker.pages.wiki.parser.tokenlinejoin import LineJoinFactory
from outwiker.pages.wiki.parser.tokentex import TexFactory
from outwiker.pages.wiki.parser.tokencommand import CommandFactory
from outwiker.pages.wiki.parser.tokentext import TextFactory

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class FakeParser (object):
    """
    Фальшивый парсер-заглушка
    """
    def __init__(self):
        pass


    def parseWikiMarkup (self, text):
        return u""


class TokenNamesTest (unittest.TestCase):
    """
    Тесты токенов википарсера на правильность имен
    """
    def setUp (self):
        self.path = mkdtemp (prefix=u'Абырвалг абыр')


    def tearDown (self):
        removeDir (self.path)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.filesPath = u"../test/samplefiles/"

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]

        files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp",
                 u"файл с пробелами.tmp", u"картинка с пробелами.png",
                 u"image.jpg", u"image.jpeg", u"image.png", u"image.tif", u"image.tiff", u"image.gif",
                 u"image_01.JPG", u"dir", u"dir.xxx", u"dir.png"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def _checkToken (self, testtoken, text, validname):
        tokens_result = testtoken.scanString (text)

        isOk = False
        for token in tokens_result:
            tokenname = token[0].getName()
            self.assertEqual (tokenname, validname)
            isOk = True

        self.assertTrue (isOk)


    def testLinkName1 (self):
        testtoken = LinkFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[[бла-бла-бла -> http://jenyay.net]]"
        validname = u"link"

        self._checkToken (testtoken, text, validname)


    def testLinkName2 (self):
        testtoken = LinkFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[[http://jenyay.net | бла-бла-бла]]"
        validname = u"link"

        self._checkToken (testtoken, text, validname)


    def testLinkName3 (self):
        testtoken = LinkFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[[http://jenyay.net]]"
        validname = u"link"

        self._checkToken (testtoken, text, validname)


    def testFontItalic (self):
        testtoken = FontsFactory.makeItalic (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"''Бла-бла-бла''"
        validname = u"italic"

        self._checkToken (testtoken, text, validname)


    def testFontBold (self):
        testtoken = FontsFactory.makeBold (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'''Бла-бла-бла'''"
        validname = u"bold"

        self._checkToken (testtoken, text, validname)


    def testFontBoldItalic (self):
        testtoken = FontsFactory.makeBoldItalic (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"''''Бла-бла-бла''''"
        validname = u"bold_italic"

        self._checkToken (testtoken, text, validname)


    def testFontUnderline (self):
        testtoken = FontsFactory.makeUnderline (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"{+Бла-бла-бла+}"
        validname = u"underline"

        self._checkToken (testtoken, text, validname)


    def testFontStrike (self):
        testtoken = FontsFactory.makeStrike (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"{-Бла-бла-бла-}"
        validname = u"strike"

        self._checkToken (testtoken, text, validname)


    def testFontSubscript (self):
        testtoken = FontsFactory.makeSubscript (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'_Бла-бла-бла_'"
        validname = u"subscript"

        self._checkToken (testtoken, text, validname)


    def testFontSuperscript (self):
        testtoken = FontsFactory.makeSuperscript (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'^Бла-бла-бла^'"
        validname = u"superscript"

        self._checkToken (testtoken, text, validname)


    def testFontCode (self):
        testtoken = FontsFactory.makeCode (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"@@Бла-бла-бла@@"
        validname = u"code"

        self._checkToken (testtoken, text, validname)


    def testFontSmall (self):
        testtoken = FontsFactory.makeSmall (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[-Бла-бла-бла-]"
        validname = u"small"

        self._checkToken (testtoken, text, validname)


    def testFontBig (self):
        testtoken = FontsFactory.makeBig (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[+Бла-бла-бла+]"
        validname = u"big"

        self._checkToken (testtoken, text, validname)


    def testHeading (self):
        testtoken = HeadingFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"!! Бла-бла-бла"
        validname = u"heading"

        self._checkToken (testtoken, text, validname)


    def testNoFormat (self):
        testtoken = NoFormatFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[=Бла-бла-бла=]"
        validname = u"noformat"

        self._checkToken (testtoken, text, validname)


    def testPreFormat (self):
        testtoken = PreFormatFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"[@Бла-бла-бла@]"
        validname = u"preformat"

        self._checkToken (testtoken, text, validname)


    def testHorline (self):
        testtoken = HorLineFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"""Бла-бла-бла
----"""
        validname = u"horline"

        self._checkToken (testtoken, text, validname)


    def testAlignCenter (self):
        testtoken = AlignFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"""%center% Бла-бла-бла"""
        validname = u"alignment"

        self._checkToken (testtoken, text, validname)


    def testAlignLeft (self):
        testtoken = AlignFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"%left% Бла-бла-бла"
        validname = u"alignment"

        self._checkToken (testtoken, text, validname)


    def testAlignRight (self):
        testtoken = AlignFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"%right% Бла-бла-бла"
        validname = u"alignment"

        self._checkToken (testtoken, text, validname)


    def testUrl (self):
        testtoken = UrlFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"http://jenyay.net"
        validname = u"url"

        self._checkToken (testtoken, text, validname)


    def testUrlImage (self):
        testtoken = UrlImageFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"http://jenyay.net/image.png"
        validname = u"image"

        self._checkToken (testtoken, text, validname)


    def testBoldSubscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"''''_Бла-бла-бла_''''"
        validname = u"bold_subscript"

        self._checkToken (testtoken, text, validname)


    def testBoldSuperscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"''''^Бла-бла-бла^''''"
        validname = u"bold_superscript"

        self._checkToken (testtoken, text, validname)


    def testItalicSubscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'''_Бла-бла-бла_'''"
        validname = u"italic_subscript"

        self._checkToken (testtoken, text, validname)


    def testItalicSuperscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'''^Бла-бла-бла^'''"
        validname = u"italic_superscript"

        self._checkToken (testtoken, text, validname)


    def testBoldItalicSubscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'''''_Бла-бла-бла_'''''"
        validname = u"bold_italic_subscript"

        self._checkToken (testtoken, text, validname)


    def testBoldItalicSuperscript (self):
        testtoken = AdHocFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"'''''^Бла-бла-бла^'''''"
        validname = u"bold_italic_superscript"

        self._checkToken (testtoken, text, validname)


    def testList1 (self):
        testtoken = ListFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"""* Бла-бла-бла
** фвывфаыва
"""
        validname = u"list"

        self._checkToken (testtoken, text, validname)


    def testList2 (self):
        testtoken = ListFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"""# Бла-бла-бла
## фвывфаыва
"""
        validname = u"list"

        self._checkToken (testtoken, text, validname)


    def testTable (self):
        testtoken = TableFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"""||border=1
||Бла-бла-бла || asdfasdfsdaf ||
||Бла-бла-бла || asdfasdfsdaf ||"""
        validname = u"table"

        self._checkToken (testtoken, text, validname)


    def testLineBreak1 (self):
        testtoken = LineBreakFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"Бла-бла-бла [[<<]]"
        validname = u"linebreak"

        self._checkToken (testtoken, text, validname)


    def testLineBreak2 (self):
        testtoken = LineBreakFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"Бла-бла-бла [[&lt;&lt;]]"
        validname = u"linebreak"

        self._checkToken (testtoken, text, validname)


    def testLineJoin (self):
        testtoken = LineJoinFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"Бла-бла-бла \\\ndfaadsfdasf"
        validname = u"linejoin"

        self._checkToken (testtoken, text, validname)


    def testTex (self):
        testtoken = TexFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"{$e^x$}"
        validname = u"tex"

        self._checkToken (testtoken, text, validname)


    def testCommand (self):
        testtoken = CommandFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"(:command:)Бла-бла-бла(:commandend:)"
        validname = u"command"

        self._checkToken (testtoken, text, validname)


    def testText (self):
        testtoken = TextFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"Бла бла бла"
        validname = u"text"

        self._checkToken (testtoken, text, validname)


    def testThumbnail (self):
        testtoken = ThumbnailFactory.make (FakeParser()).setParseAction(lambda s, l, t: None)
        text = u"%thumb%Attach:fname.png%%"
        validname = u"thumbnail"

        self._checkToken (testtoken, text, validname)


    def testAttachment (self):
        self.__createWiki()
        testtoken = AttachFactory.make (self.parser).setParseAction(lambda s, l, t: None)
        text = u"бла-бла-бла Attach:файл с пробелами.tmp ыфваыфвафв"
        validname = u"attach"

        self._checkToken (testtoken, text, validname)


    def testImageAttachment (self):
        self.__createWiki()
        testtoken = AttachImagesFactory.make (self.parser).setParseAction(lambda s, l, t: None)
        text = u"бла-бла-бла Attach:image.jpg ыфваыфвафв"
        validname = u"attach"

        self._checkToken (testtoken, text, validname)
