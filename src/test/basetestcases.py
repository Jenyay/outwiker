# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import unittest
import os
from tempfile import mkdtemp, NamedTemporaryFile
from gettext import NullTranslations

import wx

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.gui.owapplication import OutWikerApplication
from .utils import removeDir

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory


NullTranslations().install()


class BaseWxTestCase(unittest.TestCase):
    def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
        """
        Since the tests are usually run before MainLoop is called then we
        need to make our own EventLoop for Yield to actually do anything
        useful.

        The method taken from wxPython tests.
        """
        evtLoop = self._wxapp.GetTraits().CreateEventLoop()
        activator = wx.EventLoopActivator(evtLoop)
        evtLoop.YieldFor(eventsToProcess)

    def setUp(self):
        self._wxapp = wx.App()
        self.mainWindow = None

    def tearDown(self):
        if self.mainWindow is not None:
            self.mainWindow.Close()

        self._wxapp.MainLoop()
        del self._wxapp

    def initMainWindow(self):
        self.mainWindow = wx.Frame(None)
        self._wxapp.SetTopWindow(self.mainWindow)
        return self.mainWindow


class WikiTestMixin(object):
    def createWiki(self):
        wikipath = mkdtemp(prefix='OutWiker_Абырвалг абырвалг_' + str(self.__class__.__name__))
        return WikiDocument.create(wikipath)

    def destroyWiki(self, wikiroot):
        removeDir(wikiroot.path)


class BaseOutWikerMixin(WikiTestMixin):
    def initApplication(self):
        self._config_path = self._getConfigPath()
        self.application = Application
        self.application.clear()
        self.application.init(self._config_path)
        self.setLanguage('en')

    def setLanguage(self, lang):
        i18config = I18nConfig(self.application.config)
        i18config.languageOption.value = lang

    def destroyApplication(self):
        self.application.clear()
        self.application = None

        if os.path.exists(self._config_path):
            os.remove(self._config_path)

    def _getConfigPath(self):
        with NamedTemporaryFile(prefix='outwiker_config_', delete=False) as tmp_fp:
            return tmp_fp.name


class BaseOutWikerGUIMixin(BaseOutWikerMixin):
    def initApplication(self):
        super().initApplication()

        self.outwiker_app = OutWikerApplication(self.application)
        self.outwiker_app.initMainWindow()
        self.mainWindow = self.outwiker_app.mainWnd

        generalConfig = GeneralGuiConfig(self.application.config)
        generalConfig.askBeforeExit.value = False
        wx.Log.SetLogLevel(0)

        Tester.dialogTester.clear()

    def destroyApplication(self):
        Tester.dialogTester.clear()
        self.outwiker_app.destroyMainWindow()
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

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.__createWiki()

        dirlist = [self.getPluginDir()]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def __createWiki(self):
        # Здесь будет создаваться вики
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
