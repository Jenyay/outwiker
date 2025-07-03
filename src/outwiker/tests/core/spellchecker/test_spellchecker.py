# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp
import os.path
import shutil

from outwiker.core.spellchecker.spellchecker import SpellChecker
from outwiker.core.spellchecker.dictsfinder import DictsFinder
from outwiker.core.spellchecker.spellcheckersfactory import SpellCheckersFactory
from outwiker.tests.utils import removeDir


class SpellCheckerTest (unittest.TestCase):
    def setUp(self):
        self._pathToDicts = mkdtemp(prefix='tmp spell test')
        self._spellCheckerFactory = SpellCheckersFactory([self._pathToDicts])

        if not os.path.exists(self._pathToDicts):
            os.mkdir(self._pathToDicts)
        self._dictsSrc = os.path.join('src', 'outwiker', 'data', 'spell')

    def tearDown(self):
        removeDir(self._pathToDicts)

    def _copyDictFrom(self, lang, srcDictPath):
        fname_dic = os.path.join(srcDictPath, lang + ".dic")
        fname_aff = os.path.join(srcDictPath, lang + ".aff")

        shutil.copy(fname_dic, self._pathToDicts)
        shutil.copy(fname_aff, self._pathToDicts)

    def _copyDict(self, lang):
        self._copyDictFrom(lang, self._dictsSrc)

    def testEmpty_01(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker([], use_custom_dict=False)
        self.assertTrue(checker.check('ывпаывапыв'))

    def testRu_01(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        self.assertTrue(checker.check('Проверка'))
        self.assertFalse(checker.check('ывпывапыяа'))

    def testEn_01(self):
        self._copyDict('en_US')
        checker = self._spellCheckerFactory.getSpellChecker(['en_US'], use_custom_dict=False)
        self.assertTrue(checker.check('test'))
        self.assertFalse(checker.check('asdfasfffadsf'))

    def testEn_02(self):
        self._copyDict('en_US')
        checker = self._spellCheckerFactory.getSpellChecker(['en_US'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('  test   ')
        self.assertEqual(errors, [])

    def testNumbers_01(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True
        self.assertTrue(checker.check('ыяаывфафыа123'))

    def testNumbers_02(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = False
        self.assertFalse(checker.check('ыяаывфафыа123'))

    def testRu_yo_01(self):
        self._copyDict('ru_YO')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_YO'], use_custom_dict=False)
        self.assertTrue(checker.check('ёж'))

    def testRuEn_01(self):
        self._copyDict('ru_RU')
        self._copyDict('en_US')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU', 'en_US'], use_custom_dict=False)
        self.assertTrue(checker.check('Проверка'))
        self.assertTrue(checker.check('cat'))
        self.assertFalse(checker.check('ывпывапыяа'))
        self.assertFalse(checker.check('adfasdfasd'))

        finder = DictsFinder([self._pathToDicts])
        langs = sorted(finder.getLangList())

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testUserDict_01(self):
        word = 'ывпывапыяа'

        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=True)
        self.assertTrue(checker.check('Проверка'))
        self.assertFalse(checker.check(word))

        checker.addToCustomDict(word)
        self.assertTrue(checker.check(word))

        checker2 = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=True)
        self.assertTrue(checker2.check(word))

    def testUserDictNoLang(self):
        word = 'ывпывапыяа'

        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker([], use_custom_dict=True)

        self.assertFalse(checker.check(word))

        checker.addToCustomDict(word)
        self.assertTrue(checker.check(word))

        checker2 = self._spellCheckerFactory.getSpellChecker([], use_custom_dict=True)
        self.assertTrue(checker2.check(word))

    def testFindErrors_01(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True
        errors = checker.findErrors('')
        self.assertEqual(errors, [])

    def testFindErrors_02(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('  проверка   ')
        self.assertEqual(errors, [])

    def testFindErrors_03(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('ййй')
        self.assertEqual(errors, [('ййй', 0, 3)])

    def testFindErrors_04(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('ййй12')
        self.assertEqual(errors, [])

    def testFindErrors_05(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = False

        errors = checker.findErrors('ййй12')
        self.assertEqual(errors, [('ййй12', 0, 5)])

    def testFindErrors_06(self):
        self._copyDict('ru_RU')
        checker = self._spellCheckerFactory.getSpellChecker(['ru_RU'], use_custom_dict=False)
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('проверка ййй ээээ тест')
        self.assertEqual(errors, [('ййй', 9, 12), ('ээээ', 13, 17)])
