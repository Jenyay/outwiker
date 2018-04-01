# -*- coding: utf-8 -*-

from datetime import datetime
import os
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class SnippetParserTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])
        plugins_dir = ["../plugins/snippets"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(plugins_dir)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.testPage

    def tearDown(self):
        self.application.wikiroot = None
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_empty(self):
        from snippets.snippetparser import SnippetParser
        template = ''
        selectedText = ''
        vars = {}

        right_result = ''
        right_variables = set()

        page = self.testPage
        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_simple(self):
        from snippets.snippetparser import SnippetParser
        template = 'Проверка 123'
        selectedText = ''
        vars = {}

        right_result = 'Проверка 123'
        right_variables = set()

        page = self.testPage
        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_01(self):
        from snippets.snippetparser import SnippetParser
        template = '{{varname}}'
        selectedText = ''
        vars = {'varname': 'Проверка 123'}

        right_result = 'Проверка 123'
        right_variables = {'varname'}

        page = self.testPage
        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_02(self):
        from snippets.snippetparser import SnippetParser
        template = '{{varname}}'
        selectedText = ''
        vars = {
            'varname': 'Проверка 123',
            'varname_2': 'Абырвалг',
        }

        right_result = 'Проверка 123'
        right_variables = {'varname'}

        page = self.testPage
        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_03(self):
        from snippets.snippetparser import SnippetParser
        template = 'Проверка: {{varname}}'
        selectedText = ''
        vars = {}

        right_result = 'Проверка: '
        right_variables = {'varname'}

        page = self.testPage
        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_include_01(self):
        from snippets.snippetparser import SnippetParser
        template = '{{varname}} {% include "included" %}'
        selectedText = ''
        vars = {
            'varname': 'Проверка 123',
            'var_inc': 'Абырвалг',
        }

        right_result = 'Проверка 123 Включенный шаблон Абырвалг'
        right_variables = {'varname', 'var_inc'}

        page = self.testPage
        parser = SnippetParser(template,
                               '../test/snippets',
                               self.application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_global_var_title(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__title}}'
        selectedText = ''
        vars = {}

        right_result = page.title

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_text(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__text}}'
        selectedText = 'Проверка'
        vars = {}

        right_result = 'Проверка'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_subpath(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__subpath}}'
        selectedText = ''
        vars = {}

        right_result = page.subpath

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_attach(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__attach}}'
        selectedText = ''
        vars = {}

        right_result = Attachment(page).getAttachPath(False)

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)
        self.assertTrue(os.path.exists(right_result))

    def test_global_var_folder(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__folder}}'
        selectedText = ''
        vars = {}

        right_result = page.path

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_pageid(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__pageid}}'
        selectedText = ''
        vars = {}

        right_result = self.application.pageUidDepot.createUid(page)

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_eddate(self):
        from snippets.snippetparser import SnippetParser
        date = datetime(2016, 12, 9, 14, 23)
        page = self.testPage
        page.datetime = date
        template = '{{__eddate}}'
        selectedText = ''
        vars = {}

        right_result = str(date)

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_crdate(self):
        from snippets.snippetparser import SnippetParser
        date = datetime(2016, 12, 9, 14, 0)
        page = self.testPage
        page.creationdatetime = date
        template = '{{__crdate}}'
        selectedText = ''
        vars = {}

        right_result = str(date)

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_01(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = ['проверка', 'test', 'тест']
        template = '{{__tags}}'
        selectedText = ''
        vars = {}

        right_result = 'test, проверка, тест'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_02(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = ['проверка', 'test', 'тест']
        template = '{% for tag in __tags %}{{tag}}---{% endfor %}'
        selectedText = ''
        vars = {}

        right_result = 'test---проверка---тест---'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_03_empty(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = []
        template = '{{__tags}}'
        selectedText = ''
        vars = {}

        right_result = ''

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_childlist_01(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        WikiPageFactory().create(page, "Страница 1", [])
        WikiPageFactory().create(page, "Страница 2", [])
        WikiPageFactory().create(page, "Страница 3", [])

        template = '{{__childlist}}'
        selectedText = ''
        vars = {}

        right_result = 'Страница 1, Страница 2, Страница 3'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_childlist_02(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        subpage1 = WikiPageFactory().create(page, "Страница 1", [])
        subpage2 = WikiPageFactory().create(page, "Страница 2", [])
        subpage3 = WikiPageFactory().create(page, "Страница 3", [])

        subpage2.order = 1
        subpage3.order = 4
        subpage1.order = 10

        template = '{{__childlist}}'
        selectedText = ''
        vars = {}

        right_result = 'Страница 2, Страница 3, Страница 1'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_type(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = '{{__type}}'
        selectedText = ''
        vars = {}

        right_result = 'wiki'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_attachilist(self):
        from snippets.snippetparser import SnippetParser
        fnames = ['ccc.png', 'aaa.tmp', 'zzz.doc']
        page = self.testPage
        attachdir = Attachment(page).getAttachPath(True)
        for fname in fnames:
            fullpath = os.path.join(attachdir, fname)
            with open(fullpath, 'w'):
                pass

        page = self.testPage
        template = '{{__attachlist}}'
        selectedText = ''
        vars = {}

        right_result = 'aaa.tmp, ccc.png, zzz.doc'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_unicode_01(self):
        from snippets.snippetparser import SnippetParser

        page = self.testPage
        template = 'Переменная = {{переменная}}'
        selectedText = ''
        vars = {'переменная': 'Проверка 123'}
        right_result = 'Переменная = Проверка 123'

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        self.assertEqual(result, right_result)

    def test_unicode_02(self):
        from snippets.snippetparser import SnippetParser
        template = 'Переменная = {{переменная}}'
        right_result = 'Переменная = '
        selectedText = ''
        page = self.testPage
        vars = {}

        parser = SnippetParser(template, '.', self.application)
        result = parser.process(selectedText, page, **vars)
        self.assertEqual(result, right_result)
