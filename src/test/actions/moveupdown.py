# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction


class MovePageUpDownActionTest (BaseMainWndTest):
    """
    Tests for MovePageUpAction and MovePageDownAction
    """
    def testNoneWiki (self):
        Tester.dialogTester.appendOk()
        Tester.dialogTester.appendOk()
        Application.wikiroot = None

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)


    def testEmpty (self):
        Application.wikiroot = self.wikiroot

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)


    def testMove_01 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)


    def testMove_02 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order > self.wikiroot[u"Страница 2"].order)

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order < self.wikiroot[u"Страница 2"].order)


    def testMove_03 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order > self.wikiroot[u"Страница 2"].order)

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order < self.wikiroot[u"Страница 2"].order)


    def testMove_04 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order > self.wikiroot[u"Страница 2"].order)

        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order < self.wikiroot[u"Страница 2"].order)

        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        self.assertTrue (self.wikiroot[u"Страница 1"].order > self.wikiroot[u"Страница 2"].order)


    def testMoveReadonly_01 (self):
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]
        self.wikiroot[u"Страница 1"].readonly = True

        Tester.dialogTester.appendOk()
        Application.actionController.getAction (MovePageDownAction.stringId).run(None)
        self.assertEqual (Tester.dialogTester.count, 0)

        Tester.dialogTester.appendOk()
        Application.actionController.getAction (MovePageUpAction.stringId).run(None)
        self.assertEqual (Tester.dialogTester.count, 0)
