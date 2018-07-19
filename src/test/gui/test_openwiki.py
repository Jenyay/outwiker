# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

import wx

from outwiker.core.tree import WikiDocument
from outwiker.core.commands import openWikiWithDialog, openWiki, findPage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUIMixin


class OpenWikiGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты открытия вики через интерфейс
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.path2 = mkdtemp(prefix='Абырвалг абырвалг')

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        removeDir(self.path2)

    def _selectFile(self, dialog):
        fname = os.path.join(self.wikiroot.path, "__page.opt")
        dialog.SetDataForTest(fname)
        return wx.ID_OK

    def _selectInvalidFile(self, dialog):
        fname = os.path.join(self.wikiroot.path, "adsfadsas", "__page.opt")
        dialog.SetDataForTest(fname)
        return wx.ID_OK

    def test_Open_01(self):
        self.application.wikiroot = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(self.application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.wikiroot["Страница 1"])
        self.assertFalse(self.application.wikiroot.readonly)
        self.assertFalse(self.application.wikiroot["Страница 1"].readonly)

    def test_Open_02(self):
        wikiroot2 = WikiDocument.create(self.path2)
        factory = TextPageFactory()
        factory.create(wikiroot2, "Страница 1_2", [])
        factory.create(wikiroot2, "Страница 2_2", [])

        self.application.wikiroot = wikiroot2

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(self.application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.wikiroot["Страница 1"])

    def test_Open_03(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(self.application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.selectedPage)
        self.assertEqual(self.application.selectedPage.title, "Страница 3")

    def test_Open_04(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        self.application.wikiroot = None
        self.application.selectedPage = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(self.application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.selectedPage)
        self.assertEqual(self.application.selectedPage.title, "Страница 3")

    def test_Open_05(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        Tester.dialogTester.append(self._selectInvalidFile)
        Tester.dialogTester.appendOk()
        openWikiWithDialog(self.application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.selectedPage)
        self.assertEqual(self.application.selectedPage.title, "Страница 3")

    def test_Open_06(self):
        self.application.wikiroot = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(self.application.mainWindow, True)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNotNone(self.application.wikiroot["Страница 1"])
        self.assertTrue(self.application.wikiroot.readonly)
        self.assertTrue(self.application.wikiroot["Страница 1"].readonly)

    def test_openwiki_01(self):
        self.application.wikiroot = None
        openWiki(self.wikiroot.path)

        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNone(self.application.selectedPage)

    def test_openwiki_02(self):
        self.application.wikiroot = None
        openWiki(os.path.join(self.wikiroot.path, "__page.opt"))

        self.assertIsNotNone(self.application.wikiroot)
        self.assertIsNone(self.application.selectedPage)

    def test_findPage_01(self):
        self.application.wikiroot = None
        page = findPage(self.application, None)

        self.assertIsNone(page)

    def test_findPage_02(self):
        self.application.wikiroot = self.wikiroot
        page = findPage(self.application, None)

        self.assertIsNone(page)

    def test_findPage_03(self):
        self.application.wikiroot = self.wikiroot
        page = findPage(self.application, 'Страница 1')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, 'Страница 1')

    def test_findPage_04(self):
        self.application.wikiroot = self.wikiroot
        page = findPage(self.application, 'Страница 2/Страница 3')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, 'Страница 3')

    def test_findPage_05(self):
        self.application.wikiroot = self.wikiroot
        page = findPage(self.application, '/Страница 2/Страница 3')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, 'Страница 3')

    def test_findPage_06(self):
        self.application.wikiroot = self.wikiroot
        uid = self.application.pageUidDepot.createUid(self.wikiroot['/Страница 2/Страница 3'])

        page = findPage(self.application, uid)
        self.assertIsNotNone(page)
        self.assertEqual(page.title, 'Страница 3')

    def test_findPage_07(self):
        self.application.wikiroot = self.wikiroot
        uid = self.application.pageUidDepot.createUid(self.wikiroot['/Страница 2/Страница 3'])
        uid = 'page://' + uid

        page = findPage(self.application, uid)
        self.assertIsNotNone(page)
        self.assertEqual(page.title, 'Страница 3')
