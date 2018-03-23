# -*- coding: utf-8 -*-

from os.path import basename

from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUITest


class MainWndTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testProperties(self):
        self.assertNotEqual(None, self.mainWindow.treePanel.panel)
        self.assertNotEqual(None, self.mainWindow.pagePanel)
        self.assertNotEqual(None, self.mainWindow.attachPanel)
        self.assertNotEqual(None, self.mainWindow.toolbars)
        self.assertNotEqual(None, self.mainWindow.statusbar)
        self.assertNotEqual(None, self.mainWindow.taskBarIconController)
        self.assertNotEqual(None, self.mainWindow.mainWindowConfig)

    def testTitle_01(self):
        conf = MainWindowConfig(self.application.config)
        conf.titleFormat.value = "OutWiker - {page} - {file}"

        self.assertEqual(self.mainWindow.GetTitle(), "OutWiker")

        self.application.wikiroot = self.wikiroot
        self.assertEqual(self.mainWindow.GetTitle(), "OutWiker -  - {}".format(basename(self.wikiroot.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self.mainWindow.GetTitle(), "OutWiker - Страница 1 - {}".format(basename(self.wikiroot.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self.mainWindow.GetTitle(), "OutWiker - Страница 3 - {}".format(basename(self.wikiroot.path)))

    def testTitle_02(self):
        conf = MainWindowConfig(self.application.config)
        conf.titleFormat.value = "{file} - {page} - OutWiker"

        self.assertEqual(self.mainWindow.GetTitle(), "OutWiker")

        self.application.wikiroot = self.wikiroot
        self.assertEqual(self.mainWindow.GetTitle(), "{} -  - OutWiker".format(basename(self.wikiroot.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self.mainWindow.GetTitle(), "{} - Страница 1 - OutWiker".format(basename(self.wikiroot.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self.mainWindow.GetTitle(), "{} - Страница 3 - OutWiker".format(basename(self.wikiroot.path)))
