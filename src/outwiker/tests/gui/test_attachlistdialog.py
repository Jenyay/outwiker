# -*- coding: utf-8 -*-

import unittest
from pathlib import Path

from outwiker.pages.wiki.actions.attachlist import (AttachListDialog,
                                                    AttachListDialogController)
from outwiker.gui.tester import Tester
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class AttachListDialogTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты диалога для вставки команды (:attachlist:)
    """

    def setUp(self):
        self.initApplication()
        self.files_path = Path('testdata/samplefiles/')

        self.wikiroot = self.createWiki()
        factory = TextPageFactory()
        self.page = factory.create(self.wikiroot, 'Страница 1', [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.page

        self._dialog = AttachListDialog(self.application.mainWindow, self.page)
        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

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

    def testSortByNameSubdirDot(self):
        controller = AttachListDialogController(self._dialog)

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False
        self._dialog.subdir = '.'

        result = controller.getDialogResult()

        self.assertEqual(result, "(:attachlist sort=name:)")

    def testSortByNameSubdir_01(self):
        controller = AttachListDialogController(self._dialog)
        subdir = 'subdir_1'

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False
        self._dialog.subdir = subdir

        result = controller.getDialogResult()

        self.assertEqual(result, '(:attachlist sort=name subdir="subdir_1":)')

    def testSortByNameSubdir_02(self):
        controller = AttachListDialogController(self._dialog)
        subdir = 'subdir_1/subdir_2'

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False
        self._dialog.subdir = subdir

        result = controller.getDialogResult()

        self.assertEqual(result, '(:attachlist sort=name subdir="subdir_1/subdir_2":)')

    def testSortByNameSubdir_03(self):
        controller = AttachListDialogController(self._dialog)
        subdir = 'subdir_1\\subdir_2'

        Tester.dialogTester.appendOk()
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False
        self._dialog.subdir = subdir

        result = controller.getDialogResult()

        self.assertEqual(result, '(:attachlist sort=name subdir="subdir_1\\subdir_2":)')
