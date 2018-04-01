# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.actions.dates import (WikiDateCreationAction,
                                               WikiDateEditionAction)
from test.basetestcases import BaseOutWikerGUIMixin


class WikiDateActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for a inserting commands (:crdate:) and (:eddate:)
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        self._wikipage = self.wikiroot["Викистраница"]
        self._wikipage.content = ""

        self.application.wikiroot = self.wikiroot

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _savePage(self):
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

    def _setFormat(self, dialog):
        dialog.Value = "%d - %m - %Y"
        return wx.ID_OK

    def testCancelCrdate(self):
        Tester.dialogTester.appendCancel()
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateCreationAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "")

    def testCancelEddate(self):
        Tester.dialogTester.appendCancel()
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateEditionAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "")

    def testEmptyCrdate_01(self):
        Tester.dialogTester.appendOk()
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateCreationAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "(:crdate:)")

    def testEmptyEddate_01(self):
        Tester.dialogTester.appendOk()
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateEditionAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "(:eddate:)")

    def testSetFormatCrdate_01(self):
        Tester.dialogTester.append(self._setFormat)
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateCreationAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, '(:crdate format="%d - %m - %Y":)')

    def testSetFormatEddate_01(self):
        Tester.dialogTester.append(self._setFormat)
        self.application.selectedPage = self._wikipage
        self.application.actionController.getAction(WikiDateEditionAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, '(:eddate format="%d - %m - %Y":)')

    def testAppendCrdate_01(self):
        Tester.dialogTester.appendOk()
        text = "Абырвалг "
        self._wikipage.content = text

        self.application.selectedPage = self._wikipage
        self.application.mainWindow.pagePanel.pageView.codeEditor.SetSelection(len(text), len(text))

        self.application.actionController.getAction(WikiDateCreationAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "Абырвалг (:crdate:)")

    def testAppendEddate_01(self):
        Tester.dialogTester.appendOk()
        text = "Абырвалг "
        self._wikipage.content = text

        self.application.selectedPage = self._wikipage
        self.application.mainWindow.pagePanel.pageView.codeEditor.SetSelection(len(text), len(text))

        self.application.actionController.getAction(WikiDateEditionAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "Абырвалг (:eddate:)")

    def testReplaceCrdate_01(self):
        Tester.dialogTester.appendOk()
        text = "ЫЫЫ Абырвалг"
        self._wikipage.content = text

        self.application.selectedPage = self._wikipage
        self.application.mainWindow.pagePanel.pageView.codeEditor.SetSelection(0, 3)

        self.application.actionController.getAction(WikiDateCreationAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "(:crdate:) Абырвалг")

    def testReplaceEddate_01(self):
        Tester.dialogTester.appendOk()
        text = "ЫЫЫ Абырвалг"
        self._wikipage.content = text

        self.application.selectedPage = self._wikipage
        self.application.mainWindow.pagePanel.pageView.codeEditor.SetSelection(0, 3)

        self.application.actionController.getAction(WikiDateEditionAction.stringId).run(None)

        self._savePage()

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self._wikipage.content, "(:eddate:) Абырвалг")
