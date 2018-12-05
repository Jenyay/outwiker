# -*- coding: utf-8 -*-

import unittest

from outwiker.actions.globalsearch import GlobalSearchAction
from test.basetestcases import BaseOutWikerGUIMixin


class GlobalSearchActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for GlobalSearchAction
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testNoneWiki(self):
        self.application.wikiroot = None
        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)

    def testEmptyWiki(self):
        self.application.wikiroot = self.wikiroot

        self.assertEqual(len(self.application.wikiroot.children), 0)
        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)

        self.assertEqual(len(self.application.wikiroot.children), 1)
        self.assertEqual(self.application.selectedPage, self.application.wikiroot.children[0])

    def testReadOnly(self):
        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.readonly = True

        self.application.mainWindow.toaster.counter.clear()

        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)

        self.assertEqual(len(self.application.wikiroot.children), 0)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testExecSeveralTimes(self):
        self.application.wikiroot = self.wikiroot
        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)
        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)
        self.application.actionController.getAction(GlobalSearchAction.stringId).run(None)

        self.assertEqual(len(self.application.wikiroot.children), 1)
