# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class LivejournalPluginTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.__pluginname = "Livejournal"

        self.__createWiki()
        self.testPage = self.wikiroot["Страница 1"]

        dirlist = ["../plugins/livejournal"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        from livejournal.ljconfig import LJConfig

        LJConfig(self.application.config).users.value = []
        LJConfig(self.application.config).communities.value = []
        Tester.dialogTester.clear()

    def __createWiki(self):
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        from livejournal.ljconfig import LJConfig

        LJConfig(self.application.config).users.value = []
        LJConfig(self.application.config).communities.value = []
        self.loader.clear()
        Tester.dialogTester.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testUser1(self):
        text = "бла-бла-бла (:ljuser  a_str:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue(
            """<span class='ljuser ljuser-name_a_str' lj:user='a_str' style='white-space:nowrap'><a href='http://a-str.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://a-str.livejournal.com/'><b>a_str</b></a></span>""" in result)

    def testCommunity1(self):
        text = "бла-бла-бла  (:ljcomm american_gangst:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue(
            """<span class='ljuser ljuser-name_american_gangst' lj:user='american_gangst' style='white-space:nowrap'><a href='http://american-gangst.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=3' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://american-gangst.livejournal.com/'><b>american_gangst</b></a></span>""" in result)

    def testUserDialog_01(self):
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = UserDialogController(dlg, self.application, "")
        controller.showDialog()

        valid_result = "(:ljuser :)"

        self.assertEqual(controller.result, valid_result)

    def testUserDialog_02(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = UserDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        valid_result = "(:ljuser jenyay:)"

        self.assertEqual(controller.result, valid_result)
        self.assertEqual(LJConfig(self.application.config).users.value, ["jenyay"])

    def testUserDialog_03(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)
        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = UserDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = UserDialogController(dlg, self.application, "jenyay")
        controller2.showDialog()

        self.assertEqual(LJConfig(self.application.config).users.value, ["jenyay"])

    def testUserDialog_04(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = UserDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = UserDialogController(dlg, self.application, "jenyay_test")
        controller2.showDialog()

        self.assertEqual(LJConfig(self.application.config).users.value, [
                         "jenyay", "jenyay_test"])
        self.assertEqual(LJConfig(self.application.config).communities.value, [""])

    def testUserDialog_05(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = UserDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = UserDialogController(dlg, self.application, "jenyay_test")
        controller2.showDialog()

        Tester.dialogTester.appendOk()
        controller3 = UserDialogController(dlg, self.application, "jenyay")
        controller3.showDialog()

        self.assertEqual(LJConfig(self.application.config).users.value, [
                         "jenyay", "jenyay_test"])
        self.assertEqual(LJConfig(self.application.config).communities.value, [""])

    def testUserDialog_06(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        LJConfig(self.application.config).users.value = ["jenyay", "jenyay_test"]

        controller = UserDialogController(dlg, self.application, "")
        controller.showDialog()

        valid_result = "(:ljuser :)"

        self.assertEqual(controller.result, valid_result)
        self.assertEqual(dlg.GetStrings(), ["jenyay", "jenyay_test"])

    def testUserDialog_07(self):
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import UserDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = UserDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = UserDialogController(dlg, self.application, "jenyay_test")
        controller2.showDialog()

        dlg2 = ComboBoxDialog(self.application.mainWindow,
                              "",
                              "",
                              wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg2.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller3 = UserDialogController(dlg2, self.application, "jenyay")
        controller3.showDialog()

        self.assertEqual(dlg2.GetStrings(), ["jenyay", "jenyay_test"])

    def testCommDialog_01(self):
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = CommunityDialogController(dlg, self.application, "")
        controller.showDialog()

        valid_result = "(:ljcomm :)"

        self.assertEqual(controller.result, valid_result)

    def testCommDialog_02(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        controller = CommunityDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        valid_result = "(:ljcomm jenyay:)"

        self.assertEqual(controller.result, valid_result)
        self.assertEqual(
            LJConfig(self.application.config).communities.value, ["jenyay"])
        self.assertEqual(LJConfig(self.application.config).users.value, [""])

    def testCommDialog_03(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = CommunityDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = CommunityDialogController(dlg, self.application, "jenyay")
        controller2.showDialog()

        self.assertEqual(
            LJConfig(self.application.config).communities.value, ["jenyay"])
        self.assertEqual(LJConfig(self.application.config).users.value, [""])

    def testCommDialog_04(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = CommunityDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = CommunityDialogController(
            dlg, self.application, "jenyay_test")
        controller2.showDialog()

        self.assertEqual(LJConfig(self.application.config).communities.value, [
                         "jenyay", "jenyay_test"])
        self.assertEqual(LJConfig(self.application.config).users.value, [""])

    def testCommDialog_05(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = CommunityDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = CommunityDialogController(
            dlg, self.application, "jenyay_test")
        controller2.showDialog()

        Tester.dialogTester.appendOk()
        controller3 = CommunityDialogController(dlg, self.application, "jenyay")
        controller3.showDialog()

        self.assertEqual(LJConfig(self.application.config).communities.value, [
                         "jenyay", "jenyay_test"])
        self.assertEqual(LJConfig(self.application.config).users.value, [""])

    def testCommDialog_06(self):
        from livejournal.ljconfig import LJConfig
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()

        LJConfig(self.application.config).communities.value = [
            "jenyay", "jenyay_test"]

        controller = CommunityDialogController(dlg, self.application, "")
        controller.showDialog()

        valid_result = "(:ljcomm :)"

        self.assertEqual(controller.result, valid_result)
        self.assertEqual(dlg.GetStrings(), ["jenyay", "jenyay_test"])

    def testCommDialog_07(self):
        from livejournal.comboboxdialog import ComboBoxDialog
        from livejournal.dialogcontroller import CommunityDialogController

        dlg = ComboBoxDialog(self.application.mainWindow,
                             "",
                             "",
                             wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller = CommunityDialogController(dlg, self.application, "jenyay")
        controller.showDialog()

        Tester.dialogTester.appendOk()
        controller2 = CommunityDialogController(
            dlg, self.application, "jenyay_test")
        controller2.showDialog()

        dlg2 = ComboBoxDialog(self.application.mainWindow,
                              "",
                              "",
                              wx.CB_DROPDOWN | wx.CB_SORT)

        # dlg2.SetModalResult (wx.ID_OK)
        Tester.dialogTester.appendOk()
        controller3 = CommunityDialogController(dlg2, self.application, "jenyay")
        controller3.showDialog()

        self.assertEqual(dlg2.GetStrings(), ["jenyay", "jenyay_test"])
