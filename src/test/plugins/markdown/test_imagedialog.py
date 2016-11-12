# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.core.pluginsloader import PluginsLoader


class MarkdownImageDialogTest(BaseMainWndTest):
    def setUp(self):
        super(MarkdownImageDialogTest, self).setUp()
        self._application = Application

        dirlist = [u"../plugins/markdown"]
        self.loader = PluginsLoader(self._application)
        self.loader.load(dirlist)

        from markdown.images.imagedialog import ImageDialog

        self._dlg = ImageDialog(self._application.mainWindow)
        Tester.dialogTester.appendOk()

    def tearDown(self):
        super(MarkdownImageDialogTest, self).tearDown()

    def test_empty(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u''
        attachList = []
        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = u'![]()'
        self.assertEqual(controller.result, right_result)

    def test_comment_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u'Комментарий'
        attachList = []

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = u'![Комментарий]()'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, u'Комментарий')
        self.assertEqual(self._dlg.fileName, u'')
        self.assertEqual(self._dlg.filesList, [])

    def test_comment_02(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u'__attach/image.png'
        attachList = []

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = u'![__attach/image.png]()'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, u'__attach/image.png')
        self.assertEqual(self._dlg.fileName, u'')
        self.assertEqual(self._dlg.filesList, [])

    def test_attach_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u'__attach/image.png'
        attachList = [u'image.png']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = u'![](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, u'')
        self.assertEqual(self._dlg.fileName, u'__attach/image.png')
        self.assertEqual(self._dlg.filesList, [u'__attach/image.png'])

    def test_attach_02(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u'__attach/image.png'
        attachList = [u'qqq.jpg', u'image.png', u'image.gif']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = u'![](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, u'')
        self.assertEqual(self._dlg.fileName, u'__attach/image.png')
        self.assertEqual(self._dlg.filesList, [u'__attach/image.gif',
                                               u'__attach/image.png',
                                               u'__attach/qqq.jpg'])

    def test_full_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = u'__attach/image.png'
        attachList = [u'qqq.jpg', u'image.png', u'image.gif']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        self._dlg.comment = u'Комментарий'
        controller.showDialog()

        right_result = u'![Комментарий](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, u'Комментарий')
        self.assertEqual(self._dlg.fileName, u'__attach/image.png')
        self.assertEqual(self._dlg.filesList, [u'__attach/image.gif',
                                               u'__attach/image.png',
                                               u'__attach/qqq.jpg'])
