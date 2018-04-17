# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.wiki.tabledialogcontroller import TableDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerGUIMixin


class WikiTableDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
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
        dlg = TableDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table border="1":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)

    def testDefault_suffix(self):
        suffix = '20'
        dlg = TableDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table20 border="1":)
(:row20:)
(:cell20:)
(:table20end:)'''

        self.assertEqual(result, validResult, result)

    def testCells(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table border="1":)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)

    def testRowsCells(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table border="1":)
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
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)

    def testBorder_01(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 10
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table border="10":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)

    def testBorder_02(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 0
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table:)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)

    def testColsCount(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableDialog(self.mainWindow)
        controller2 = TableDialogController(dlg2,
                                            suffix,
                                            self.application.config)

        self.assertEqual(dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()

    def testHCells(self):
        suffix = ''
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg,
                                           suffix,
                                           self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:table border="1":)
(:row:)
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
(:cell:)
(:tableend:)'''

        self.assertEqual(result, validResult, result)
