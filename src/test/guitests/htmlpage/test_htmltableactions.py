# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.actions.polyactionsid import (TABLE_STR_ID,
                                            TABLE_ROW_STR_ID,
                                            TABLE_CELL_STR_ID)


class HtmlTableActionsTest (BaseMainWndTest):
    def setUp (self):
        super (HtmlTableActionsTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create (self.wikiroot, "Страница 1", [])

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self._testpage

        Tester.dialogTester.appendOk()


    def tearDown (self):
        super (HtmlTableActionsTest, self).tearDown()
        Tester.dialogTester.clear()


    def testInsertTable_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = '''<table border="1">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = '''<tr>
<td></td>
</tr>'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertCell_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_CELL_STR_ID).run (None)

        validResult = '''<td></td>'''

        self.assertEqual (editor.GetText(), validResult)


    def _getPageView (self):
        return Application.mainWindow.pagePanel.pageView


    def _getCodeEditor (self):
        return self._getPageView().codeEditor
