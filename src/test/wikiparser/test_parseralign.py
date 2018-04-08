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


class ParserAlignTest (unittest.TestCase):
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

        files = ["accept.png", "add.png", "anchor.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif", "image.tiff", "image.gif",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png"]

        fullFilesPath = [
            os.path.join(
                self.filesPath,
                fname) for fname in files]

        self.attach_page2 = Attachment(self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        removeDir(self.path)

    def testCenter1(self):
        text = "бла-бла-бла \n%center%кхм бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<div align="center">кхм бла-бла-бла\nбла-бла-бла</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCenter2(self):
        text = "бла-бла-бла \n%center%кхм бла-бла-бла\n\nбла-бла-бла"
        result = 'бла-бла-бла \n<div align="center">кхм бла-бла-бла</div>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCenter3(self):
        text = "%center%бла-бла-бла \nкхм бла-бла-бла\n\nбла-бла-бла"
        result = '<div align="center">бла-бла-бла \nкхм бла-бла-бла</div>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCenter4(self):
        text = "%center%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '<div align="center">бла-бла-бла \n<b>кхм</b> бла-бла-бла</div>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCenter5(self):
        text = "бла-бла-бла \n\n% center %Attach:accept.png\n\nбла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n\n<div align="center"><img src="__attach/accept.png"/></div>\n\nбла-бла-бла\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testRight1(self):
        text = "бла-бла-бла \n% right %кхм бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<div align="right">кхм бла-бла-бла\nбла-бла-бла</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand1(self):
        text = "бла-бла-бла \n% right %(:command:)"
        result = 'бла-бла-бла \n<div align="right">(:command:)</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand2(self):
        text = "бла-бла-бла \n% right %(:command:)\nАбырвалг"
        result = 'бла-бла-бла \n<div align="right">(:command:)\nАбырвалг</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand3(self):
        text = "бла-бла-бла \n% right %Абырвалг (:command:)\nАбырвалг"
        result = 'бла-бла-бла \n<div align="right">Абырвалг (:command:)\nАбырвалг</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand4(self):
        text = "бла-бла-бла \n% right %(:command:) Абырвалг"
        result = 'бла-бла-бла \n<div align="right">(:command:) Абырвалг</div>'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand5(self):
        text = "бла-бла-бла \n% right %(:command:) Абырвалг\n\n111"
        result = 'бла-бла-бла \n<div align="right">(:command:) Абырвалг</div>\n\n111'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand6(self):
        text = "бла-бла-бла \n% right %(:command:)qqq\n\nwww\n(:commandend:) Абырвалг\n\n111"
        result = 'бла-бла-бла \n<div align="right">(:command:)qqq\n\nwww\n(:commandend:) Абырвалг</div>\n\n111'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand7(self):
        text = "бла-бла-бла \n% right %1111 (:command:)qqq\n\nwww\n(:commandend:) Абырвалг\n\n111"
        result = 'бла-бла-бла \n<div align="right">1111 (:command:)qqq\n\nwww\n(:commandend:) Абырвалг</div>\n\n111'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testCommand8(self):
        text = "бла-бла-бла \n%right%1111 (:command:)111\n\n222(:commandend:) Абырвалг (:command2:)333\n\n\n444(:command2end:)\n\n777"
        result = 'бла-бла-бла \n<div align="right">1111 (:command:)111\n\n222(:commandend:) Абырвалг (:command2:)333\n\n\n444(:command2end:)</div>\n\n777'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testLeft1(self):
        text = "%left%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '<div align="left">бла-бла-бла \n<b>кхм</b> бла-бла-бла</div>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testJustify1(self):
        text = "%justify%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '<div align="justify">бла-бла-бла \n<b>кхм</b> бла-бла-бла</div>\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testInvalidAlign1(self):
        text = "%invalid%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '%invalid%бла-бла-бла \n<b>кхм</b> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testInvalidAlign2(self):
        text = "%invalid center%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '%invalid center%бла-бла-бла \n<b>кхм</b> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))

    def testInvalidAlign3(self):
        text = "%center invalid%бла-бла-бла \n'''кхм''' бла-бла-бла\n\nбла-бла-бла"
        result = '%center invalid%бла-бла-бла \n<b>кхм</b> бла-бла-бла\n\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(
                self.encoding))
