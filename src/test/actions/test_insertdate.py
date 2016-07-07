# -*- coding: UTF-8 -*-

from datetime import datetime

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.actions.polyactionsid import CURRENT_DATE
from outwiker.gui.guiconfig import GeneralGuiConfig


class InsertDateTest (BaseMainWndTest):
    """
    Tests for a inserting of the current date
    """
    def setUp (self):
        super (InsertDateTest, self).setUp()

        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        HtmlPageFactory().create (self.wikiroot, u"HTML", [])

        self._wikipage = self.wikiroot[u"Викистраница"]
        self._wikipage.content = u""

        self._htmlpage = self.wikiroot[u"Викистраница"]
        self._htmlpage.content = u""

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self._wikipage


    def _setFormat_01 (self, dialog):
        dialog.Value = u"%d; %m; %Y"
        return wx.ID_OK


    def _setFormat_02_cancel (self, dialog):
        dialog.Value = u"%d; %m; %Y"
        return wx.ID_CANCEL


    def _setFormat_03_empty (self, dialog):
        dialog.Value = u""
        return wx.ID_OK


    def testInsertDate_01_wiki (self):
        Tester.dialogTester.append (self._setFormat_01)

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime ("%d; %m; %Y")

        self.assertEqual (self._wikipage.content, rightResult)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testInsertDate_01_html (self):
        Tester.dialogTester.append (self._setFormat_01)

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._htmlpage

        rightResult = datetime.now().strftime ("%d; %m; %Y")

        self.assertEqual (self._htmlpage.content, rightResult)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testInsertDate_02_cancel (self):
        Tester.dialogTester.append (self._setFormat_02_cancel)

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._wikipage

        self.assertEqual (self._wikipage.content, u"")
        self.assertEqual (Tester.dialogTester.count, 0)


    def testInsertDate_03_empty (self):
        Tester.dialogTester.append (self._setFormat_03_empty)

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._wikipage

        self.assertEqual (self._wikipage.content, u"")
        self.assertEqual (Tester.dialogTester.count, 0)


    def testConfig_01 (self):
        config = GeneralGuiConfig (Application.config)
        config.recentDateTimeFormat.value = "%d - %m - %Y"
        Tester.dialogTester.appendOk()

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime ("%d - %m - %Y")

        self.assertEqual (self._wikipage.content, rightResult)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testConfig_02_ignore (self):
        config = GeneralGuiConfig (Application.config)
        config.recentDateTimeFormat.value = "%d - %m - %Y"
        Tester.dialogTester.append (self._setFormat_01)

        Application.actionController.getAction (CURRENT_DATE).run (None)

        # For saving current page
        Application.selectedPage = None
        Application.selectedPage = self._wikipage

        rightResult = datetime.now().strftime ("%d; %m; %Y")

        self.assertEqual (self._wikipage.content, rightResult)
        self.assertEqual (Tester.dialogTester.count, 0)
