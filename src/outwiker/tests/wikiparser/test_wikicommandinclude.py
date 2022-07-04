# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.basetestcases import BaseOutWikerMixin
from outwiker.tests.utils import removeDir


class WikiIncludeCommandTest(BaseOutWikerMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        self.encoding = "utf8"

        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        files = ["text_utf8.txt", "text utf8.txt", "text_utf8.txt2",
                 "image.gif", "текст_utf8.txt", "text_1251.txt", "html.txt",
                 "html_1251.txt", "wiki.txt"]

        fullFilesPath = [os.path.join(self.filesPath, fname)
                         for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def test_utf8_simple(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_utf8_single_quotes(self):
        text = """бла-бла-бла
(:include Attach:'text_utf8.txt' :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_utf8_double_quotes(self):
        text = """бла-бла-бла
(:include Attach:"text_utf8.txt" :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_utf8_file_with_spaces_single_quotes(self):
        text = """бла-бла-бла
(:include Attach:'text utf8.txt' :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_utf8_file_with_spaces_double_quotes(self):
        text = """бла-бла-бла
(:include Attach:"text utf8.txt" :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_unknown_params(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt param param1="www" :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_extension_with_number(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt2:)"""

        result_right = """бла-бла-бла
Текст2 в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_extension_with_number_unknown_params(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt2 param param1="www":)"""

        result_right = """бла-бла-бла
Текст2 в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_nonlatin_file_name_unknown_params(self):
        text = """бла-бла-бла
(:include Attach:текст_utf8.txt param param1="www":)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_nonlatin_file_name(self):
        text = """бла-бла-бла
(:include Attach:текст_utf8.txt :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_encoding_cp1251(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding=cp1251 :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_encoding_cp1251_attach_single_quotes(self):
        text = """бла-бла-бла
(:include Attach:'text_1251.txt' encoding=cp1251 :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_encoding_cp1251_attach_double_quotes(self):
        text = """бла-бла-бла
(:include Attach:"text_1251.txt" encoding=cp1251 :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_encoding_cp1251_encoding_double_quotes_spaces_around_equality(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding = "cp1251" :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_encoding_cp1251_encoding_double_quotes(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding="cp1251" :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_htmlescape_param(self):
        text = """бла-бла-бла (:include Attach:html.txt htmlescape:)"""

        result_right = """бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_htmlescape__encoding_params(self):
        text = """бла-бла-бла (:include Attach:html_1251.txt htmlescape encoding="cp1251":)"""

        result_right = """бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_wikiparse_param(self):
        text = """бла-бла-бла (:include Attach:wiki.txt wikiparse:)"""

        result_right = """бла-бла-бла <b>Этот текст содержит вики-нотацию</b>"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_invalid_file_1(self):
        text = """бла-бла-бла(:include Attach:text_utf8_1.txt :)"""

        result_right = """бла-бла-бла"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_invalid_file_2(self):
        text = """бла-бла-бла(:include Attach:image.gif :)"""

        result_right = """бла-бла-бла""" + "<b>Encoding error in file image.gif</b>"

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_invalid_file_with_encoding(self):
        text = """бла-бла-бла(:include Attach:image.gif encoding=base64 :)"""

        result_right = """бла-бла-бла""" + "<b>Encoding error in file image.gif</b>"

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_without_attach(self):
        text = """бла-бла-бла (:include text_utf8.txt :) абырвалг"""

        result_right = """бла-бла-бла  абырвалг"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_subdir(self):
        subdir = 'subdir'
        fname = 'text utf8.txt'

        text = """бла-бла-бла
(:include Attach:"{}/{}" :)""".format(subdir, fname)

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        attach_full_paths = [os.path.join(self.filesPath, fname)]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(attach_full_paths, subdir)

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_subdir_with_spaces_forward_slash(self):
        subdir = 'subdir with spaces'
        fname = 'text utf8.txt'

        text = """бла-бла-бла
(:include Attach:"{}/{}" :)""".format(subdir, fname)

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        attach_full_paths = [os.path.join(self.filesPath, fname)]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(attach_full_paths, subdir)

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def test_subdir_with_spaces_back_slash(self):
        subdir = 'subdir with spaces'
        fname = 'text utf8.txt'

        text = """бла-бла-бла
(:include Attach:"{}\\{}" :)""".format(subdir, fname)

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        attach_full_paths = [os.path.join(self.filesPath, fname)]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(attach_full_paths, subdir)

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)
