# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUIMixin


class HackPage_SetAliasTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.__createWiki()
        self.testPage = self.wikiroot["Страница 1"]

        dirlist = ["../plugins/hackpage"]

        self._loader = PluginsLoader(self.application)
        self._loader.load(dirlist)

        Tester.dialogTester.clear()

    def tearDown(self):
        Tester.dialogTester.clear()
        self.application.wikiroot = None

        removeDir(self.wikiroot.path)
        self._loader.clear()

        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def __createWiki(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

    def _setValue(self, dialog, value):
        dialog.Value = value
        return wx.ID_OK

    def test_set_alias_default_01(self):
        from hackpage.utils import setAliasWithDialog

        Tester.dialogTester.appendOk()

        setAliasWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_default_02(self):
        from hackpage.utils import setAliasWithDialog

        Tester.dialogTester.appendCancel()

        setAliasWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_01(self):
        from hackpage.utils import setAliasWithDialog

        alias = 'Псевдоним страницы'

        Tester.dialogTester.append(self._setValue, alias)

        setAliasWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, alias)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_02(self):
        from hackpage.utils import setAliasWithDialog

        alias = '   Псевдоним страницы   '

        Tester.dialogTester.append(self._setValue, alias)

        setAliasWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, alias)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_03(self):
        from hackpage.utils import setAliasWithDialog

        self.testPage.alias = 'Псевдоним страницы'

        Tester.dialogTester.append(self._setValue, '')

        setAliasWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)
