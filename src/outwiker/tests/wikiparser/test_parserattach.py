# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class ParserAttachTest(unittest.TestCase):
    def setUp(self):
        self.filesPath = "testdata/samplefiles/"

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
                 "image.jpg", "image.jpeg", "image.png", "image.tif",
                 "image.tiff", "image.gif", "image.webp",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png"]

        fullFilesPath = [os.path.join(self.filesPath, fname)
                         for fname in files]

        self.attach_page2 = Attachment(self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        removeDir(self.path)

    def test_attach_simple(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_simple_single_quotes(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_simple_double_quotes(self):
        fname = "filename.tmp"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_simple(self):
        fname = "accept.png"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_single_quotes(self):
        fname = "accept.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_double_quotes(self):
        fname = "accept.png"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_webp(self):
        fname = "image.webp"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_simple(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_single_quotes(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \n[[Attach:'{}']] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_double_quotes(self):
        fname = "filename.tmp"
        text = 'бла-бла-бла \n[[Attach:"{}"]] бла-бла-бла\nбла-бла-бла'.format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_04(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_05(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_spaces(self):
        fname = "картинка с пробелами.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_07(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_08(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:{} | Комментарий]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_09(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:{} | Комментарий]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_10(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Комментарий -> Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_11(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Комментарий -> Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_jpg(self):
        fname = "image_01.JPG"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_13(self):
        fname = "dir.xxx"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_14(self):
        fname = "dir"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)
