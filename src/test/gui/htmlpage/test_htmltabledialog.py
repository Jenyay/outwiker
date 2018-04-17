# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.html.tabledialogcontroller import TableDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerGUIMixin


class HtmlTableDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        config = GeneralGuiConfig(self.application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefault(self):
        dlg = TableDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableDialogController(dlg, self.application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="1">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)

    def testCells(self):
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg, self.application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="1">
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)

    def testRowsCells(self):
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg, self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="1">
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)

    def testBorder_01(self):
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg, self.application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 10
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="10">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)

    def testBorder_02(self):
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg, self.application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 0
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table>
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)

    def testColsCount(self):
        dlg = TableDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableDialogController(dlg, self.application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableDialog(self.mainWindow)
        controller2 = TableDialogController(dlg2, self.application.config)

        self.assertEqual(dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()

    def testHCells(self):
        dlg = TableDialog(self.mainWindow)
        controller = TableDialogController(dlg, self.application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="1">
<tr>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>'''

        self.assertEqual(result, validResult, result)
