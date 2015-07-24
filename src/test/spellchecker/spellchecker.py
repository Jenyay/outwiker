# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.spellchecker import SpellChecker


class SpellCheckerTest (unittest.TestCase):
    def setUp (self):
        self._pathToDicts = u'spell'


    def testEmpty_01 (self):
        checker = SpellChecker ([u'ru_RU'], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_02 (self):
        checker = SpellChecker ([], [])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testEmpty_03 (self):
        checker = SpellChecker ([], [self._pathToDicts])
        self.assertTrue (checker.check (u'ывпаывапыв'))


    def testRu_01 (self):
        checker = SpellChecker ([u'ru_RU'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertFalse (checker.check (u'ывпывапыяа'))
        self.assertFalse (checker.check (u'ёж'))


    def testInvalid_01 (self):
        SpellChecker ([u'en-US-абырвалг'], [u'../test/spell'])


    def testRu_yo_01 (self):
        checker = SpellChecker ([u'ru_YO'], [self._pathToDicts])
        self.assertFalse (checker.check (u'еж'))
        self.assertTrue (checker.check (u'ёж'))


    def testRuEn_01 (self):
        checker = SpellChecker ([u'ru_RU', u'en_US'], [self._pathToDicts])
        self.assertTrue (checker.check (u'Проверка'))
        self.assertTrue (checker.check (u'cat'))
        self.assertFalse (checker.check (u'ывпывапыяа'))
        self.assertFalse (checker.check (u'adfasdfasd'))
