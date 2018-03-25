# -*- coding: utf-8 -*-

from datetime import datetime

import wx

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.actions.polyactionsid import CURRENT_DATE
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerGUITest


class InsertDateTest(BaseOutWikerGUITest):
    """
    Tests for a inserting of the current date
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        HtmlPageFactory().create(self.wikiroot, "HTML", [])

        self._wikipage = self.wikiroot["Викистраница"]
        self._wikipage.content = ""

        self._htmlpage = self.wikiroot["Викистраница"]
        self._htmlpage.content = ""

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self._wikipage

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _setFormat_01(self, dialog):
        dialog.Value = "%d; %m; %Y"
        return wx.ID_OK

    def _setFormat_02_cancel(self, dialog):
        dialog.Value = "%d; %m; %Y"
        return wx.ID_CANCEL

    def _setFormat_03_empty(self, dialog):
        dialog.Value = ""
        return wx.ID_OK

    def testInsertDate_01_wiki(self):
        Tester.dialogTester.append(self._setFormat_01)

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime("%d; %m; %Y")

        self.assertEqual(self._wikipage.content, rightResult)
        self.assertEqual(Tester.dialogTester.count, 0)

    def testInsertDate_01_html(self):
        Tester.dialogTester.append(self._setFormat_01)

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._htmlpage

        rightResult = datetime.now().strftime("%d; %m; %Y")

        self.assertEqual(self._htmlpage.content, rightResult)
        self.assertEqual(Tester.dialogTester.count, 0)

    def testInsertDate_02_cancel(self):
        Tester.dialogTester.append(self._setFormat_02_cancel)

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

        self.assertEqual(self._wikipage.content, "")
        self.assertEqual(Tester.dialogTester.count, 0)

    def testInsertDate_03_empty(self):
        Tester.dialogTester.append(self._setFormat_03_empty)

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

        self.assertEqual(self._wikipage.content, "")
        self.assertEqual(Tester.dialogTester.count, 0)

    def testConfig_01(self):
        config = GeneralGuiConfig(self.application.config)
        config.recentDateTimeFormat.value = "%d - %m - %Y"
        Tester.dialogTester.appendOk()

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime("%d - %m - %Y")

        self.assertEqual(self._wikipage.content, rightResult)
        self.assertEqual(Tester.dialogTester.count, 0)

    def testConfig_02_ignore(self):
        config = GeneralGuiConfig(self.application.config)
        config.recentDateTimeFormat.value = "%d - %m - %Y"
        Tester.dialogTester.append(self._setFormat_01)

        self.application.actionController.getAction(CURRENT_DATE).run(None)

        # For saving current page
        self.application.selectedPage = None
        self.application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime("%d; %m; %Y")

        self.assertEqual(self._wikipage.content, rightResult)
        self.assertEqual(Tester.dialogTester.count, 0)
