# -*- coding: UTF-8 -*-

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
        parser = SnippetParser(template, self._application)
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
        parser = SnippetParser(template, self._application)
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
        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)
        variables = parser.getVariables()

        self.assertEqual(result, right_result)
        self.assertEqual(variables, right_variables)

    def test_global_var_01(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__title}}'
        selectedText = u''
        vars = {}

        right_result = page.title

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_02(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__text}}'
        selectedText = u'Проверка'
        vars = {}

        right_result = u'Проверка'

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_03(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__subpath}}'
        selectedText = u''
        vars = {}

        right_result = page.subpath

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_04(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__attach}}'
        selectedText = u''
        vars = {}

        right_result = Attachment(page).getAttachPath(False)

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)
        self.assertTrue(os.path.exists(right_result))

    def test_global_var_05(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__folder}}'
        selectedText = u''
        vars = {}

        right_result = page.path

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_global_var_06(self):
        from snippets.snippetparser import SnippetParser
        page = self.testPage
        template = u'{{__pageid}}'
        selectedText = u''
        vars = {}

        right_result = self._application.pageUidDepot.createUid(page)

        parser = SnippetParser(template, self._application)
        result = parser.process(selectedText, page, **vars)

        self.assertEqual(result, right_result)

    def test_error_01(self):
        from snippets.snippetparser import SnippetParser
        from snippets.libs.jinja2 import TemplateError
        template = u'Переменная = {{переменная}}'
        selectedText = u''
        vars = {u'переменная': u'Проверка 123'}

        page = self.testPage
        parser = SnippetParser(template, self._application)

        self.assertRaises(TemplateError,
                          parser.process,
                          selectedText,
                          page,
                          **vars)

    def test_error_02(self):
        from snippets.snippetparser import SnippetParser
        from snippets.libs.jinja2 import TemplateError
        template = u'Переменная = {{переменная}}'

        parser = SnippetParser(template, self._application)

        self.assertRaises(TemplateError, parser.getVariables)
