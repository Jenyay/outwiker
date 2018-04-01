# -*- coding: utf-8 -*-

import unittest

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.moving import (GoToParentAction,
                                     GoToFirstChildAction,
                                     GoToNextSiblingAction,
                                     GoToPrevSiblingAction)
from test.basetestcases import BaseOutWikerGUIMixin


class MovingActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for moving on pages
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_goToParent_01(self):
        self.application.wikiroot = None
        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToParent_02(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToParent_03(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]
        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToParent_04(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 1"]
        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

    def test_goToParent_05(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4"]
        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

    def test_goToParent_06(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"]

        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 4"])

        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

        self.application.actionController.getAction(GoToParentAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToFirstChild_01(self):
        self.application.wikiroot = None
        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToFirstChild_02(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.application.wikiroot["Страница 1"])

    def test_goToFirstChild_03(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.application.wikiroot["Страница 1"])

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.application.wikiroot["Страница 1/Страница 1 - 1"])

    def test_goToFirstChild_04(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToFirstChild_05(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4"]

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"])

        self.application.actionController.getAction(GoToFirstChildAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage,
                         self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"])

    def test_goToNextSibling_01(self):
        self.application.wikiroot = None
        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToNextSibling_02(self):
        self.application.wikiroot = self.wikiroot

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToNextSibling_03(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToNextSibling_04(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 3"])

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 3"])

    def test_goToNextSibling_05(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 1"]

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 2"])

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 3"])

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 4"])

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 4"])

    def test_goToNextSibling_06(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"]

        self.application.actionController.getAction(GoToNextSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"])

    def test_goToPrevSibling_01(self):
        self.application.wikiroot = None
        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToPrevSibling_02(self):
        self.application.wikiroot = self.wikiroot

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToPrevSibling_03(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, None)

    def test_goToPrevSibling_04(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 3"]

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 2"])

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1"])

    def test_goToPrevSibling_05(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4"]

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 3"])

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 2"])

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 1"])

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 1"])

    def test_goToPrevSibling_06(self):
        self._createWikiPages()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"]

        self.application.actionController.getAction(GoToPrevSiblingAction.stringId).run(None)
        self.assertEqual(self.application.selectedPage, self.wikiroot["Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"])

    def _createWikiPages(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        factory.create(self.wikiroot["Страница 1"], "Страница 1 - 1", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 1 - 2", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 1 - 3", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 1 - 4", [])

        factory.create(self.wikiroot["Страница 1/Страница 1 - 4"], "Страница 1 - 4 - 1", [])

        factory.create(self.wikiroot["Страница 2"], "Страница 2 - 1", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 2 - 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 2 - 3", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 2 - 4", [])
