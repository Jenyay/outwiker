# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.html.tabledialogcontroller import TableDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig


class HtmlTableDialogTest (BaseMainWndTest):
    def setUp (self):
        super (HtmlTableDialogTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create (self.wikiroot, "Страница 1", [])


    def tearDown (self):
        super (HtmlTableDialogTest, self).tearDown()


    def testDefault (self):
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="1">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual (result, validResult, result)


    def testCells (self):
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, self._application.config)

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

        self.assertEqual (result, validResult, result)


    def testRowsCells (self):
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, self._application.config)

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

        self.assertEqual (result, validResult, result)


    def testBorder_01 (self):
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, self._application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 10
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table border="10">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual (result, validResult, result)


    def testBorder_02 (self):
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, self._application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 0
        controller.showDialog()

        result = controller.getResult()

        validResult = '''<table>
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual (result, validResult, result)


    def testColsCount (self):
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, self._application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableDialog (self.wnd)
        controller2 = TableDialogController (dlg2, self._application.config)

        self.assertEqual (dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()


    def testHCells (self):
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, self._application.config)

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

        self.assertEqual (result, validResult, result)
