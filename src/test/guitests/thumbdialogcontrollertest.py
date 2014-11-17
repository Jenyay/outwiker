# -*- coding: UTF-8 -*-

import os
import unittest

from outwiker.pages.wiki.thumbdialogcontroller import ThumbDialogController
from outwiker.pages.wiki.thumbdialog import ThumbDialog
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from ..utils import removeDir


class FakeThumbDialog (object):
    """
    Фальшивый диалог для вставки превьюшки
    """
    def __init__ (self, parent, filesList, selectedFile, thumbSize, fileName, scaleType):
        self.parent = parent
        self.filesList = filesList
        self.selectedFile = selectedFile

        self.size = thumbSize
        self.fileName = fileName
        self.scaleType = scaleType


    def ShowModal (self):
        return None


    def Destroy (self):
        pass


class TestThumbDialogController (ThumbDialogController):
    def __init__ (self,
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
        super (TestThumbDialogController, self).__init__ (parent, page, selectedText)
        self._thumbSize = thumbSize
        self._fileName = fileName
        self._scaleType = scaleType

        self.dlg = None


    def _createDialog (self, parent, filesList, selectedFile):
        self.dlg = FakeThumbDialog (parent,
                                    filesList,
                                    selectedFile,
                                    self._thumbSize,
                                    self._fileName,
                                    self._scaleType)

        return self.dlg


class ThumbDialogControllerTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testwiki"
        removeDir (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]

        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"first.jpg", u"image.jpeg", u"файл с пробелами.tmp"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]



    def tearDown (self):
        removeDir (self.path)


    def testEmpty (self):
        controller = TestThumbDialogController (None, self.testPage, u"", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.result, u"%thumb%%%")
        self.assertEqual (controller.dlg.filesList, [])


    def testAttachList (self):
        Attachment (self.testPage).attach (self.fullFilesPath)
        controller = TestThumbDialogController (None, self.testPage, u"", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertTrue (u"accept.png" in controller.dlg.filesList)
        self.assertTrue (u"add.png" in controller.dlg.filesList)
        self.assertTrue (u"first.jpg" in controller.dlg.filesList)
        self.assertTrue (u"image.jpeg" in controller.dlg.filesList)
        self.assertFalse (u"файл с пробелами.tmp" in controller.dlg.filesList)


    def testSelectedAttach1 (self):
        Attachment (self.testPage).attach (self.fullFilesPath)
        controller = TestThumbDialogController (None, self.testPage, u"Attach:accept.png", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.dlg.selectedFile, u"accept.png")


    def testSelectedAttach2 (self):
        Attachment (self.testPage).attach (self.fullFilesPath)
        controller = TestThumbDialogController (None, self.testPage, u"бла-бла-бла", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.dlg.selectedFile, u"")


    def testSelectedAttach3 (self):
        Attachment (self.testPage).attach (self.fullFilesPath)
        controller = TestThumbDialogController (None, self.testPage, u"Attach:accept-2.png", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.dlg.selectedFile, u"")


    def testSelectedAttach4 (self):
        Attachment (self.testPage).attach (self.fullFilesPath)
        controller = TestThumbDialogController (None, self.testPage, u"  Attach:accept.png   ", 0, u"", ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.dlg.selectedFile, u"accept.png")


    def testResult1 (self):
        controller = TestThumbDialogController (None,
                                                self.testPage,
                                                u"",
                                                0,
                                                u"accept.png",
                                                ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.result, u"%thumb%Attach:accept.png%%")


    def testResultWidth (self):
        controller = TestThumbDialogController (None,
                                                self.testPage,
                                                u"",
                                                100,
                                                u"accept.png",
                                                ThumbDialog.WIDTH)
        controller.showDialog()

        self.assertEqual (controller.result, u"%thumb width=100%Attach:accept.png%%")


    def testResultHeight (self):
        controller = TestThumbDialogController (None,
                                                self.testPage,
                                                u"",
                                                100,
                                                u"accept.png",
                                                ThumbDialog.HEIGHT)
        controller.showDialog()

        self.assertEqual (controller.result, u"%thumb height=100%Attach:accept.png%%")


    def testResultMaxSize (self):
        controller = TestThumbDialogController (None,
                                                self.testPage,
                                                u"",
                                                100,
                                                u"accept.png",
                                                ThumbDialog.MAX_SIZE)
        controller.showDialog()

        self.assertEqual (controller.result, u"%thumb maxsize=100%Attach:accept.png%%")
