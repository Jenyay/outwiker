# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from test.basetestcases import BaseOutWikerGUIMixin


class LangListTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

        dirlist = ["../plugins/source"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        from source.langlist import LangList
        self._langlist = LangList()

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def test_all(self):
        self.assertIn('Ada', self._langlist.allNames())
        self.assertIn('HTML + Angular2', self._langlist.allNames())
        self.assertIn('1S', self._langlist.allNames())

    def test_getAllDesignations(self):
        self.assertEqual(self._langlist.getAllDesignations('Ada'),
                         ('ada', 'ada95', 'ada2005'))
        self.assertEqual(self._langlist.getAllDesignations('ANTLR'),
                         ('antlr',))

    def test_getAllDesignations_invalid(self):
        self.assertIsNone(self._langlist.getAllDesignations('adsfa asdfadf'))

    def test_getDesignation(self):
        self.assertEqual(self._langlist.getDesignation('Ada'), 'ada')
        self.assertEqual(self._langlist.getDesignation('ANTLR'), 'antlr')
        self.assertEqual(self._langlist.getDesignation('C++'), 'cpp')

    def test_getDesignation_invalid(self):
        self.assertIsNone(self._langlist.getDesignation('adfasdfaf'))

    def test_getLangName(self):
        self.assertEqual(self._langlist.getLangName('ada'), 'Ada')
        self.assertEqual(self._langlist.getLangName('ada2005'), 'Ada')
        self.assertEqual(self._langlist.getLangName('html+spitfire'),
                         'HTML+Cheetah')

    def test_getLangName_invalid(self):
        self.assertIsNone(self._langlist.getLangName('asdfadsfads'))
