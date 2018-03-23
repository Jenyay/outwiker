# -*- coding: utf-8 -*-

import unittest
import os
from tempfile import mkdtemp, NamedTemporaryFile

import wx

from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.gui.owapplication import OutWikerApplication
from outwiker.core.tree import WikiDocument
from .utils import removeDir


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


class BaseOutWikerGUITest(unittest.TestCase, WikiTestMixin):
    def initApplication(self):
        self._config_path = self._getConfigPath()

        self.outwiker_app = OutWikerApplication(self._config_path)
        self.outwiker_app.initMainWindow()
        self.application = self.outwiker_app.application
        self.mainWindow = self.outwiker_app.mainWnd

        generalConfig = GeneralGuiConfig(self.application.config)
        generalConfig.askBeforeExit.value = False
        wx.Log.SetLogLevel(0)

        Tester.dialogTester.clear()
        self.application.wikiroot = None

    def destroyApplication(self):
        self.mainWindow.Destroy()
        self.outwiker_app.MainLoop()
        self.application = None
        self.mainWindow = None
        del self.outwiker_app

        if os.path.exists(self._config_path):
            os.remove(self._config_path)

        Tester.dialogTester.clear()

    def _getConfigPath(self):
        with NamedTemporaryFile(prefix='outwiker_config_', delete=False) as tmp_fp:
            return tmp_fp.name
