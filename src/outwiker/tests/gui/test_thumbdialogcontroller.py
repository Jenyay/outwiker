# -*- coding: utf-8 -*-

import os
import unittest
from pathlib import Path
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.thumbdialogcontroller import ThumbDialogController
from outwiker.pages.wiki.thumbdialog import ThumbDialog
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin
from outwiker.tests.utils import removeDir


class ThumbDialogControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

        filesPath = "testdata/samplefiles/"
        self.files = [
            "accept.png",
            "add.png",
            "first.jpg",
            "image.jpeg",
            "файл с пробелами.tmp",
        ]
        self.fullFilesPath = [os.path.join(filesPath, fname) for fname in self.files]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def _mixin_select_file(self, dialog: ThumbDialog, fname: str):
        dialog.SetSelectedFile(fname)

    def _mixin_set_height(self, dialog: ThumbDialog, value: int):
        dialog.scaleType = ThumbDialog.HEIGHT
        dialog.scale = value

    def _mixin_set_width(self, dialog: ThumbDialog, value: int):
        dialog.scaleType = ThumbDialog.WIDTH
        dialog.scale = value

    def _mixin_set_max_size(self, dialog: ThumbDialog, value: int):
        dialog.scaleType = ThumbDialog.MAX_SIZE
        dialog.scale = value

    def testEmpty(self):
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, ""
        )
        controller.showDialog()

        self.assertEqual(controller.result, "")

    def testAttachList(self):
        Tester.dialogTester.appendCancel()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, ""
        )
        controller.showDialog()

        self.assertTrue("accept.png" in controller.filesList)
        self.assertTrue("add.png" in controller.filesList)
        self.assertTrue("first.jpg" in controller.filesList)
        self.assertTrue("image.jpeg" in controller.filesList)
        self.assertFalse("файл с пробелами.tmp" in controller.filesList)

    def testSelectedAttachNoQuotes(self):
        selected_text = "Attach:accept.png"

        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "accept.png")

    def testSelectedAttachSingleQuotes(self):
        selected_text = "Attach:'accept.png'"

        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "accept.png")

    def testSelectedAttachDoubleQuotes(self):
        selected_text = 'Attach:"accept.png"'

        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "accept.png")

    def testSelectedAttachSubdirForwardSlashesSingleQuotes(self):
        subdir = Path('subdir 1', 'subdir 2')
        relative_path = 'subdir 1/subdir 2/accept.png'
        selected_text = "Attach:'{}'".format(relative_path)

        Tester.dialogTester.appendOk()

        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(self.fullFilesPath, subdir)

        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, relative_path)

    def testSelectedAttachSubdirBackSlashesSingleQuotes(self):
        subdir = Path('subdir 1', 'subdir 2')
        relative_path = 'subdir 1\\subdir 2\\accept.png'
        selected_text = "Attach:'{}'".format(relative_path)

        Tester.dialogTester.appendOk()

        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(self.fullFilesPath, subdir)

        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, relative_path.replace('\\', '/'))

    def testSelectedAttachSubdirForwardSlashesDoubleQuotes(self):
        subdir = Path('subdir 1', 'subdir 2')
        relative_path = 'subdir 1/subdir 2/accept.png'
        selected_text = 'Attach:"{}"'.format(relative_path)

        Tester.dialogTester.appendOk()

        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(self.fullFilesPath, subdir)

        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, relative_path)

    def testSelectedAttachSubdirBackSlashesDoubleQuotes(self):
        subdir = Path('subdir 1', 'subdir 2')
        relative_path = 'subdir 1\\subdir 2\\accept.png'
        selected_text = 'Attach:"{}"'.format(relative_path)

        Tester.dialogTester.appendOk()

        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(self.fullFilesPath, subdir)

        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, relative_path.replace('\\', '/'))

    def testSelectedAttach2(self):
        selected_text = "бла-бла-бла"

        Tester.dialogTester.appendCancel()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "")

    def testSelectedAttach3(self):
        selected_text = "Attach:accept-2.png"

        Tester.dialogTester.appendCancel()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "")

    def testSelectedAttach4(self):
        selected_text = "  Attach:accept.png   "

        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.selectedFile, "accept.png")

    def testResult1(self):
        selected_text = ""

        Tester.dialogTester.append(self._mixin_select_file, "accept.png")
        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb%Attach:accept.png%%")

    def testResultWidth(self):
        selected_text = ""

        Tester.dialogTester.append(self._mixin_select_file, "accept.png")
        Tester.dialogTester.append(self._mixin_set_width, 100)
        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb width=100%Attach:accept.png%%")

    def testResultHeight(self):
        selected_text = ""

        Tester.dialogTester.append(self._mixin_select_file, "accept.png")
        Tester.dialogTester.append(self._mixin_set_height, 100)
        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb height=100%Attach:accept.png%%")

    def testResultMaxSize(self):
        selected_text = ""

        Tester.dialogTester.append(self._mixin_select_file, "accept.png")
        Tester.dialogTester.append(self._mixin_set_max_size, 100)
        Tester.dialogTester.appendOk()

        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(
            self.application, self.application.mainWindow, self.testPage, selected_text
        )
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb maxsize=100%Attach:accept.png%%")
