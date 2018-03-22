# -*- coding: utf-8 -*-

import os
import unittest
from os.path import basename
from tempfile import mkdtemp, NamedTemporaryFile

from outwiker.gui.owapplication import OutWikerApplication
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.guiconfig import GeneralGuiConfig, MainWindowConfig
from outwiker.core.tree import WikiDocument
from outwiker.gui.tester import Tester
from test.utils import removeDir

# from .basemainwnd import BaseMainWndTest


class MainWndTest(unittest.TestCase):
    def setUp(self):
        with NamedTemporaryFile(prefix='outwiker_config_', delete=False) as tmp_fp:
            self._config_path = tmp_fp.name

        self._outwiker_app = OutWikerApplication(self._config_path)
        self._application = self._outwiker_app.application
        self._mainWindow = self._outwiker_app.mainWnd

        # A code from the BaseMainWndTest class begin
        self.path = mkdtemp(prefix='OutWiker_Абырвалг абырвалг_' + str(self.__class__.__name__))

        self._application.config.remove_section(MainWindowConfig.MAIN_WINDOW_SECTION)

        generalConfig = GeneralGuiConfig(self._application.config)
        generalConfig.askBeforeExit.value = False

        self.wikiroot = WikiDocument.create(self.path)

        Tester.dialogTester.clear()
        self._application.wikiroot = None
        # The code from the BaseMainWndTest class end

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def tearDown(self):
        self._mainWindow.Destroy()
        self._outwiker_app.MainLoop()
        del self._outwiker_app

        removeDir(self.path)
        if os.path.exists(self._config_path):
            os.remove(self._config_path)

    def testProperties(self):
        self.assertNotEqual(None, self._mainWindow.treePanel.panel)
        self.assertNotEqual(None, self._mainWindow.pagePanel)
        self.assertNotEqual(None, self._mainWindow.attachPanel)
        self.assertNotEqual(None, self._mainWindow.toolbars)
        self.assertNotEqual(None, self._mainWindow.statusbar)
        self.assertNotEqual(None, self._mainWindow.taskBarIconController)
        self.assertNotEqual(None, self._mainWindow.mainWindowConfig)

    def testTitle1(self):
        conf = MainWindowConfig(self._application.config)
        conf.titleFormat.value = "OutWiker - {page} - {file}"

        self.assertEqual(self._mainWindow.GetTitle(), "OutWiker")

        self._application.wikiroot = self.wikiroot
        self.assertEqual(self._mainWindow.GetTitle(), "OutWiker -  - {}".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self._mainWindow.GetTitle(), "OutWiker - Страница 1 - {}".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self._mainWindow.GetTitle(), "OutWiker - Страница 3 - {}".format(basename(self.path)))

    def testTitle2(self):
        conf = MainWindowConfig(self._application.config)
        conf.titleFormat.value = "{file} - {page} - OutWiker"

        self.assertEqual(self._mainWindow.GetTitle(), "OutWiker")

        self._application.wikiroot = self.wikiroot
        self.assertEqual(self._mainWindow.GetTitle(), "{} -  - OutWiker".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self._mainWindow.GetTitle(), "{} - Страница 1 - OutWiker".format(basename(self.path)))

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self._mainWindow.GetTitle(), "{} - Страница 3 - OutWiker".format(basename(self.path)))
