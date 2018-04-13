# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.pages.wiki.thumbdialogcontroller import ThumbDialogController
from outwiker.pages.wiki.thumbdialog import ThumbDialog
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from ..utils import removeDir


class FakeThumbDialog(object):
    """
    Фальшивый диалог для вставки превьюшки
    """
    def __init__(self, parent, filesList, selectedFile,
                 thumbSize, fileName, scaleType):
        self.parent = parent
        self.filesList = filesList
        self.selectedFile = selectedFile

        self.size = thumbSize
        self.fileName = fileName
        self.scaleType = scaleType

    def ShowModal(self):
        return None

    def Destroy(self):
        pass


class ExampleThumbDialogController(ThumbDialogController):
    def __init__(self,
                 parent,
                 page,
                 selectedText,
                 thumbSize,
                 fileName,
                 scaleType):
        """
        thumbSize - размер, якобы выбранный в диалоге
        fileName - имя файла, якобы выбанное в диалоге
        scaleType - способ масштабирования, якобы выбанный в диалоге
        """
        super(ExampleThumbDialogController, self).__init__(parent,
                                                           page,
                                                           selectedText)
        self._thumbSize = thumbSize
        self._fileName = fileName
        self._scaleType = scaleType

        self.dlg = None

    def _createDialog(self, parent, filesList, selectedFile):
        self.dlg = FakeThumbDialog(parent,
                                   filesList,
                                   selectedFile,
                                   self._thumbSize,
                                   self._fileName,
                                   self._scaleType)

        return self.dlg


class ThumbDialogControllerTest(unittest.TestCase):
    def setUp(self):
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "first.jpg",
                      "image.jpeg", "файл с пробелами.tmp"]
        self.fullFilesPath = [os.path.join(filesPath, fname)
                              for fname
                              in self.files]

    def tearDown(self):
        removeDir(self.path)

    def testEmpty(self):
        controller = ExampleThumbDialogController(None, self.testPage, "",
                                                  0, "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb%%%")
        self.assertEqual(controller.dlg.filesList, [])

    def testAttachList(self):
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ExampleThumbDialogController(None, self.testPage, "",
                                                  0, "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertTrue("accept.png" in controller.dlg.filesList)
        self.assertTrue("add.png" in controller.dlg.filesList)
        self.assertTrue("first.jpg" in controller.dlg.filesList)
        self.assertTrue("image.jpeg" in controller.dlg.filesList)
        self.assertFalse("файл с пробелами.tmp" in controller.dlg.filesList)

    def testSelectedAttach1(self):
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ExampleThumbDialogController(None, self.testPage,
                                                  "Attach:accept.png", 0,
                                                  "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "accept.png")

    def testSelectedAttach2(self):
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ExampleThumbDialogController(None, self.testPage,
                                                  "бла-бла-бла", 0,
                                                  "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "")

    def testSelectedAttach3(self):
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ExampleThumbDialogController(None, self.testPage,
                                                  "Attach:accept-2.png", 0,
                                                  "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "")

    def testSelectedAttach4(self):
        Attachment(self.testPage).attach(self.fullFilesPath)
        controller = ExampleThumbDialogController(None, self.testPage,
                                                  "  Attach:accept.png   ",
                                                  0, "", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.dlg.selectedFile, "accept.png")

    def testResult1(self):
        controller = ExampleThumbDialogController(None,
                                                  self.testPage,
                                                  "",
                                                  0,
                                                  "accept.png",
                                                  ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.result, "%thumb%Attach:accept.png%%")

    def testResultWidth(self):
        controller = ExampleThumbDialogController(None,
                                                  self.testPage,
                                                  "",
                                                  100,
                                                  "accept.png",
                                                  ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb width=100%Attach:accept.png%%")

    def testResultHeight(self):
        controller = ExampleThumbDialogController(None,
                                                  self.testPage,
                                                  "",
                                                  100,
                                                  "accept.png",
                                                  ThumbDialog.HEIGHT)
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb height=100%Attach:accept.png%%")

    def testResultMaxSize(self):
        controller = ExampleThumbDialogController(None,
                                                  self.testPage,
                                                  "",
                                                  100,
                                                  "accept.png",
                                                  ThumbDialog.MAX_SIZE)
        controller.showDialog()

        self.assertEqual(controller.result,
                         "%thumb maxsize=100%Attach:accept.png%%")
