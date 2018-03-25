# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import createNewWiki
from outwiker.gui.tester import Tester
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUITest


class NewWikiGuiTest(BaseOutWikerGUITest):
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
        dialog.SetPathForTest(self.wikiroot.path)
        return wx.ID_OK

    def testCreate_01(self):
        Tester.dialogTester.append(self._selectFile)
        createNewWiki(self.application.mainWindow)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertIsNotNone(self.application.wikiroot)
        self.assertEqual(len(self.application.wikiroot.children), 1)
        self.assertNotEqual(len(self.application.wikiroot.children[0].content), 1)
        self.assertEqual(self.application.wikiroot.children[0].getTypeString(), "wiki")
