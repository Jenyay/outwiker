# -*- coding: UTF-8 -*-

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.actions.dates import WikiDateCreationAction, WikiDateEditionAction


class WikiDateActionTest (BaseMainWndTest):
    """
    Tests for a inserting commands (:crdate:) and (:eddate:)
    """
    def setUp (self):
        super (WikiDateActionTest, self).setUp()

        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])

        self._wikipage = self.wikiroot[u"Викистраница"]
        self._wikipage.content = u""

        Application.wikiroot = self.wikiroot


    def _savePage (self):
        Application.selectedPage = None
        Application.selectedPage = self._wikipage


    def _setFormat (self, dialog):
        dialog.Value = u"%d - %m - %Y"
        return wx.ID_OK


    def testCancelCrdate (self):
        Tester.dialogTester.appendCancel ()
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateCreationAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"")


    def testCancelEddate (self):
        Tester.dialogTester.appendCancel ()
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateEditionAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"")


    def testEmptyCrdate_01 (self):
        Tester.dialogTester.appendOk ()
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateCreationAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"(:crdate:)")


    def testEmptyEddate_01 (self):
        Tester.dialogTester.appendOk ()
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateEditionAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"(:eddate:)")


    def testSetFormatCrdate_01 (self):
        Tester.dialogTester.append (self._setFormat)
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateCreationAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u'(:crdate format="%d - %m - %Y":)')


    def testSetFormatEddate_01 (self):
        Tester.dialogTester.append (self._setFormat)
        Application.selectedPage = self._wikipage
        Application.actionController.getAction (WikiDateEditionAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u'(:eddate format="%d - %m - %Y":)')


    def testAppendCrdate_01 (self):
        Tester.dialogTester.appendOk ()
        text = u"Абырвалг "
        self._wikipage.content = text

        Application.selectedPage = self._wikipage
        Application.mainWindow.pagePanel.pageView.codeEditor.SetSelection (len (text), len (text))

        Application.actionController.getAction (WikiDateCreationAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"Абырвалг (:crdate:)")


    def testAppendEddate_01 (self):
        Tester.dialogTester.appendOk ()
        text = u"Абырвалг "
        self._wikipage.content = text

        Application.selectedPage = self._wikipage
        Application.mainWindow.pagePanel.pageView.codeEditor.SetSelection (len (text), len (text))

        Application.actionController.getAction (WikiDateEditionAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"Абырвалг (:eddate:)")


    def testReplaceCrdate_01 (self):
        Tester.dialogTester.appendOk ()
        text = u"ЫЫЫ Абырвалг"
        self._wikipage.content = text

        Application.selectedPage = self._wikipage
        Application.mainWindow.pagePanel.pageView.codeEditor.SetSelection (0, 3)

        Application.actionController.getAction (WikiDateCreationAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"(:crdate:) Абырвалг")


    def testReplaceEddate_01 (self):
        Tester.dialogTester.appendOk ()
        text = u"ЫЫЫ Абырвалг"
        self._wikipage.content = text

        Application.selectedPage = self._wikipage
        Application.mainWindow.pagePanel.pageView.codeEditor.SetSelection (0, 3)

        Application.actionController.getAction (WikiDateEditionAction.stringId).run (None)

        self._savePage()

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self._wikipage.content, u"(:eddate:) Абырвалг")
