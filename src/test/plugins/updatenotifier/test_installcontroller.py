# -*- coding: utf-8 -*-

import logging
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.appinfo import AppInfo, VersionInfo
from outwiker.core.version import Version
from test.utils import SkipLogFilter
from test.basetestcases import BaseOutWikerGUIMixin
from outwiker.gui.guiconfig import PluginsConfig


logger = logging.getLogger('UpdateNotifierPlugin')
logger.addFilter(SkipLogFilter())


class InstallControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """Tests for istallcontroller unit of the UpdateNotifier plugin."""

    def setUp(self):
        self.initApplication()
        self.loader = PluginsLoader(self.application)
        self.loader.load(["../plugins/updatenotifier"])
        self.config = PluginsConfig(self.application.config)
        self.config.disabledPlugins.value = []

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def test_get_plugin(self):
        from updatenotifier.installcontroller import InstallController

        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2"]

        self.application.plugins.load(dirlist)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = ["TestEmpty1"]
        self.application.plugins.updateDisableList()

        controller = InstallController(self.application)

        # check enabled list
        result = controller.get_plugin('TestEmpty1')
        self.assertEqual(result.name, 'TestEmpty1')

        # check disabled list
        result = controller.get_plugin('TestEmpty2')
        self.assertEqual(result.name, 'TestEmpty2')

        # check unexpected plugin
        result = controller.get_plugin('TestEmpty3')
        self.assertIs(result, None)
