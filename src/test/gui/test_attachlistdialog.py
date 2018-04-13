# -*- coding: utf-8 -*-

import unittest

from outwiker.pages.wiki.actions.attachlist import (AttachListDialog,
                                                    AttachListDialogController)
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class AttachListDialogTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты диалога для вставки команды (:attachlist:)
    """
    def setUp(self):
        self.initApplication()
        self._dialog = AttachListDialog(self.application.mainWindow)
        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()

    def testCancel(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendCancel()
        result = controller.getDialogResult()

        self.assertEqual(result, None)

    def testSortByName(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=name:)")

    def testSortByNameDescend(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=descendname:)")

    def testSortByExt(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 1
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=ext:)")

    def testSortByExtDescend(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 1
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=descendext:)")

    def testSortBySize(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 2
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=size:)")

    def testSortBySizeDescend(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 2
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=descendsize:)")

    def testSortByDate(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 3
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=date:)")

    def testSortByDateDescend(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 3
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=descenddate:)")
