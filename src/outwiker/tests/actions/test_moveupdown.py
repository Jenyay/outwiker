# -*- coding: utf-8 -*-

import unittest

from outwiker.app.actions.movepageup import MovePageUpAction
from outwiker.app.actions.movepagedown import MovePageDownAction
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class MovePageUpDownActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for MovePageUpAction and MovePageDownAction
    """

    def setUp(self):
        self.initApplication(createTreePanel=True)
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testNoneWiki(self):
        self.application.wikiroot = None

        self.application.actionController.getAction(
            MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(
            MovePageDownAction.stringId).run(None)

        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount, 2)

    def testEmpty(self):
        self.application.wikiroot = self.wikiroot

        self.application.actionController.getAction(
            MovePageUpAction.stringId).run(None)
        self.application.actionController.getAction(
            MovePageDownAction.stringId).run(None)

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

        self.application.mainWindow.toaster.counter.clear()
        self.application.actionController.getAction(MovePageDownAction.stringId).run(None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

        self.application.mainWindow.toaster.counter.clear()
        self.application.actionController.getAction(MovePageUpAction.stringId).run(None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)
