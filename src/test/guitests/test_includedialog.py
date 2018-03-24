# -*- coding: utf-8 -*-

import os.path

from outwiker.pages.wiki.actions.include import (IncludeDialog,
                                                 IncludeDialogController)
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.attachment import Attachment
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUITest


class IncludeDialogTest(BaseOutWikerGUITest):
    """
    Тесты диалога для вставки команды (:include:)
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self._dialog = IncludeDialog(self.application.mainWindow)

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        self.testedPage = self.wikiroot["Викистраница"]

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "anchor.png", "файл с пробелами.tmp", "dir"]
        self.fullFilesPath = [os.path.join(filesPath, fname) for fname in self.files]

        Attachment(self.testedPage).attach(self.fullFilesPath)
        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testCancel(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)
        Tester.dialogTester.appendCancel()
        result = controller.getDialogResult()

        self.assertEqual(result, None)
        self.assertEqual(len(self._dialog.attachmentList), 5)

    def test_01(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:include Attach:accept.png:)")

    def test_02(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 1
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:include Attach:add.png:)")

    def test_03(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 3
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:include Attach:dir:)")

    def test_04(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 4
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:include Attach:файл с пробелами.tmp:)")

    def test_05(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 400
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, "(:include Attach:accept.png:)")

    def test_encoding_01(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png encoding="utf-16":)')

    def test_encoding_02(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 6
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png encoding="mac_cyrillic":)')

    def test_encoding_04(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 600
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png:)')

    def test_escapeHtml_01(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png htmlescape:)')

    def test_escapeHtml_02(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png encoding="utf-16" htmlescape:)')

    def test_wikiparse_01(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png wikiparse:)')

    def test_wikiparse_02(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png encoding="utf-16" wikiparse:)')

    def test_wikiparse_escapehtml(self):
        controller = IncludeDialogController(self._dialog, self.testedPage)

        Tester.dialogTester.appendOk()
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual(result, '(:include Attach:accept.png encoding="utf-16" htmlescape wikiparse:)')
