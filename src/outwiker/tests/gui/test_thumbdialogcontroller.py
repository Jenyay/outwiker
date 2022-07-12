# -*- coding: utf-8 -*-

import os
import unittest
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
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

        filesPath = "testdata/samplefiles/"
        self.files = ["accept.png", "add.png", "first.jpg",
                      "image.jpeg", "файл с пробелами.tmp"]
        self.fullFilesPath = [os.path.join(filesPath, fname)
                              for fname
                              in self.files]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testEmpty(self):
        Tester.dialogTester.appendOk()
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb%%%")
        self.assertEqual(controller.dlg.filesList, [])

    def testAttachList(self):
        Tester.dialogTester.appendOk()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertTrue("accept.png" in controller.dlg.filesList)
        self.assertTrue("add.png" in controller.dlg.filesList)
        self.assertTrue("first.jpg" in controller.dlg.filesList)
        self.assertTrue("image.jpeg" in controller.dlg.filesList)
        self.assertFalse("файл с пробелами.tmp" in controller.dlg.filesList)

    def testSelectedAttach1(self):
        Tester.dialogTester.appendOk()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "Attach:accept.png")
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "accept.png")

    def testSelectedAttach2(self):
        Tester.dialogTester.appendOk()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "бла-бла-бла")
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "")

    def testSelectedAttach3(self):
        Tester.dialogTester.appendOk()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "Attach:accept-2.png")
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "")

    def testSelectedAttach4(self):
        Tester.dialogTester.appendOk()
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "  Attach:accept.png   ")
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "accept.png")

    def testResult1(self):
        Tester.dialogTester.appendOk()
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb%Attach:accept.png%%")

    def testResultWidth(self):
        Tester.dialogTester.appendOk()
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb width=100%Attach:accept.png%%")

    def testResultHeight(self):
        Tester.dialogTester.appendOk()
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb height=100%Attach:accept.png%%")

    def testResultMaxSize(self):
        Tester.dialogTester.appendOk()
        controller = ThumbDialogController(self.application.mainWindow, self.testPage, "")
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb maxsize=100%Attach:accept.png%%")
