# -*- coding: UTF-8 -*-

import wx

from .basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.commands import createNewWiki
from outwiker.gui.tester import Tester
from test.utils import removeDir


class NewWikiGuiTest (BaseMainWndTest):
    """
    Тесты создания вики через интерфейс
    """
    def setUp (self):
        super (NewWikiGuiTest, self).setUp()
        removeDir (self.path)


    def _selectFile (self, dialog):
        dialog.SetPathForTest (self.path)
        return wx.ID_OK


    def testCreate_01 (self):
        Tester.dialogTester.append (self._selectFile)
        createNewWiki (Application.mainWindow)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertIsNotNone (Application.wikiroot)
        self.assertEqual (len (Application.wikiroot.children), 1)
        self.assertNotEqual (len (Application.wikiroot.children[0].content), 1)
        self.assertEqual (Application.wikiroot.children[0].getTypeString(), "wiki")
