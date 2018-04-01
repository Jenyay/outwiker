# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.tester import Tester
from outwiker.core.pluginsloader import PluginsLoader
from test.basetestcases import BaseOutWikerGUIMixin


class MarkdownImageDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        dirlist = ["../plugins/markdown"]
        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        from markdown.images.imagedialog import ImageDialog

        self._dlg = ImageDialog(self.application.mainWindow)
        Tester.dialogTester.appendOk()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_empty(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = ''
        attachList = []
        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = '![]()'
        self.assertEqual(controller.result, right_result)

    def test_comment_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = 'Комментарий'
        attachList = []

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = '![Комментарий]()'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, 'Комментарий')
        self.assertEqual(self._dlg.fileName, '')
        self.assertEqual(self._dlg.filesList, [])

    def test_comment_02(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = '__attach/image.png'
        attachList = []

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = '![__attach/image.png]()'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, '__attach/image.png')
        self.assertEqual(self._dlg.fileName, '')
        self.assertEqual(self._dlg.filesList, [])

    def test_attach_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = '__attach/image.png'
        attachList = ['image.png']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = '![](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, '')
        self.assertEqual(self._dlg.fileName, '__attach/image.png')
        self.assertEqual(self._dlg.filesList, ['__attach/image.png'])

    def test_attach_02(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = '__attach/image.png'
        attachList = ['qqq.jpg', 'image.png', 'image.gif']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        controller.showDialog()

        right_result = '![](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, '')
        self.assertEqual(self._dlg.fileName, '__attach/image.png')
        self.assertEqual(self._dlg.filesList, ['__attach/image.gif',
                                               '__attach/image.png',
                                               '__attach/qqq.jpg'])

    def test_full_01(self):
        from markdown.images.imagedialogcontroller import ImageDialogController

        selectedText = '__attach/image.png'
        attachList = ['qqq.jpg', 'image.png', 'image.gif']

        controller = ImageDialogController(self._dlg, attachList, selectedText)
        self._dlg.comment = 'Комментарий'
        controller.showDialog()

        right_result = '![Комментарий](__attach/image.png)'
        self.assertEqual(controller.result, right_result)

        self.assertEqual(self._dlg.comment, 'Комментарий')
        self.assertEqual(self._dlg.fileName, '__attach/image.png')
        self.assertEqual(self._dlg.filesList, ['__attach/image.gif',
                                               '__attach/image.png',
                                               '__attach/qqq.jpg'])
