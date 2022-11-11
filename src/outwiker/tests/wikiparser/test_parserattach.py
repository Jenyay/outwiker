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

        files = ["accept.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.webp", "image_01.JPG", "dir"]

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
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_simple_single_quotes(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_simple_double_quotes(self):
        fname = "filename.tmp"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_simple(self):
        fname = "accept.png"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_single_quotes(self):
        fname = "accept.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_double_quotes(self):
        fname = "accept.png"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_webp(self):
        fname = "image.webp"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_simple(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_single_quotes(self):
        fname = "filename.tmp"
        text = "бла-бла-бла \n[[Attach:'{}']] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_in_link_double_quotes(self):
        fname = "filename.tmp"
        text = 'бла-бла-бла \n[[Attach:"{}"]] бла-бла-бла\nбла-бла-бла'.format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_04(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_05(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_png_spaces(self):
        fname = "картинка с пробелами.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_07(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_08(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Attach:{} | Комментарий]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_09(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Attach:{} | Комментарий]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_10(self):
        fname = "accept.png"
        text = "бла-бла-бла \n[[Комментарий -> Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_11(self):
        fname = "файл с пробелами.tmp"
        text = "бла-бла-бла \n[[Комментарий -> Attach:{}]] бла-бла-бла\nбла-бла-бла".format(
            fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">Комментарий</a> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_jpg(self):
        fname = "image_01.JPG"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_13(self):
        fname = "dir.xxx"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_folder(self):
        fname = "dir"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_forward_slash(self):
        fname = "dir/subdir/subdir2/application.py"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_forward_slash_single_quotes(self):
        fname = "dir/subdir/subdir2/application.py"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_forward_slash_duoble_quotes(self):
        fname = "dir/subdir/subdir2/application.py"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_backslash(self):
        fname = "dir\\subdir\\subdir2\\application.py"
        fname_result = fname.replace('\\', '/')

        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname_result, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_backslash_single_quotes(self):
        fname = "dir\\subdir\\subdir2\\application.py"
        fname_result = fname.replace('\\', '/')

        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname_result, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_in_folder_backslash_duoble_quotes(self):
        fname = "dir\\subdir\\subdir2\\application.py"
        fname_result = fname.replace('\\', '/')

        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname_result, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_forward_slash(self):
        fname = "dir/subdir/subdir2/image.png"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_forward_slash_single_quotes(self):
        fname = "dir/subdir/subdir2/image.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_forward_slash_double_quotes(self):
        fname = "dir/subdir/subdir2/image.png"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_backslash(self):
        fname = "dir\\subdir\\subdir2\\image.png"
        text = "бла-бла-бла \nAttach:{} бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
                fname.replace('\\', '/'))

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_backslash_single_quotes(self):
        fname = "dir\\subdir\\subdir2\\image.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname.replace('\\', '/'))

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_subfolder_backslash_double_quotes(self):
        fname = "dir\\subdir\\subdir2\\image.png"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname.replace('\\', '/'))

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_with_spaces_in_folder_forward_slash_single_quotes(self):
        fname = "dir/subdir/subdir2/файл с пробелами.tmp"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_file_with_spaces_in_folder_forward_slash_double_quotes(self):
        fname = "dir/subdir/subdir2/файл с пробелами.tmp"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="__attach/{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            fname, fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_with_spaces_subfolder_forward_slash_single_quotes(self):
        fname = "dir/subdir/subdir2/картинка с пробелами.png"
        text = "бла-бла-бла \nAttach:'{}' бла-бла-бла\nбла-бла-бла".format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)

    def test_attach_image_with_spaces_subfolder_forward_slash_double_quotes(self):
        fname = "dir/subdir/subdir2/картинка с пробелами.png"
        text = 'бла-бла-бла \nAttach:"{}" бла-бла-бла\nбла-бла-бла'.format(fname)
        result = 'бла-бла-бла \n<img class="ow-image" src="__attach/{}"/> бла-бла-бла\nбла-бла-бла'.format(
            fname)

        self.assertEqual(self.parser.toHtml(text), result)
