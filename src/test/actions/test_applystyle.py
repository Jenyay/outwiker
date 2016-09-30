# -*- coding: UTF-8 -*-

import os.path

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.applystyle import SetStyleToBranchAction


class ApplyStyleActionTest (BaseMainWndTest):
    """
    Tests for SetStyleToBranchAction
    """
    styleFile = u"__style.html"


    def __selectSecond (self, dialog):
        dialog.stylesCombo.SetSelection (1)
        return wx.ID_OK


    def __selectDefault (self, dialog):
        dialog.stylesCombo.SetSelection (0)
        return wx.ID_OK


    def testEmptyWiki (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        Tester.dialogTester.append (self.__selectSecond)

        path = os.path.join (self.wikiroot.path, self.styleFile)

        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)
        self.assertFalse (os.path.exists (path))


    def testNoneWiki (self):
        Application.wikiroot = None

        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)


    def testSingle_01 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        page = self.wikiroot[u"Викистраница"]
        path = os.path.join (page.path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Tester.dialogTester.append (self.__selectSecond)

        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (os.path.exists (path))
        self.assertTrue (os.path.exists (page.getHtmlPath()))


    def testSingle_02 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        page = self.wikiroot[u"Викистраница"]
        path = os.path.join (page.path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = page

        Tester.dialogTester.append (self.__selectSecond)

        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (os.path.exists (path))
        self.assertTrue (os.path.exists (page.getHtmlPath()))


    def testSingle_03 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        page = self.wikiroot[u"Викистраница"]
        path = os.path.join (page.path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Tester.dialogTester.append (self.__selectDefault)

        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertFalse (os.path.exists (path))


    def testSingle_04 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница", [])
        page = self.wikiroot[u"Викистраница"]
        path = os.path.join (page.path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = page

        Tester.dialogTester.append (self.__selectSecond)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (os.path.exists (path))
        self.assertTrue (os.path.exists (page.getHtmlPath()))

        Tester.dialogTester.append (self.__selectDefault)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertFalse (os.path.exists (path))


    def testMulti_01 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Викистраница 2", [])

        fname_1 = os.path.join (self.wikiroot[u"Викистраница 1"].path, self.styleFile)
        fname_2 = os.path.join (self.wikiroot[u"Викистраница 2"].path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Tester.dialogTester.append (self.__selectSecond)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertTrue (os.path.exists (fname_1))
        self.assertTrue (os.path.exists (fname_2))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1"].getHtmlPath()))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 2"].getHtmlPath()))


    def testMulti_02 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница 1", [])
        WikiPageFactory().create (self.wikiroot[u"Викистраница 1"], u"Викистраница 2", [])

        fname_1 = os.path.join (self.wikiroot[u"Викистраница 1"].path, self.styleFile)
        fname_2 = os.path.join (self.wikiroot[u"Викистраница 1/Викистраница 2"].path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Tester.dialogTester.append (self.__selectSecond)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertTrue (os.path.exists (fname_1))
        self.assertTrue (os.path.exists (fname_2))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1"].getHtmlPath()))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1/Викистраница 2"].getHtmlPath()))


    def testMulti_03 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница 1", [])
        WikiPageFactory().create (self.wikiroot[u"Викистраница 1"], u"Викистраница 2", [])

        fname_1 = os.path.join (self.wikiroot[u"Викистраница 1"].path, self.styleFile)
        fname_2 = os.path.join (self.wikiroot[u"Викистраница 1/Викистраница 2"].path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница 1"]

        Tester.dialogTester.append (self.__selectSecond)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertTrue (os.path.exists (fname_1))
        self.assertTrue (os.path.exists (fname_2))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1"].getHtmlPath()))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1/Викистраница 2"].getHtmlPath()))


    def testMulti_04 (self):
        WikiPageFactory().create (self.wikiroot, u"Викистраница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Викистраница 2", [])

        fname_1 = os.path.join (self.wikiroot[u"Викистраница 1"].path, self.styleFile)
        fname_2 = os.path.join (self.wikiroot[u"Викистраница 2"].path, self.styleFile)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Викистраница 1"]

        Tester.dialogTester.append (self.__selectSecond)
        Application.actionController.getAction (SetStyleToBranchAction.stringId).run(None)

        self.assertTrue (os.path.exists (fname_1))
        self.assertFalse (os.path.exists (fname_2))
        self.assertTrue (os.path.exists (self.wikiroot[u"Викистраница 1"].getHtmlPath()))
