# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp
import os.path
import shutil

from outwiker.core.application import Application
from outwiker.core.spellchecker import SpellChecker, DictsFinder
from test.utils import removeDir


class SpellCheckerTest (unittest.TestCase):
    def setUp (self):
        self._pathToDicts = mkdtemp (prefix=u'Абырвалг spell')
        self._dictsSrc = u'spell'
        self._application = Application


    def tearDown (self):
        removeDir (self._pathToDicts)


    def _copyDictFrom (self, lang, srcDictPath):
        shutil.copy (os.path.join (srcDictPath, lang + ".dic"),
                     self._pathToDicts)
        shutil.copy (os.path.join (srcDictPath, lang + ".aff"),
                     self._pathToDicts)


    def _copyDict (self, lang):
        self._copyDictFrom (lang, self._dictsSrc)


    def testEmpty_01 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_02 (self):
        checker = SpellChecker (self._application, [], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_03 (self):
        checker = SpellChecker (self._application, [], [self._pathToDicts])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testRu_01 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (u'ывпывапыяа'))


    def testNumbers_01 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True
        self.assertTrue (checker.check (u'ыяаывфафыа123'))


    def testNumbers_02 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = False
        self.assertFalse (checker.check (u'ыяаывфафыа123'))


    def testInvalid_01 (self):
        self._copyDictFrom (u'en-US-абырвалг', u'../test/spell')
        SpellChecker (self._application, [u'en-US-абырвалг'], [self._pathToDicts])


    def testRu_yo_01 (self):
        self._copyDict (u'ru_YO')
        checker = SpellChecker (self._application, [u'ru_YO'], [self._pathToDicts])
        self.assertTrue (checker.check (u'ёж'))


    def testRuEn_01 (self):
        self._copyDict (u'ru_RU')
        self._copyDict (u'en_US')
        checker = SpellChecker (self._application, [u'ru_RU', u'en_US'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertTrue (checker.check (u'cat'))
        self.assertFalse (checker.check (u'ывпывапыяа'))
        self.assertFalse (checker.check (u'adfasdfasd'))

        finder = DictsFinder ([self._pathToDicts])
        langs = finder.getLangList()
        langs.sort()

        self.assertEqual (langs, [u"en_US", u"ru_RU"])


    def testUserDict_01 (self):
        word = u'ывпывапыяа'
        dictname = u'mydict.dic'

        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (word))

        checker.addCustomDict (os.path.join (self._pathToDicts, dictname))
        checker.addToCustomDict (0, word)
        self.assertTrue (checker.check (word))

        checker2 = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker2.addCustomDict (os.path.join (self._pathToDicts, dictname))
        self.assertTrue (checker2.check (word))


    def testUserDict_02 (self):
        word = u'ывпывапыяа'
        dictname1 = u'mydict_1.dic'
        dictname2 = u'mydict_2.dic'

        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (word))

        checker.addCustomDict (os.path.join (self._pathToDicts, dictname1))
        checker.addCustomDict (os.path.join (self._pathToDicts, dictname2))
        checker.addToCustomDict (1, word)
        self.assertTrue (checker.check (word))

        checker2 = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker2.addCustomDict (os.path.join (self._pathToDicts, dictname1))
        self.assertFalse (checker2.check (word))

        checker3 = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker3.addCustomDict (os.path.join (self._pathToDicts, dictname2))
        self.assertTrue (checker3.check (word))


    def testFindErrors_01 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True
        errors = checker.findErrors (u'')
        self.assertEqual (errors, [])


    def testFindErrors_02 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors (u'  проверка   ')
        self.assertEqual (errors, [])


    def testFindErrors_03 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors (u'ййй')
        self.assertEqual (errors, [(u'ййй', 0, 3)])


    def testFindErrors_04 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors (u'ййй12')
        self.assertEqual (errors, [])


    def testFindErrors_05 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = False

        errors = checker.findErrors (u'ййй12')
        self.assertEqual (errors, [(u'ййй12', 0, 5)])


    def testFindErrors_06 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker (self._application, [u'ru_RU'], [self._pathToDicts])
        checker.skipWordsWithNumbers = True

        errors = checker.findErrors (u'проверка ййй ээээ тест')
        self.assertEqual (errors, [(u'ййй', 9, 12), (u'ээээ', 13, 17)])
