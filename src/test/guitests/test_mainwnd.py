# -*- coding: utf-8 -*-

from os.path import basename

from outwiker.core.application import Application
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest


class MainWndTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def testProperties(self):
        self.assertNotEqual(None, self.wnd.treePanel.panel)
        self.assertNotEqual(None, self.wnd.pagePanel)
        self.assertNotEqual(None, self.wnd.attachPanel)
        self.assertNotEqual(None, self.wnd.toolbars)
        self.assertNotEqual(None, self.wnd.statusbar)
        self.assertNotEqual(None, self.wnd.taskBarIconController)
        self.assertNotEqual(None, self.wnd.mainWindowConfig)

    def testTitle1(self):
        conf = MainWindowConfig(Application.config)
        conf.titleFormat.value = "OutWiker - {page} - {file}"

        self.assertEqual(self.wnd.GetTitle(), "OutWiker")

        Application.wikiroot = self.wikiroot
        self.assertEqual(self.wnd.GetTitle(), "OutWiker -  - {}".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self.wnd.GetTitle(), "OutWiker - Страница 1 - {}".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self.wnd.GetTitle(), "OutWiker - Страница 3 - {}".format(basename(self.path)))

    def testTitle2(self):
        conf = MainWindowConfig(Application.config)
        conf.titleFormat.value = "{file} - {page} - OutWiker"

        self.assertEqual(self.wnd.GetTitle(), "OutWiker")

        Application.wikiroot = self.wikiroot
        self.assertEqual(self.wnd.GetTitle(), "{} -  - OutWiker".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self.wnd.GetTitle(), "{} - Страница 1 - OutWiker".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self.wnd.GetTitle(), "{} - Страница 3 - OutWiker".format(basename(self.path)))
