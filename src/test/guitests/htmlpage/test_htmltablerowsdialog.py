# -*- coding: utf-8 -*-

from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.html.tabledialogcontroller import TableRowsDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerGUITest


class HtmlTableRowsDialogTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self._application = self.application

        config = GeneralGuiConfig(self._application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefault(self):
        dlg = TableRowsDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController(dlg, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<tr>
<td></td>
</tr>'''

        self.assertEqual(result, validResult, result)

    def testCells(self):
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg, self._application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>'''

        self.assertEqual(result, validResult, result)

    def testRowsCells(self):
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<tr>
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
</tr>'''

        self.assertEqual(result, validResult, result)

    def testColsCount(self):
        dlg = TableRowsDialog(self.mainWindow)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController(dlg, self._application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableRowsDialog(self.mainWindow)
        controller2 = TableRowsDialogController(dlg2, self._application.config)

        self.assertEqual(dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()

    def testHCells(self):
        dlg = TableRowsDialog(self.mainWindow)
        controller = TableRowsDialogController(dlg, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = '''<tr>
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
</tr>'''

        self.assertEqual(result, validResult, result)
