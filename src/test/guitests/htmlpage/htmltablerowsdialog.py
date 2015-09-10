# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.html.tabledialogcontroller import TableRowsDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig


class HtmlTableRowsDialogTest (BaseMainWndTest):
    def setUp (self):
        super (HtmlTableRowsDialogTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create (self.wikiroot, u"Страница 1", [])


    def tearDown (self):
        super (HtmlTableRowsDialogTest, self).tearDown()


    def testDefault (self):
        dlg = TableRowsDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController (dlg, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''<tr>
<td></td>
</tr>'''

        self.assertEqual (result, validResult, result)


    def testCells (self):
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, self._application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>'''

        self.assertEqual (result, validResult, result)


    def testRowsCells (self):
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''<tr>
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

        self.assertEqual (result, validResult, result)


    def testColsCount (self):
        dlg = TableRowsDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController (dlg, self._application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableRowsDialog (self.wnd)
        controller2 = TableRowsDialogController (dlg2, self._application.config)

        self.assertEqual (dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()


    def testHCells (self):
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''<tr>
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

        self.assertEqual (result, validResult, result)
