# -*- coding: UTF-8 -*-

from datetime import datetime
import os
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir


class SnippetParserTest(unittest.TestCase):
    def setUp(self):
        plugins_dir = [u"../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)
        self._createWiki()
        self._application = Application

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.testPage

    def tearDown(self):
        self._application.wikiroot = None
        removeDir(self.path)
        self.loader.clear()

    def _createWiki(self):
        self.path = mkdtemp(prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]

    def test_empty(self):
        from snippets.snippetparser import SnippetParser
        template = u''
        selectedText = u''
        vars = {}

        right_result = u''
        right_variables = set()

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_simple(self):
        from snippets.snippetparser import SnippetParser
        template = u'Проверка 123'
        selectedText = u''
        vars = {}

        right_result = u'Проверка 123'
        right_variables = set()

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_01(self):
        from snippets.snippetparser import SnippetParser
        template = u'{{varname}}'
        selectedText = u''
        vars = {u'varname': u'Проверка 123'}

        right_result = u'Проверка 123'
        right_variables = {u'varname'}

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_02(self):
        from snippets.snippetparser import SnippetParser
        template = u'{{varname}}'
        selectedText = u''
        vars = {
            u'varname': u'Проверка 123',
            u'varname_2': u'Абырвалг',
        }

        right_result = u'Проверка 123'
        right_variables = {u'varname'}

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_vars_03(self):
        from snippets.snippetparser import SnippetParser
        template = u'Проверка: {{varname}}'
        selectedText = u''
        vars = {}

        right_result = u'Проверка: '
        right_variables = {u'varname'}

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_include_01(self):
        from snippets.snippetparser import SnippetParser
        template = u'{{varname}} {% include "included.tpl" %}'
        selectedText = u''
        vars = {
            u'varname': u'Проверка 123',
            u'var_inc': u'Абырвалг',
        }

        right_result = u'Проверка 123 Включенный шаблон Абырвалг'
        right_variables = {u'varname', u'var_inc'}

        page = self.testPage
        parser = SnippetParser(template,
                               u'../test/snippets',
                               self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_global_var_title(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__title}}'
        selectedText = u''
        vars = {}

        right_result = page.title

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_text(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__text}}'
        selectedText = u'Проверка'
        vars = {}

        right_result = u'Проверка'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_subpath(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__subpath}}'
        selectedText = u''
        vars = {}

        right_result = page.subpath

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_attach(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__attach}}'
        selectedText = u''
        vars = {}

        right_result = Attachment(page).getAttachPath(False)

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)
        self.assertTrue(os.path.exists(right_result))

    def test_global_var_folder(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__folder}}'
        selectedText = u''
        vars = {}

        right_result = page.path

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_pageid(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__pageid}}'
        selectedText = u''
        vars = {}

        right_result = self._application.pageUidDepot.createUid(page)

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_eddate(self):
        from snippets.snippetparser import SnippetParser
        date = datetime(2016, 12, 9, 14, 23)
        page = self.testPage
        page.datetime = date
        template = u'{{__eddate}}'
        selectedText = u''
        vars = {}

        right_result = unicode(date)

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_crdate(self):
        from snippets.snippetparser import SnippetParser
        date = datetime(2016, 12, 9, 14, 0)
        page = self.testPage
        page.creationdatetime = date
        template = u'{{__crdate}}'
        selectedText = u''
        vars = {}

        right_result = unicode(date)

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_01(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = [u'проверка', u'test', u'тест']
        template = u'{{__tags}}'
        selectedText = u''
        vars = {}

        right_result = u'test, проверка, тест'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_02(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = [u'проверка', u'test', u'тест']
        template = u'{% for tag in __tags %}{{tag}}---{% endfor %}'
        selectedText = u''
        vars = {}

        right_result = u'test---проверка---тест---'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_tags_03_empty(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        page.tags = []
        template = u'{{__tags}}'
        selectedText = u''
        vars = {}

        right_result = u''

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_childlist_01(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        WikiPageFactory().create(page, u"Страница 1", [])
        WikiPageFactory().create(page, u"Страница 2", [])
        WikiPageFactory().create(page, u"Страница 3", [])

        template = u'{{__childlist}}'
        selectedText = u''
        vars = {}

        right_result = u'Страница 1, Страница 2, Страница 3'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_childlist_02(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        subpage1 = WikiPageFactory().create(page, u"Страница 1", [])
        subpage2 = WikiPageFactory().create(page, u"Страница 2", [])
        subpage3 = WikiPageFactory().create(page, u"Страница 3", [])

        subpage2.order = 1
        subpage3.order = 4
        subpage1.order = 10

        template = u'{{__childlist}}'
        selectedText = u''
        vars = {}

        right_result = u'Страница 2, Страница 3, Страница 1'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_type(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__type}}'
        selectedText = u''
        vars = {}

        right_result = u'wiki'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_attachilist(self):
        from snippets.snippetparser import SnippetParser
        fnames = [u'ccc.png', u'aaa.tmp', u'zzz.doc']
        page = self.testPage
        attachdir = Attachment(page).getAttachPath(True)
        for fname in fnames:
            fullpath = os.path.join(attachdir, fname)
            with open(fullpath, 'w'):
                pass

        page = self.testPage
        template = u'{{__attachlist}}'
        selectedText = u''
        vars = {}

        right_result = u'aaa.tmp, ccc.png, zzz.doc'

        parser = SnippetParser(template, u'.', self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_error_01(self):
        from snippets.snippetparser import SnippetParser
        from snippets.libs.jinja2 import TemplateError
        template = u'Переменная = {{переменная}}'
        selectedText = u''
        vars = {u'переменная': u'Проверка 123'}

        page = self.testPage
        parser = SnippetParser(template, u'.', self._application)

        self.assertRaises(TemplateError,
                          parser.process,
                          selectedText,
                          page,
                          **vars)

    def test_error_02(self):
        from snippets.snippetparser import SnippetParser
        from snippets.libs.jinja2 import TemplateError
        template = u'Переменная = {{переменная}}'

        parser = SnippetParser(template, u'.', self._application)

        self.assertRaises(TemplateError, parser.getVariables)
