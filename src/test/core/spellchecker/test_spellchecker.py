# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp
import os.path
import shutil

from outwiker.core.spellchecker.spellchecker import SpellChecker
from outwiker.core.spellchecker.dictsfinder import DictsFinder
from test.utils import removeDir


class SpellCheckerTest (unittest.TestCase):
    def setUp(self):
        self._pathToDicts = mkdtemp(prefix='tmp spell test')

        if not os.path.exists(self._pathToDicts):
            os.mkdir(self._pathToDicts)
        self._dictsSrc = 'spell'

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
        checker = SpellChecker(['ru_RU'], [])
        self.assertTrue(checker.check('ывпаывапыв'))

    def testEmpty_02(self):
        checker = SpellChecker([], [])
        self.assertTrue(checker.check('ывпаывапыв'))

    def testEmpty_03(self):
        checker = SpellChecker([], [self._pathToDicts])
        self.assertTrue(checker.check('ывпаывапыв'))

    def testRu_01(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        self.assertTrue(checker.check('Проверка'))
        self.assertFalse(checker.check('ывпывапыяа'))

    def testEn_01(self):
        self._copyDict('en_US')
        checker = SpellChecker(['en_US'], [self._pathToDicts])
        self.assertTrue(checker.check('test'))
        self.assertFalse(checker.check('asdfasfffadsf'))

    def testEn_02(self):
        self._copyDict('en_US')
        checker = SpellChecker(['en_US'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('  test   ')
        self.assertEqual(errors, [])

    def testNumbers_01(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True
        self.assertTrue(checker.check('ыяаывфафыа123'))

    def testNumbers_02(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = False
        self.assertFalse(checker.check('ыяаывфафыа123'))

    def testInvalid_01(self):
        self._copyDictFrom('en-US-абырвалг', '../test/spell')
        SpellChecker(['en-US-абырвалг'], [self._pathToDicts])

    def testRu_yo_01(self):
        self._copyDict('ru_YO')
        checker = SpellChecker(['ru_YO'], [self._pathToDicts])
        self.assertTrue(checker.check('ёж'))

    def testRuEn_01(self):
        self._copyDict('ru_RU')
        self._copyDict('en_US')
        checker = SpellChecker(['ru_RU', 'en_US'], [self._pathToDicts])
        self.assertTrue(checker.check('Проверка'))
        self.assertTrue(checker.check('cat'))
        self.assertFalse(checker.check('ывпывапыяа'))
        self.assertFalse(checker.check('adfasdfasd'))

        finder = DictsFinder([self._pathToDicts])
        langs = sorted(finder.getLangList())

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testUserDict_01(self):
        word = 'ывпывапыяа'
        dictname = 'mydict.dic'

        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        self.assertTrue(checker.check('Проверка'))
        self.assertFalse(checker.check(word))

        checker.addCustomDict(os.path.join(self._pathToDicts, dictname))
        checker.addToCustomDict(0, word)
        self.assertTrue(checker.check(word))

        checker2 = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker2.addCustomDict(os.path.join(self._pathToDicts, dictname))
        self.assertTrue(checker2.check(word))

    def testUserDict_02(self):
        word = 'ывпывапыяа'
        dictname1 = 'mydict_1.dic'
        dictname2 = 'mydict_2.dic'

        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        self.assertTrue(checker.check('Проверка'))
        self.assertFalse(checker.check(word))

        checker.addCustomDict(os.path.join(self._pathToDicts, dictname1))
        checker.addCustomDict(os.path.join(self._pathToDicts, dictname2))
        checker.addToCustomDict(1, word)
        self.assertTrue(checker.check(word))

        checker2 = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker2.addCustomDict(os.path.join(self._pathToDicts, dictname1))
        self.assertFalse(checker2.check(word))

        checker3 = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker3.addCustomDict(os.path.join(self._pathToDicts, dictname2))
        self.assertTrue(checker3.check(word))

    def testFindErrors_01(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True
        errors = checker.findErrors('')
        self.assertEqual(errors, [])

    def testFindErrors_02(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('  проверка   ')
        self.assertEqual(errors, [])

    def testFindErrors_03(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('ййй')
        self.assertEqual(errors, [('ййй', 0, 3)])

    def testFindErrors_04(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('ййй12')
        self.assertEqual(errors, [])

    def testFindErrors_05(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = False

        errors = checker.findErrors('ййй12')
        self.assertEqual(errors, [('ййй12', 0, 5)])

    def testFindErrors_06(self):
        self._copyDict('ru_RU')
        checker = SpellChecker(['ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('проверка ййй ээээ тест')
        self.assertEqual(errors, [('ййй', 9, 12), ('ээээ', 13, 17)])

    def testFindErrors_07(self):
        checker = SpellChecker(['ru_RU'], ['spell'])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors('  проверка   ')
        self.assertEqual(errors, [])
