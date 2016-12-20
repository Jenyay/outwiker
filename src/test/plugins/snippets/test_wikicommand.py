# -*- coding: UTF-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.utilites.textfile import writeTextFile
from test.utils import removeDir


class SnippetsWikiCommandTest(unittest.TestCase):
    def setUp(self):
        plugins_dir = [u"../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)
        self._createWiki()
        self._application = Application

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application.config)

        from snippets.utils import getSnippetsDir
        root_snippets_dir = getSnippetsDir()

        # snippets dir for tests
        self._snippets_dir = os.path.join(root_snippets_dir, u'__test_snippets')
        os.mkdir(self._snippets_dir)

    def tearDown(self):
        self.loader.clear()
        self._application.wikiroot = None
        removeDir(self.path)
        removeDir(self._snippets_dir)

    def _createWiki(self):
        self.path = mkdtemp(prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]

    def test_empty(self):
        # from snippets.utils import getSnippetsDir
        # snippets_dir = getSnippetsDir()
        text = u'(:snip:)(:snipend:)'
        result_right = u''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_simple(self):
        text = u'(:snip:)Шаблон(:snipend:)'
        result_right = u'Шаблон'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_global_var_title(self):
        text = u'(:snip:){{__title}}(:snipend:)'
        result_right = u'Страница 1'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_01(self):
        text = u'(:snip var="Переменная":){{var}}(:snipend:)'
        result_right = u'Переменная'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_02(self):
        text = u'(:snip:){{var}}(:snipend:)'
        result_right = u''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_03(self):
        text = u'(:snip var2="Переменная":){{var}}(:snipend:)'
        result_right = u''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_include(self):
        text = u'(:snip:){% include "__test_snippets/included.tpl" %}(:snipend:)'
        fname = os.path.join(self._snippets_dir, u'included.tpl')
        writeTextFile(fname, u'Включенный текст')
        result_right = u'Включенный текст'

        result = self.parser.toHtml(text)

        self.assertEqual(result_right, result)

    def test_content_invalid_01(self):
        text = u'(:snip:){% if %}(:snipend:)'
        result = self.parser.toHtml(text)
        self.assertNotIn(u'Traceback', result, result)
        self.assertIn(u"<div class='__error'>", result)

    def test_content_invalid_02(self):
        text = u"(:snip:){% include '' %}(:snipend:)"
        result = self.parser.toHtml(text)
        self.assertNotIn(u'Traceback', result, result)
        self.assertIn(u"<div class='__error'>", result)

    def test_content_invalid_03(self):
        text = u"(:snip:){% include 'invalid.tpl' %}(:snipend:)"
        result = self.parser.toHtml(text)
        self.assertNotIn(u'Traceback', result, result)
        self.assertIn(u"<div class='__error'>", result)

    def test_file_empty_01(self):
        snippet_text = u''
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = u''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_empty_02(self):
        snippet_text = u''
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip.tpl":)(:snipend:)'
        result_right = u''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_simple(self):
        snippet_text = u'Текст шаблона'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip.tpl":)(:snipend:)'
        result_right = u'Текст шаблона'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_global_var_title_01(self):
        snippet_text = u'{{__title}}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip.tpl":)(:snipend:)'
        result_right = u'Страница 1'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_global_var_title_02(self):
        snippet_text = u'{{__title}}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = u'Страница 1'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_01(self):
        snippet_text = u'{{varname}}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip" varname="Переменная":)(:snipend:)'
        result_right = u'Переменная'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_02(self):
        snippet_text = u'{{varname}}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = u''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_03(self):
        snippet_text = u'{{__text}}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip":)Текст(:snipend:)'
        result_right = u'Текст'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_invalid(self):
        text = u'(:snip file="__test_snippets/invalid":)(:snipend:)'

        result = self.parser.toHtml(text)
        self.assertNotIn(u'Traceback', result, result)
        self.assertIn(u"<div class='__error'>", result)

    def test_file_include_01(self):
        snippet_text = u'{% include "included.tpl" %}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = u'Включение'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        snip_fname_full_2 = os.path.join(self._snippets_dir, u'included.tpl')
        writeTextFile(snip_fname_full_2, u'Включение')

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_include_02(self):
        snippet_text = u'{% include "included.tpl" %}'
        snippet_fname = u'testsnip.tpl'
        text = u'(:snip file="__test_snippets/testsnip" var="Переменная":)(:snipend:)'
        result_right = u'Переменная'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        snip_fname_full_2 = os.path.join(self._snippets_dir, u'included.tpl')
        writeTextFile(snip_fname_full_2, u'{{var}}')

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)
