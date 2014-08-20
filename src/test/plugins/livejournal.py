# -*- coding: UTF-8 -*-

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki
from test.guitests.basemainwnd import BaseMainWndTest


class LivejournalPluginTest (BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp (self)

        self.__pluginname = u"Livejournal"

        self.__createWiki()
        self.testPage = self.wikiroot[u"Страница 1"]

        dirlist = [u"../plugins/livejournal"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self._plugin = self.loader[self.__pluginname]

        self._plugin.LJConfig (Application.config).users.value = []
        self._plugin.LJConfig (Application.config).communities.value = []

        # Application.wikiroot = self.wikiroot
        # Application.selectedPage = self.testPage


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])


    def tearDown(self):
        BaseMainWndTest.tearDown (self)
        # Application.selectedPage = None
        # Application.wikiroot = None
        removeWiki (self.path)
        self._plugin.LJConfig (Application.config).users.value = []
        self._plugin.LJConfig (Application.config).communities.value = []
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testUser1 (self):
        text = u"бла-бла-бла (:ljuser  a_str:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"""<span class='ljuser ljuser-name_a_str' lj:user='a_str' style='white-space:nowrap'><a href='http://a-str.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://a-str.livejournal.com/'><b>a_str</b></a></span>""" in result)


    def testCommunity1 (self):
        text = u"бла-бла-бла  (:ljcomm american_gangst:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"""<span class='ljuser ljuser-name_american_gangst' lj:user='american_gangst' style='white-space:nowrap'><a href='http://american-gangst.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=3' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://american-gangst.livejournal.com/'><b>american_gangst</b></a></span>""" in result)


    def testUserDialog_01 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"")
        controller.showDialog()

        valid_result = u"(:ljuser :)"

        self.assertEqual (controller.result, valid_result)


    def testUserDialog_02 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        valid_result = u"(:ljuser jenyay:)"

        self.assertEqual (controller.result, valid_result)
        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u"jenyay"])


    def testUserDialog_03 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller2.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u"jenyay"])


    def testUserDialog_04 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.UserDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u"jenyay", u"jenyay_test"])
        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u""])


    def testUserDialog_05 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.UserDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        controller3 = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller3.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u"jenyay", u"jenyay_test"])
        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u""])


    def testUserDialog_06 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        self._plugin.LJConfig (Application.config).users.value = [u"jenyay", u"jenyay_test"]

        controller = self._plugin.UserDialogController (dlg, Application, u"")
        controller.showDialog()

        valid_result = u"(:ljuser :)"

        self.assertEqual (controller.result, valid_result)
        self.assertEqual (dlg.GetStrings(), [u"jenyay", u"jenyay_test"])


    def testUserDialog_07 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.UserDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.UserDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        dlg2 = self._plugin.ComboBoxDialog (Application.mainWindow,
                                            u"",
                                            u"",
                                            wx.CB_DROPDOWN | wx.CB_SORT)
        dlg2.SetModalResult (wx.ID_OK)

        controller3 = self._plugin.UserDialogController (dlg2, Application, u"jenyay")
        controller3.showDialog()

        self.assertEqual (dlg2.GetStrings(), [u"jenyay", u"jenyay_test"])


    def testCommDialog_01 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"")
        controller.showDialog()

        valid_result = u"(:ljcomm :)"

        self.assertEqual (controller.result, valid_result)


    def testCommDialog_02 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        valid_result = u"(:ljcomm jenyay:)"

        self.assertEqual (controller.result, valid_result)
        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u"jenyay"])
        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u""])


    def testCommDialog_03 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller2.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u"jenyay"])
        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u""])


    def testCommDialog_04 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.CommunityDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u"jenyay", u"jenyay_test"])
        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u""])


    def testCommDialog_05 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.CommunityDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        controller3 = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller3.showDialog()

        self.assertEqual (self._plugin.LJConfig (Application.config).communities.value, [u"jenyay", u"jenyay_test"])
        self.assertEqual (self._plugin.LJConfig (Application.config).users.value, [u""])


    def testCommDialog_06 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        self._plugin.LJConfig (Application.config).communities.value = [u"jenyay", u"jenyay_test"]

        controller = self._plugin.CommunityDialogController (dlg, Application, u"")
        controller.showDialog()

        valid_result = u"(:ljcomm :)"

        self.assertEqual (controller.result, valid_result)
        self.assertEqual (dlg.GetStrings(), [u"jenyay", u"jenyay_test"])


    def testCommDialog_07 (self):
        dlg = self._plugin.ComboBoxDialog (Application.mainWindow,
                                           u"",
                                           u"",
                                           wx.CB_DROPDOWN | wx.CB_SORT)
        dlg.SetModalResult (wx.ID_OK)

        controller = self._plugin.CommunityDialogController (dlg, Application, u"jenyay")
        controller.showDialog()

        controller2 = self._plugin.CommunityDialogController (dlg, Application, u"jenyay_test")
        controller2.showDialog()

        dlg2 = self._plugin.ComboBoxDialog (Application.mainWindow,
                                            u"",
                                            u"",
                                            wx.CB_DROPDOWN | wx.CB_SORT)
        dlg2.SetModalResult (wx.ID_OK)

        controller3 = self._plugin.CommunityDialogController (dlg2, Application, u"jenyay")
        controller3.showDialog()

        self.assertEqual (dlg2.GetStrings(), [u"jenyay", u"jenyay_test"])
