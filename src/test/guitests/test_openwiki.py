# -*- coding: UTF-8 -*-

import os.path
from tempfile import mkdtemp

import wx

from basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.commands import openWikiWithDialog, openWiki, findPage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeDir


class OpenWikiGuiTest(BaseMainWndTest):
    """
    Тесты открытия вики через интерфейс
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)

        self.path2 = mkdtemp(prefix=u'Абырвалг абырвалг')

        factory = TextPageFactory()
        factory.create(self.wikiroot, u"Страница 1", [])
        factory.create(self.wikiroot, u"Страница 2", [])
        factory.create(self.wikiroot[u"Страница 2"], u"Страница 3", [])

        Tester.dialogTester.clear()

    def tearDown(self):
        BaseMainWndTest.tearDown(self)
        removeDir(self.path2)

    def _selectFile(self, dialog):
        fname = os.path.join(self.path, u"__page.opt")
        dialog.SetPathForTest(fname)
        return wx.ID_OK

    def _selectInvalidFile(self, dialog):
        fname = os.path.join(self.path, u"adsfadsas", u"__page.opt")
        dialog.SetPathForTest(fname)
        return wx.ID_OK

    def test_Open_01(self):
        Application.wikiroot = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(Application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.wikiroot[u"Страница 1"])
        self.assertFalse(Application.wikiroot.readonly)
        self.assertFalse(Application.wikiroot[u"Страница 1"].readonly)

    def test_Open_02(self):
        wikiroot2 = WikiDocument.create(self.path2)
        factory = TextPageFactory()
        factory.create(wikiroot2, u"Страница 1_2", [])
        factory.create(wikiroot2, u"Страница 2_2", [])

        Application.wikiroot = wikiroot2

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(Application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.wikiroot[u"Страница 1"])

    def test_Open_03(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(Application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.selectedPage)
        self.assertEqual(Application.selectedPage.title, u"Страница 3")

    def test_Open_04(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Application.wikiroot = None
        Application.selectedPage = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(Application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.selectedPage)
        self.assertEqual(Application.selectedPage.title, u"Страница 3")

    def test_Open_05(self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Tester.dialogTester.append(self._selectInvalidFile)
        Tester.dialogTester.appendOk()
        openWikiWithDialog(Application.mainWindow, False)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.selectedPage)
        self.assertEqual(Application.selectedPage.title, u"Страница 3")

    def test_Open_06(self):
        Application.wikiroot = None

        Tester.dialogTester.append(self._selectFile)
        openWikiWithDialog(Application.mainWindow, True)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNotNone(Application.wikiroot[u"Страница 1"])
        self.assertTrue(Application.wikiroot.readonly)
        self.assertTrue(Application.wikiroot[u"Страница 1"].readonly)

    def test_openwiki_01(self):
        Application.wikiroot = None
        openWiki(self.path)

        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNone(Application.selectedPage)

    def test_openwiki_02(self):
        Application.wikiroot = None
        openWiki(os.path.join(self.path, u"__page.opt"))

        self.assertIsNotNone(Application.wikiroot)
        self.assertIsNone(Application.selectedPage)

    def test_findPage_01(self):
        Application.wikiroot = None
        page = findPage(Application, None)

        self.assertIsNone(page)

    def test_findPage_02(self):
        Application.wikiroot = self.wikiroot
        page = findPage(Application, None)

        self.assertIsNone(page)

    def test_findPage_03(self):
        Application.wikiroot = self.wikiroot
        page = findPage(Application, u'Страница 1')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, u'Страница 1')

    def test_findPage_04(self):
        Application.wikiroot = self.wikiroot
        page = findPage(Application, u'Страница 2/Страница 3')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, u'Страница 3')

    def test_findPage_05(self):
        Application.wikiroot = self.wikiroot
        page = findPage(Application, u'/Страница 2/Страница 3')

        self.assertIsNotNone(page)
        self.assertEqual(page.title, u'Страница 3')

    def test_findPage_06(self):
        Application.wikiroot = self.wikiroot
        uid = Application.pageUidDepot.createUid(self.wikiroot[u'/Страница 2/Страница 3'])

        page = findPage(Application, uid)
        self.assertIsNotNone(page)
        self.assertEqual(page.title, u'Страница 3')

    def test_findPage_07(self):
        Application.wikiroot = self.wikiroot
        uid = Application.pageUidDepot.createUid(self.wikiroot[u'/Страница 2/Страница 3'])
        uid = u'page://' + uid

        page = findPage(Application, uid)
        self.assertIsNotNone(page)
        self.assertEqual(page.title, u'Страница 3')
