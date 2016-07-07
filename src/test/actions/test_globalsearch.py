# -*- coding: UTF-8 -*-

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.globalsearch import GlobalSearchAction


class GlobalSearchActionTest (BaseMainWndTest):
    """
    Tests for GlobalSearchAction
    """
    def testNoneWiki (self):
        Application.wikiroot = None
        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)


    def testEmptyWiki (self):
        Application.wikiroot = self.wikiroot

        self.assertEqual (len (Application.wikiroot.children), 0)
        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)

        self.assertEqual (len (Application.wikiroot.children), 1)
        self.assertEqual (Application.selectedPage, Application.wikiroot.children[0])


    def testReadOnly (self):
        Application.wikiroot = self.wikiroot
        Application.wikiroot.readonly = True

        Tester.dialogTester.appendOk()

        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)

        self.assertEqual (len (Application.wikiroot.children), 0)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testExecSeveralTimes (self):
        Application.wikiroot = self.wikiroot
        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)
        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)
        Application.actionController.getAction (GlobalSearchAction.stringId).run (None)

        self.assertEqual (len (Application.wikiroot.children), 1)
