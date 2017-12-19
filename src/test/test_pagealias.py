# -*- coding: utf-8 -*-
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir


class PageAliasTest(unittest.TestCase):
    """
    Page alias tests
    """
    def setUp(self):
        self.updateCount = 0
        self.updateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        self.page = TextPageFactory().create(self.wikiroot, 'Страница 1', [])
        Application.wikiroot = self.wikiroot

        Application.onTreeUpdate += self._onTreeUpdate

    def tearDown(self):
        Application.onTreeUpdate -= self._onTreeUpdate
        Application.wikiroot = None
        removeDir(self.path)

    def _onTreeUpdate(self, sender):
        self.updateCount += 1
        self.updateSender = sender

    def _changeAlias(self, page, alias):
        page.alias = alias

    def test_default(self):
        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_alias_None(self):
        self.page.alias = None
        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_alias_empty(self):
        self.page.alias = ''
        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_alias_01(self):
        self.assertEqual(self.updateCount, 0)
        self.assertIsNone(self.updateSender)

        self.page.alias = 'Псевдоним'
        self.assertEqual(self.page.alias, 'Псевдоним')
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Псевдоним')

        self.assertEqual(self.updateCount, 1)
        self.assertEqual(self.updateSender, self.page)

    def test_alias_02(self):
        self.page.alias = 'Псевдоним'
        newwiki = WikiDocument.load(self.path)
        page = newwiki['Страница 1']

        self.assertEqual(page.alias, 'Псевдоним')
        self.assertEqual(page.title, 'Страница 1')
        self.assertEqual(page.display_title, 'Псевдоним')

    def test_alias_03(self):
        self.page.alias = 'Псевдоним'
        Application.wikiroot = None
        Application.wikiroot = self.wikiroot

        newwiki = WikiDocument.load(self.path)
        page = newwiki['Страница 1']

        self.assertEqual(page.alias, 'Псевдоним')
        self.assertEqual(page.title, 'Страница 1')
        self.assertEqual(page.display_title, 'Псевдоним')

    def test_alias_04(self):
        self.page.alias = 'Псевдоним'
        self.page.save()
        Application.wikiroot = None
        Application.wikiroot = self.wikiroot

        newwiki = WikiDocument.load(self.path)
        page = newwiki['Страница 1']

        self.assertEqual(page.alias, 'Псевдоним')
        self.assertEqual(page.title, 'Страница 1')
        self.assertEqual(page.display_title, 'Псевдоним')

    def test_alias_readonly_01(self):
        newwiki = WikiDocument.load(self.path, readonly=True)
        page = newwiki['Страница 1']

        self.assertRaises(ReadonlyException,
                          self._changeAlias,
                          page, 'Тест')

    def test_alias_readonly_02(self):
        self.page.alias = 'Псевдоним'

        newwiki = WikiDocument.load(self.path, readonly=True)
        page = newwiki['Страница 1']

        self.assertRaises(ReadonlyException,
                          self._changeAlias,
                          page, None)

    def test_alias_readonly_03(self):
        self.page.alias = 'Псевдоним'

        newwiki = WikiDocument.load(self.path, readonly=True)
        page = newwiki['Страница 1']

        self.assertRaises(ReadonlyException,
                          self._changeAlias,
                          page, '')

    def test_alias_readonly_04(self):
        self.page.alias = 'Псевдоним'

        newwiki = WikiDocument.load(self.path, readonly=True)
        page = newwiki['Страница 1']

        self.assertRaises(ReadonlyException,
                          self._changeAlias,
                          page, 'test')

    def test_display_title_rename_01(self):
        self.page.display_title = None
        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_display_title_rename_02(self):
        self.page.alias = 'Псевдоним'
        self.page.display_title = None

        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_display_title_rename_03(self):
        self.page.alias = 'Псевдоним'
        self.page.display_title = ''

        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Страница 1')

    def test_display_title_rename_04(self):
        self.page.alias = 'Псевдоним'
        self.page.display_title = 'Новый псевдоним'

        self.assertEqual(self.page.alias, 'Новый псевдоним')
        self.assertEqual(self.page.title, 'Страница 1')
        self.assertEqual(self.page.display_title, 'Новый псевдоним')

    def test_display_title_rename_05(self):
        self.page.alias = None
        self.page.display_title = 'Новый заголовок'

        self.assertIsNone(self.page.alias)
        self.assertEqual(self.page.title, 'Новый заголовок')
        self.assertEqual(self.page.display_title, 'Новый заголовок')
