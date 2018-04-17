# -*- coding: UTF-8 -*-

import unittest

from outwiker.pages.wiki.actions.childlist import (ChildListDialog,
                                                   ChildListDialogController)
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class ChildListDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты диалога для вставки команды (:childlist:)
    """
    def setUp(self):
        self.initApplication()
        self._dialog = ChildListDialog(self.application.mainWindow)

    def tearDown(self):
        self.destroyApplication()

    def testCancel(self):
        controller = ChildListDialogController(self._dialog)
        Tester.dialogTester.appendCancel()
        result = controller.getDialogResult()

        self.assertEqual(result, None)

    def testSortByOrder(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist:)")

    def testSortByOrderDescend(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=descendorder:)")

    def testSortByName(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 1
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=name:)")

    def testSortByNameDescend(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 1
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=descendname:)")

    def testSortByCreation(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 2
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=creation:)")

    def testSortByCreationDescend(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 2
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=descendcreation:)")

    def testSortByEdit(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 3
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=edit:)")

    def testSortByEditDescend(self):
        controller = ChildListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 3
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:childlist sort=descendedit:)")
