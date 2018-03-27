# -*- coding: utf-8 -*-

import os

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.utilites.textfile import writeTextFile
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUITest


class SnippetsWikiCommandTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])
        plugins_dir = ["../plugins/snippets"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(plugins_dir)

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self.application.config)

        from snippets.utils import getSnippetsDir
        root_snippets_dir = getSnippetsDir()

        # snippets dir for tests
        self._snippets_dir = os.path.join(
            root_snippets_dir, '__test_snippets')
        os.mkdir(self._snippets_dir)

    def tearDown(self):
        self.loader.clear()
        self.application.wikiroot = None
        removeDir(self._snippets_dir)
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_empty(self):
        # from snippets.utils import getSnippetsDir
        # snippets_dir = getSnippetsDir()
        text = '(:snip:)(:snipend:)'
        result_right = ''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_simple(self):
        text = '(:snip:)Шаблон(:snipend:)'
        result_right = 'Шаблон'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_global_var_title(self):
        text = '(:snip:){{__title}}(:snipend:)'
        result_right = 'Страница 1'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_01(self):
        text = '(:snip var="Переменная":){{var}}(:snipend:)'
        result_right = 'Переменная'

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_02(self):
        text = '(:snip:){{var}}(:snipend:)'
        result_right = ''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_var_03(self):
        text = '(:snip var2="Переменная":){{var}}(:snipend:)'
        result_right = ''

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def test_content_include(self):
        text = '(:snip:){% include "__test_snippets/included" %}(:snipend:)'
        fname = os.path.join(self._snippets_dir, 'included')
        writeTextFile(fname, 'Включенный текст')
        result_right = 'Включенный текст'

        result = self.parser.toHtml(text)

        self.assertEqual(result_right, result)

    def test_content_invalid_01(self):
        text = '(:snip:){% if %}(:snipend:)'
        result = self.parser.toHtml(text)
        self.assertNotIn('Traceback', result, result)
        self.assertIn("<div class='__error'>", result)

    def test_content_invalid_02(self):
        text = "(:snip:){% include '' %}(:snipend:)"
        result = self.parser.toHtml(text)
        self.assertNotIn('Traceback', result, result)
        self.assertIn("<div class='__error'>", result)

    def test_content_invalid_03(self):
        text = "(:snip:){% include 'invalid' %}(:snipend:)"
        result = self.parser.toHtml(text)
        self.assertNotIn('Traceback', result, result)
        self.assertIn("<div class='__error'>", result)

    def test_file_empty_01(self):
        snippet_text = ''
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = ''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_empty_02(self):
        snippet_text = ''
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = ''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_simple(self):
        snippet_text = 'Текст шаблона'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = 'Текст шаблона'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_global_var_title_01(self):
        snippet_text = '{{__title}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = 'Страница 1'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_global_var_title_02(self):
        snippet_text = '{{__title}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = 'Страница 1'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_global_var_title_alias(self):
        self.testPage.alias = 'Псевдоним'
        snippet_text = '{{__title}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = 'Псевдоним'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_01(self):
        snippet_text = '{{varname}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip" varname="Переменная":)(:snipend:)'
        result_right = 'Переменная'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_02(self):
        snippet_text = '{{varname}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = ''

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_var_03(self):
        snippet_text = '{{__text}}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)Текст(:snipend:)'
        result_right = 'Текст'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_invalid(self):
        text = '(:snip file="__test_snippets/invalid":)(:snipend:)'

        result = self.parser.toHtml(text)
        self.assertNotIn('Traceback', result, result)
        self.assertIn("<div class='__error'>", result)

    def test_file_include_01(self):
        snippet_text = '{% include "included" %}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip":)(:snipend:)'
        result_right = 'Включение'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        snip_fname_full_2 = os.path.join(self._snippets_dir, 'included')
        writeTextFile(snip_fname_full_2, 'Включение')

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def test_file_include_02(self):
        snippet_text = '{% include "included" %}'
        snippet_fname = 'testsnip'
        text = '(:snip file="__test_snippets/testsnip" var="Переменная":)(:snipend:)'
        result_right = 'Переменная'

        snip_fname_full = os.path.join(self._snippets_dir, snippet_fname)
        writeTextFile(snip_fname_full, snippet_text)

        snip_fname_full_2 = os.path.join(self._snippets_dir, 'included')
        writeTextFile(snip_fname_full_2, '{{var}}')

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)
