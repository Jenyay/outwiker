# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.wiki.tabledialogcontroller import TableDialogController
from outwiker.gui.guiconfig import GeneralGuiConfig


class WikiTableDialogTest (BaseMainWndTest):
    def setUp (self):
        super (WikiTableDialogTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = WikiPageFactory()
        self._testpage = factory.create (self.wikiroot, u"Страница 1", [])


    def tearDown (self):
        super (WikiTableDialogTest, self).tearDown()


    def testDefault (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testDefault_suffix (self):
        suffix = u'20'
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table20 border="1":)
(:row20:)
(:cell20:)
(:table20end:)'''

        self.assertEqual (result, validResult, result)


    def testCells (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testRowsCells (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
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

        self.assertEqual (result, validResult, result)


    def testBorder_01 (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 10
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="10":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testBorder_02 (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 0
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table:)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testColsCount (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        dlg.colsCount = 10
        controller.showDialog()

        dlg2 = TableDialog (self.wnd)
        controller2 = TableDialogController (dlg2, suffix, self._application.config)

        self.assertEqual (dlg2.colsCount, 10)

        Tester.dialogTester.appendOk()
        controller2.showDialog()


    def testHCells (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        dlg.headerCells = True
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
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

        self.assertEqual (result, validResult, result)
