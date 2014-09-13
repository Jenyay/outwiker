# -*- coding: UTF-8 -*-

import os.path

import wx

from basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.commands import openWikiWithDialog
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeWiki


class OpenWikiGuiTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        self.path2 = u"../test/testwiki2"
        removeWiki (self.path)
        removeWiki (self.path2)

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])

        Tester.dialogTester.clear()


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.selectedPage = None
        Application.wikiroot = None
        removeWiki (self.path)
        removeWiki (self.path2)


    def _selectFile (self, dialog):
        fname = os.path.join (self.path, u"__page.opt")
        dialog.SetPathForTest (fname)
        return wx.ID_OK


    def _selectInvalidFile (self, dialog):
        fname = os.path.join (self.path, u"adsfadsas", u"__page.opt")
        dialog.SetPathForTest (fname)
        return wx.ID_OK


    def testOpen_01 (self):
        Application.wikiroot = None

        Tester.dialogTester.append (self._selectFile)
        openWikiWithDialog (Application.mainWindow, False)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.wikiroot[u"Страница 1"])
        self.assertFalse (Application.wikiroot.readonly)
        self.assertFalse (Application.wikiroot[u"Страница 1"].readonly)


    def testOpen_02 (self):
        wikiroot2 = WikiDocument.create (self.path2)
        factory = TextPageFactory()
        factory.create (wikiroot2, u"Страница 1_2", [])
        factory.create (wikiroot2, u"Страница 2_2", [])

        Application.wikiroot = wikiroot2

        Tester.dialogTester.append (self._selectFile)
        openWikiWithDialog (Application.mainWindow, False)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.wikiroot[u"Страница 1"])


    def testOpen_03 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Tester.dialogTester.append (self._selectFile)
        openWikiWithDialog (Application.mainWindow, False)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.selectedPage)
        self.assertEqual (Application.selectedPage.title, u"Страница 3")


    def testOpen_04 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Application.wikiroot = None
        Application.selectedPage = None

        Tester.dialogTester.append (self._selectFile)
        openWikiWithDialog (Application.mainWindow, False)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.selectedPage)
        self.assertEqual (Application.selectedPage.title, u"Страница 3")


    def testOpen_05 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Tester.dialogTester.append (self._selectInvalidFile)
        Tester.dialogTester.appendOk ()
        openWikiWithDialog (Application.mainWindow, False)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.selectedPage)
        self.assertEqual (Application.selectedPage.title, u"Страница 3")


    def testOpen_06 (self):
        Application.wikiroot = None

        Tester.dialogTester.append (self._selectFile)
        openWikiWithDialog (Application.mainWindow, True)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertIsNotNone (Application.wikiroot[u"Страница 1"])
        self.assertTrue (Application.wikiroot.readonly)
        self.assertTrue (Application.wikiroot[u"Страница 1"].readonly)
