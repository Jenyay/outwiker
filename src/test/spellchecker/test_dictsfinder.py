# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.spellchecker import DictsFinder
from test.utils import removeDir


class DictsFinderTest(unittest.TestCase):
    def setUp(self):
        self.tempDirList = []

    def tearDown(self):
        for tempdir in self.tempDirList:
            removeDir(tempdir)

        self.tempDirList = []

    def testGetLangEmpty(self):
        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getLangList(), [])

    def testGetLangSingleEmpty(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell'))
        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), [])

    def testGetLangSingle_01(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell'))
        self._createDict(self.tempDirList[0], "ru_RU")

        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), ["ru_RU"])

    def testGetLangSingle_02(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")

        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), ["ru_RU"])

    def testGetLangSingle_03(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")
        self._createDict(self.tempDirList[1], "ru_RU")

        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), ["ru_RU"])

    def testGetLangSingle_invalid_01(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell'))

        with open(os.path.join(self.tempDirList[0],
                               "ru_RU" + DictsFinder.dictExtensions[0]), "w"):
            pass

        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), [])

    def testGetLangSingle_invalid_02(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell'))

        with open(os.path.join(self.tempDirList[0],
                               "ru_RU" + DictsFinder.dictExtensions[1]), "w"):
            pass

        finder = DictsFinder(self.tempDirList)

        self.assertEqual(finder.getLangList(), [])

    def testGetLangSeveral_01(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell'))
        self._createDict(self.tempDirList[0], "ru_RU")
        self._createDict(self.tempDirList[0], "en_US")

        finder = DictsFinder(self.tempDirList)

        langs = finder.getLangList()
        langs.sort()

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testGetLangSeveral_02(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[1], "ru_RU")
        self._createDict(self.tempDirList[1], "en_US")

        finder = DictsFinder(self.tempDirList)

        langs = finder.getLangList()
        langs.sort()

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testGetLangSeveral_03(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")
        self._createDict(self.tempDirList[1], "en_US")

        finder = DictsFinder(self.tempDirList)

        langs = finder.getLangList()
        langs.sort()

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testGetLangSeveral_04(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")
        self._createDict(self.tempDirList[1], "ru_RU")
        self._createDict(self.tempDirList[1], "en_US")

        finder = DictsFinder(self.tempDirList)

        langs = finder.getLangList()
        langs.sort()

        self.assertEqual(langs, ["en_US", "ru_RU"])

    def testGetFolders_empty_01(self):
        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"), [])

    def testGetFolders_empty_02(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"), [])

    def testGetFolders_empty_03_invalid(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))

        with open(os.path.join(self.tempDirList[0],
                               "ru_RU" + DictsFinder.dictExtensions[0]), "w"):
            pass

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"), [])

    def testGetFolders_01(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self._createDict(self.tempDirList[0], "ru_RU")

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"),
                         [self.tempDirList[0]])

    def testGetFolders_02(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"),
                         [self.tempDirList[0]])

    def testGetFolders_03(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[0], "ru_RU")
        self._createDict(self.tempDirList[1], "ru_RU")

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"),
                         [self.tempDirList[0], self.tempDirList[1]])

    def testGetFolders_04(self):
        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 1'))
        self._createDict(self.tempDirList[0], "ru_RU")

        self.tempDirList.append(mkdtemp(prefix='Абырвалг spell 2'))
        self._createDict(self.tempDirList[1], "ru_RU")
        self._createDict(self.tempDirList[1], "en_US")

        finder = DictsFinder(self.tempDirList)
        self.assertEqual(finder.getFoldersForLang("ru_RU"),
                         [self.tempDirList[0], self.tempDirList[1]])
        self.assertEqual(finder.getFoldersForLang("en_US"),
                         [self.tempDirList[1]])

    def _createDict(self, path, lang):
        with open(os.path.join(path, lang + DictsFinder.dictExtensions[0]),
                  "w"):
            pass

        with open(os.path.join(path, lang + DictsFinder.dictExtensions[1]),
                  "w"):
            pass
