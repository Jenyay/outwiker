# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp
import os.path
import shutil

from outwiker.core.spellchecker import SpellChecker, DictsFinder
from test.utils import removeDir


class SpellCheckerTest (unittest.TestCase):
    def setUp (self):
        self._pathToDicts = mkdtemp (prefix=u'Абырвалг spell')
        self._dictsSrc = u'spell'


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
        checker = SpellChecker ([u'ru_RU'], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_02 (self):
        checker = SpellChecker ([], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_03 (self):
        checker = SpellChecker ([], [self._pathToDicts])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testRu_01 (self):
        self._copyDict (u'ru_RU')
        checker = SpellChecker ([u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (u'ывпывапыяа'))
        self.assertFalse (checker.check (u'ёж'))


    def testInvalid_01 (self):
        self._copyDictFrom (u'en-US-абырвалг', u'../test/spell')
        SpellChecker ([u'en-US-абырвалг'], [self._pathToDicts])


    def testRu_yo_01 (self):
        self._copyDict (u'ru_YO')
        checker = SpellChecker ([u'ru_YO'], [self._pathToDicts])
        self.assertTrue (checker.check (u'ёж'))


    def testRuEn_01 (self):
        self._copyDict (u'ru_RU')
        self._copyDict (u'en_US')
        checker = SpellChecker ([u'ru_RU', u'en_US'], [self._pathToDicts])
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
        self._copyDict (u'ru_RU')
        checker = SpellChecker ([u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (word))

        checker.addToCustomDict (word)
        self.assertTrue (checker.check (word))

        checker2 = SpellChecker ([u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker2.check (word))
