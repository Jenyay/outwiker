# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.api.app.tree import createNewWiki
from outwiker.gui.tester import Tester
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class NewWikiGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты создания вики через интерфейс
    """

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        removeDir(self.wikiroot.path)

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _selectFile(self, dialog):
        dialog.SetDataForTest(self.wikiroot.path)
        return wx.ID_OK

    def testCreate_01(self):
        Tester.dialogTester.append(self._selectFile)
        createNewWiki(self.application.mainWindow)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertEqual(len(self.application.wikiroot.children), 1)
        self.assertNotEqual(len(self.application.wikiroot.children[0].content), 1)
        self.assertEqual(self.application.wikiroot.children[0].getTypeString(), "wiki")
