# -*- coding: utf-8 -*-

import locale
import os
from typing import Dict, Any
import unittest
from abc import ABCMeta, abstractmethod
from gettext import NullTranslations
from tempfile import NamedTemporaryFile, mkdtemp

import wx

# from line_profiler import profile

from outwiker.api.core.tree import createNotesTree
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from .utils import removeDir
import outwiker.core.defines as defines


NullTranslations().install()


class WikiTestMixin:
    def createWiki(self) -> WikiDocument:
        wikipath = mkdtemp(
            prefix="OutWiker_Абырвалг абырвалг_" + str(self.__class__.__name__)
        )
        return createNotesTree(wikipath)

    def destroyWiki(self, wikiroot):
        removeDir(wikiroot.path)


class BaseWxTestCase(unittest.TestCase):
    def setUp(self):
        self._wxapp = wx.App()
        locale.setlocale(locale.LC_ALL, "")
        self.mainWindow = None

    def tearDown(self):
        if self.mainWindow is not None:
            self.mainWindow.Close()

        wx.SafeYield()
        self._wxapp.MainLoop()
        del self._wxapp

    def initMainWindow(self):
        self.mainWindow = wx.Frame(None)
        self._wxapp.SetTopWindow(self.mainWindow)
        return self.mainWindow


class BaseOutWikerMixin(WikiTestMixin):
    def initApplication(self, lang="en"):
        self._config_path = self._getConfigPath()
        self.application = Application()
        self.application.clear()
        self.application.init(self._config_path)
        self.application.testMode = True
        self._setLanguage(lang)

    def _setLanguage(self, lang):
        i18config = I18nConfig(self.application.config)
        i18config.languageOption.value = lang

    def destroyApplication(self):
        self.application.clear()
        self.application = None

        if os.path.exists(self._config_path):
            os.remove(self._config_path)

    def _getConfigPath(self):
        with NamedTemporaryFile(prefix="outwiker_config_", delete=False) as tmp_fp:
            return tmp_fp.name


class BaseOutWikerGUIMixin(BaseOutWikerMixin):
    # @profile
    def initApplication(
        self,
        lang="en",
        enableActionsGui=False,
        createTreePanel=False,
        createAttachPanel=False,
        createTagsPanel=False,
    ):
        super().initApplication(lang)
        self.application.sharedData[defines.APP_DATA_CREATE_TREE_PANEL] = (
            createTreePanel
        )
        self.application.sharedData[defines.APP_DATA_CREATE_ATTACH_PANEL] = (
            createAttachPanel
        )
        self.application.sharedData[defines.APP_DATA_CREATE_TAGS_PANEL] = (
            createTagsPanel
        )

        self.outwiker_app = OutWikerApplication(self.application)
        self.outwiker_app.use_fake_html_render = True
        self.outwiker_app.enableActionsGui = enableActionsGui
        self.outwiker_app.initMainWindow()
        self.mainWindow = self.outwiker_app.getMainWindow()

        generalConfig = GeneralGuiConfig(self.application.config)
        generalConfig.askBeforeExit.value = False
        wx.Log.SetLogLevel(0)

        Tester.dialogTester.clear()

    # @profile
    def destroyApplication(self):
        Tester.dialogTester.clear()
        self.outwiker_app.destroyMainWindow()
        wx.SafeYield()
        self.outwiker_app.MainLoop()
        self.mainWindow = None
        del self.outwiker_app
        self.outwiker_app = None
        super().destroyApplication()


class PluginLoadingMixin(BaseOutWikerGUIMixin, metaclass=ABCMeta):
    @abstractmethod
    def getPluginDir(self):
        """
        Должен возвращать путь до папки с тестируемым плагином
        """
        pass

    @abstractmethod
    def getPluginName(self):
        """
        Должен возвращать имя плагина,
        по которому его можно найти в PluginsLoader
        """
        pass

    def isEnabledActionsGui(self) -> bool:
        return False

    def getInitApplicationParams(self) -> Dict[str, Any]:
        return {}

    def setUp(self):
        self.initApplication(
            enableActionsGui=self.isEnabledActionsGui(),
            **self.getInitApplicationParams(),
        )
        self.wikiroot = self.createWiki()
        self.__createWiki()

        dirlist = [self.getPluginDir()]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def __createWiki(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        TextPageFactory().create(self.wikiroot, "Текст", [])
        HtmlPageFactory().create(self.wikiroot, "HTML", [])
        SearchPageFactory().create(self.wikiroot, "Search", [])

    def tearDown(self):
        self.application.selectedPage = None
        self.application.wikiroot = None
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
        self.assertNotEqual(self.loader[self.getPluginName()], None)

    def testDestroy_01(self):
        self.application.wikiroot = None
        self.loader.clear()

    def testDestroy_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.loader.clear()

    def testDestroy_03(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.loader.clear()

    def testDestroy_04(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Текст"]
        self.loader.clear()

    def testDestroy_05(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML"]
        self.loader.clear()

    def testDestroy_06(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Search"]
        self.loader.clear()

    def testDestroy_07(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.loader.disable(self.getPluginName())

        action = self.application.actionController.getAction(
            SwitchCodeResultAction.stringId
        )
        action.run(None)
        self.loader.clear()

    def testDestroy_08(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML"]
        self.loader.disable(self.getPluginName())

        action = self.application.actionController.getAction(
            SwitchCodeResultAction.stringId
        )
        action.run(None)
        self.loader.clear()

    def testDestroy_09(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Викистраница"]
        self.loader.clear()

        action = self.application.actionController.getAction(
            SwitchCodeResultAction.stringId
        )
        action.run(None)

    def testDestroy_10(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["HTML"]
        self.loader.clear()

        action = self.application.actionController.getAction(
            SwitchCodeResultAction.stringId
        )
        action.run(None)
