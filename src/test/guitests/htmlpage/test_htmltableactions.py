# -*- coding: utf-8 -*-

from outwiker.gui.tester import Tester
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.actions.polyactionsid import (TABLE_STR_ID,
                                            TABLE_ROW_STR_ID,
                                            TABLE_CELL_STR_ID)
from test.basetestcases import BaseOutWikerGUITest


class HtmlTableActionsTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        config = GeneralGuiConfig(self.application.config)
        config.tableColsCount.remove_option()
        factory = HtmlPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._testpage

        Tester.dialogTester.appendOk()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        Tester.dialogTester.clear()

    def testInsertTable_01(self):
        editor = self._getCodeEditor()
        self.application.actionController.getAction(TABLE_STR_ID).run(None)

        validResult = '''<table border="1">
<tr>
<td></td>
</tr>
</table>'''

        self.assertEqual(editor.GetText(), validResult)

    def testInsertRow_01(self):
        editor = self._getCodeEditor()
        self.application.actionController.getAction(TABLE_ROW_STR_ID).run(None)

        validResult = '''<tr>
<td></td>
</tr>'''

        self.assertEqual(editor.GetText(), validResult)

    def testInsertCell_01(self):
        editor = self._getCodeEditor()
        self.application.actionController.getAction(TABLE_CELL_STR_ID).run(None)

        validResult = '''<td></td>'''

        self.assertEqual(editor.GetText(), validResult)

    def _getPageView(self):
        return self.application.mainWindow.pagePanel.pageView

    def _getCodeEditor(self):
        return self._getPageView().codeEditor
