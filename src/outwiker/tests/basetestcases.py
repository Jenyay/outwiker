# -*- coding: utf-8 -*-

import os
from typing import Dict, Any
from abc import ABCMeta, abstractmethod
from gettext import NullTranslations
from tempfile import NamedTemporaryFile, mkdtemp

import wx

# from line_profiler import profile

from outwiker.api.core.tree import createNotesTree
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core import defines
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


NullTranslations().install()


class _WikiTestMixin:
    def createWiki(self) -> WikiDocument:
        wikipath = mkdtemp(
            prefix="OutWiker_Абырвалг абырвалг_" + str(self.__class__.__name__)
        )
        return createNotesTree(wikipath)

    def destroyWiki(self, wikiroot):
        removeDir(wikiroot.path)


class BaseOutWikerMixin(_WikiTestMixin):
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
        createBookmarksPanel=False,
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
        self.application.sharedData[defines.APP_DATA_CREATE_TAGS_PANEL] = (
            createTagsPanel
        )
        self.application.sharedData[defines.APP_DATA_CREATE_BOOKMARKS_PANEL] = (
            createBookmarksPanel
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
