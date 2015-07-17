# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.spellchecker import DictsFinder
from test.utils import removeDir


class DictsFinderTest (unittest.TestCase):
    def setUp (self):
        self.tempDirList = []


    def tearDown (self):
        for tempdir in self.tempDirList:
            removeDir (tempdir)

        self.tempDirList = []


    def testEmpty (self):
        finder = DictsFinder (self.tempDirList)
        self.assertEqual (finder.getLangList(), [])


    def testSingleEmpty (self):
        self.tempDirList.append (mkdtemp (prefix=u'Абырвалг spell'))
        finder = DictsFinder (self.tempDirList)

        self.assertEqual (finder.getLangList(), [])


    def testSingle (self):
        self.tempDirList.append (mkdtemp (prefix=u'Абырвалг spell'))
        self._createDict (self.tempDirList[0], u"ru_RU")

        finder = DictsFinder (self.tempDirList)

        self.assertEqual (finder.getLangList(), [u"ru_RU"])


    def testSingle_invalid_01 (self):
        self.tempDirList.append (mkdtemp (prefix=u'Абырвалг spell'))

        with open (os.path.join (self.tempDirList[0], "ru_RU" + DictsFinder.dictExtensions[0]), "w"):
            pass

        finder = DictsFinder (self.tempDirList)

        self.assertEqual (finder.getLangList(), [])


    def testSingle_invalid_02 (self):
        self.tempDirList.append (mkdtemp (prefix=u'Абырвалг spell'))

        with open (os.path.join (self.tempDirList[0], "ru_RU" + DictsFinder.dictExtensions[1]), "w"):
            pass

        finder = DictsFinder (self.tempDirList)

        self.assertEqual (finder.getLangList(), [])


    def _createDict (self, path, lang):
        with open (os.path.join (path, lang + DictsFinder.dictExtensions[0]), "w"):
            pass

        with open (os.path.join (path, lang + DictsFinder.dictExtensions[1]), "w"):
            pass
