# -*- coding: utf-8 -*-

import unittest
import os
from tempfile import mkdtemp, NamedTemporaryFile
from gettext import NullTranslations

import wx

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.gui.owapplication import OutWikerApplication
from .utils import removeDir


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

    def tearDown(self):
        self._wxapp.MainLoop()
        del self._wxapp


class WikiTestMixin(object):
    def createWiki(self):
        wikipath = mkdtemp(prefix='OutWiker_Абырвалг абырвалг_' + str(self.__class__.__name__))
        return WikiDocument.create(wikipath)

    def destroyWiki(self, wikiroot):
        removeDir(wikiroot.path)


class BaseOutWikerTest(unittest.TestCase, WikiTestMixin):
    def initApplication(self):
        self._config_path = self._getConfigPath()
        self.application = Application
        self.application.clear()
        self.application.init(self._config_path)

    def destroyApplication(self):
        self.application.clear()
        self.application = None

        if os.path.exists(self._config_path):
            os.remove(self._config_path)

    def _getConfigPath(self):
        with NamedTemporaryFile(prefix='outwiker_config_', delete=False) as tmp_fp:
            return tmp_fp.name


class BaseOutWikerGUITest(BaseOutWikerTest):
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
        self.mainWindow.Destroy()
        self.outwiker_app.MainLoop()
        self.mainWindow = None
        del self.outwiker_app
        super().destroyApplication()
