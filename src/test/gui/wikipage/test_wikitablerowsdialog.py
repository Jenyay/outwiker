# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.wiki.tabledialogcontroller import TableRowsDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerGUIMixin


class WikiTableRowsDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        config = GeneralGuiConfig(self.application.config)
        config.tableColsCount.remove_option()
        factory = WikiPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefault(self):
        suffix = ''
        dlg = TableRowsDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row:)
(:cell:)'''

        self.assertEqual(result, validResult, result)

    def testDefault_suffix(self):
        suffix = '20'
        dlg = TableRowsDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row20:)
(:cell20:)'''

        self.assertEqual(result, validResult, result)

    def testCells(self):
        suffix = ''
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)'''

        self.assertEqual(result, validResult, result)

    def testRowsCells(self):
        suffix = ''
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)'''

        self.assertEqual(result, validResult, result)

    def testColsCount(self):
        suffix = ''
        dlg = TableRowsDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableRowsDialog(self.mainWindow)
        controller2 = TableRowsDialogController(dlg2,
                                                suffix,
                                                self.application.config)

        self.assertEqual(dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()

    def testHCells(self):
        suffix = ''
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg,
                                               suffix,
                                               self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row:)
(:hcell:)
(:hcell:)
(:hcell:)
(:hcell:)
(:hcell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)'''

        self.assertEqual(result, validResult, result)
