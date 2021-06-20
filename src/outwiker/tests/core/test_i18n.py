# -*- coding: utf-8 -*-

import unittest

import outwiker.core.i18n


class I18nTest(unittest.TestCase):
    def setUp(self):
        self.path = "testdata/locale"

    def testGetLang(self):
        langs = outwiker.core.i18n.getLanguages()
        self.assertEqual(len(langs), 5)
        langs.index("de")
        langs.index("en")
        langs.index("ru")
        langs.index("sv")
        langs.index("uk")

        self.assertRaises(ValueError, langs.index, "test")

    def testIsLang(self):
        self.assertTrue(outwiker.core.i18n.isLangDir(self.path, "ru"))
        self.assertFalse(outwiker.core.i18n.isLangDir(self.path, "test"))
        self.assertTrue(outwiker.core.i18n.isLangDir(self.path, "test2"))
