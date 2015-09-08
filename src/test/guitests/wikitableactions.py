# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.actions.polyactionsid import (TABLE_STR_ID,
                                            TABLE_ROW_STR_ID,
                                            TABLE_CELL_STR_ID)


class WikiTableActionsTest (BaseMainWndTest):
    def setUp (self):
        super (WikiTableActionsTest, self).setUp()
        self._application = Application

        config = GeneralGuiConfig (self._application.config)
        config.tableColsCount.remove_option()
        factory = WikiPageFactory()
        self._testpage = factory.create (self.wikiroot, u"Страница 1", [])

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self._testpage

        Tester.dialogTester.appendOk()


    def tearDown (self):
        super (WikiTableActionsTest, self).tearDown()
        Tester.dialogTester.clear()


    def testInsertTable_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_02 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table:)\n'
        initTextPart2 = u'\n(:tableend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table:)
(:table2 border="1":)
(:row2:)
(:cell2:)
(:table2end:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_03 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:table:)
(:table10:)
'''

        initTextPart2 = u'''
(:table10end:)
(:tableend:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table:)
(:table10:)
(:table11 border="1":)
(:row11:)
(:cell11:)
(:table11end:)
(:table10end:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_04 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:table20:)\n'''
        initTextPart2 = u'''\n(:table20end:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table20:)
(:table21 border="1":)
(:row21:)
(:cell21:)
(:table21end:)
(:table20end:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_05 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:tableqqq:)\n'''
        initTextPart2 = u'''\n(:tableqqqend:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:tableqqq:)
(:table border="1":)
(:row:)
(:cell:)
(:tableend:)
(:tableqqqend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_06 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:table:)
(:row:)
(:cell:)'''

        initTextPart2 = u'''\n(:tableend:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table:)
(:row:)
(:cell:)(:table2 border="1":)
(:row2:)
(:cell2:)
(:table2end:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_07 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:table:)(:tableend:)\n'''
        initTextPart2 = u'''\n(:table:)(:tableend:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table:)(:tableend:)
(:table border="1":)
(:row:)
(:cell:)
(:tableend:)
(:table:)(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertTable_08 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'''(:table2:)(:table2end:)\n'''
        initTextPart2 = u'''\n(:table3:)(:table3end:)'''

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_STR_ID).run (None)

        validResult = u'''(:table2:)(:table2end:)
(:table border="1":)
(:row:)
(:cell:)
(:tableend:)
(:table3:)(:table3end:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = u'''(:row:)
(:cell:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_02 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table:)\n'
        initTextPart2 = u'\n(:tableend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = u'''(:table:)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_03 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table2:)\n'
        initTextPart2 = u'\n(:table2end:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = u'''(:table2:)
(:row2:)
(:cell2:)
(:table2end:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_04 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:tableqqq:)\n'
        initTextPart2 = u'\n(:tableqqqend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = u'''(:tableqqq:)
(:row:)
(:cell:)
(:tableqqqend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertRow_05 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table:)(:table2:)\n'
        initTextPart2 = u'\n(:table2end:)(:tableend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_ROW_STR_ID).run (None)

        validResult = u'''(:table:)(:table2:)
(:row2:)
(:cell2:)
(:table2end:)(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertCell_01 (self):
        editor = self._getCodeEditor()
        self._application.actionController.getAction (TABLE_CELL_STR_ID).run (None)

        validResult = u'''(:cell:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertCell_02 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table:)\n'
        initTextPart2 = u'\n(:tableend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_CELL_STR_ID).run (None)

        validResult = u'''(:table:)
(:cell:)
(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def testInsertCell_03 (self):
        editor = self._getCodeEditor()

        initTextPart1 = u'(:table:)(:table2:)\n'
        initTextPart2 = u'\n(:table2end:)(:tableend:)'

        editor.SetText (initTextPart1 + initTextPart2)
        editor.SetSelection (len (initTextPart1), len (initTextPart1))

        self._application.actionController.getAction (TABLE_CELL_STR_ID).run (None)

        validResult = u'''(:table:)(:table2:)
(:cell2:)
(:table2end:)(:tableend:)'''

        self.assertEqual (editor.GetText(), validResult)


    def _getPageView (self):
        return Application.mainWindow.pagePanel.pageView


    def _getCodeEditor (self):
        return self._getPageView().codeEditor
