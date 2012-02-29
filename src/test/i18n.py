#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import unittest

import outwiker.core.i18n


class I18nTest(unittest.TestCase):
    def setUp(self):
        self.path = "../test/locale"

    def testGetLang (self):
        langs = outwiker.core.i18n.getLanguages()
        self.assertEqual (len (langs), 3)
        index1 = langs.index ("ru_RU")
        index2 = langs.index ("en")

        self.assertRaises (ValueError, langs.index, "test")
    

    def testIsLang (self):
        self.assertTrue (outwiker.core.i18n.isLangDir (self.path, "ru") )
        self.assertFalse (outwiker.core.i18n.isLangDir (self.path, "test") )
        self.assertTrue (outwiker.core.i18n.isLangDir (self.path, "test2") )

