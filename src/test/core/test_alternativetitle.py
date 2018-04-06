# -*- coding: utf-8 -*-

import unittest

from outwiker.core.commands import getAlternativeTitle


class AlternativeTitleTest(unittest.TestCase):
    '''
    Test for the outwiker.test.commands.getAlternativeTitle
    '''
    def test_empty_01(self):
        title = ''
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, '(1)')

    def test_empty_02(self):
        title = '     '
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, '(1)')

    def test_title_ok_01(self):
        title = 'Проверка'
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, title)

    def test_title_ok_02(self):
        title = 'Проверка тест'
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, title)

    def test_title_strip(self):
        title = '    Проверка тест    '
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка тест')

    def test_title_siblings_01(self):
        title = 'Проверка'
        siblings = ['Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_02(self):
        title = 'Проверка'
        siblings = ['Test', 'Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_03(self):
        title = 'Проверка   '
        siblings = ['Test', 'Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_04(self):
        title = '   Проверка'
        siblings = ['Test', 'Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_05(self):
        title = '   Проверка   '
        siblings = ['Test', 'Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_06(self):
        title = 'Проверка'
        siblings = ['Test', 'Проверка', 'Проверка (1)', 'Проверка (2)']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (3)')

    def test_title_siblings_07(self):
        title = 'Проверка'
        siblings = ['Test', 'проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (1)')

    def test_title_siblings_08(self):
        title = 'проверка'
        siblings = ['Test', 'Проверка']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'проверка (1)')

    def test_title_siblings_09(self):
        title = 'Проверка'
        siblings = ['Test', 'проверка', 'проверка (1)']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка (2)')

    def test_title_siblings_10(self):
        title = 'проверка'
        siblings = ['Test', 'Проверка', 'Проверка (1)']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'проверка (2)')

    def test_title_replace_siblings_01(self):
        title = 'Проверка:'
        siblings = ['Проверка_']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка_ (1)')

    def test_title_replace_siblings_02(self):
        title = 'Проверка:'
        siblings = ['Проверка_', 'Проверка_ (1)']

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка_ (2)')

    def test_title_replace_01(self):
        title = 'Проверка:'
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка_')

    def test_title_replace_02(self):
        title = 'Проверка ><|?*:"\\/#%'
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка ___________')

    def test_title_replace_03(self):
        title = 'Проверка ><|?*:"\\/#% test'
        siblings = []

        newtitle = getAlternativeTitle(title, siblings)
        self.assertEqual(newtitle, 'Проверка ___________ test')
