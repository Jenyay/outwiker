# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.wiki.tabledialogcontroller import TableRowsDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig


class WikiTableRowsDialogTest (BaseMainWndTest):
    def setUp (self):
        super (WikiTableRowsDialogTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = WikiPageFactory()
        self._testpage = factory.create (self.wikiroot, "Страница 1", [])


    def tearDown (self):
        super (WikiTableRowsDialogTest, self).tearDown()


    def testDefault (self):
        suffix = ''
        dlg = TableRowsDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row:)
(:cell:)'''

        self.assertEqual (result, validResult, result)


    def testDefault_suffix (self):
        suffix = '20'
        dlg = TableRowsDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = '''(:row20:)
(:cell20:)'''

        self.assertEqual (result, validResult, result)


    def testCells (self):
        suffix = ''
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, suffix, self._application.config)

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

        self.assertEqual (result, validResult, result)


    def testRowsCells (self):
        suffix = ''
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, suffix, self._application.config)

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

        self.assertEqual (result, validResult, result)


    def testColsCount (self):
        suffix = ''
        dlg = TableRowsDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableRowsDialogController (dlg, suffix, self._application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableRowsDialog (self.wnd)
        controller2 = TableRowsDialogController (dlg2, suffix, self._application.config)

        self.assertEqual (dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()


    def testHCells (self):
        suffix = ''
        dlg = TableRowsDialog (self.wnd)
        controller = TableRowsDialogController (dlg, suffix, self._application.config)

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

        self.assertEqual (result, validResult, result)
