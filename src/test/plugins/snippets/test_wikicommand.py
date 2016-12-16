# -*- coding: UTF-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class WikiCommandTest(unittest.TestCase):
    def setUp(self):
        plugins_dir = [u"../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)
        self._createWiki()
        self._application = Application

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application.config)

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

    def test_content_invalid_01(self):
        text = u'(:snip:){% if %}(:snipend:)'
        result = self.parser.toHtml(text)
        self.assertNotIn(u'Traceback', result, result)
