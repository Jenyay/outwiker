# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction
from test.basetestcases import BaseOutWikerGUIMixin


class MovePageUpDownActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for MovePageUpAction and MovePageDownAction
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testNoneWiki(self):
        Tester.dialogTester.appendOk()
        Tester.dialogTester.appendOk()
        self.application.wikiroot = None

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)

        self.assertEqual(Tester.dialogTester.count, 0)

    def testEmpty(self):
        self.application.wikiroot = self.wikiroot

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)

    def testMove_01(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)

    def testMove_02(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order > self.wikiroot["Страница 2"].order)

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order < self.wikiroot["Страница 2"].order)

    def testMove_03(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order > self.wikiroot["Страница 2"].order)

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order < self.wikiroot["Страница 2"].order)

    def testMove_04(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order > self.wikiroot["Страница 2"].order)

        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order < self.wikiroot["Страница 2"].order)

        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertTrue(self.wikiroot["Страница 1"].order > self.wikiroot["Страница 2"].order)

    def testMoveReadonly_01(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.wikiroot["Страница 1"].readonly = True

        Tester.dialogTester.appendOk()
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertEqual(Tester.dialogTester.count, 0)

        Tester.dialogTester.appendOk()
        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.assertEqual(Tester.dialogTester.count, 0)
