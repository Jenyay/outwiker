# -*- coding: utf-8 -*-

import logging

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.appinfo import AppInfo, VersionInfo
from outwiker.core.version import Version
from test.utils import SkipLogFilter
from test.basetestcases import BaseOutWikerGUITest


logger = logging.getLogger('UpdateNotifierPlugin')
logger.addFilter(SkipLogFilter())


class UpdateControllerTest(BaseOutWikerGUITest):
    """Tests for the UpdateNotifier plugin."""

    def setUp(self):
        self.initApplication()
        self.loader = PluginsLoader(self.application)
        self.loader.load(["../plugins/updatenotifier"])

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def test_filter_empty_01(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        currentVersionsDict = {}
        latestVersionsDict = {}

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_02(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        currentVersionsDict = {'test_01': '0.1'}
        latestVersionsDict = {}

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_03(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        currentVersionsDict = {}
        latestVersionsDict = {
            'test_01': AppInfo('test', None),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_04(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {}
        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_05(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {'test_02': '1.0'}
        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_06(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {'test_01': '1.0'}
        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_07(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(1, 1)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {'test_01': '1.0'}
        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(len(result), 1)
        self.assertEqual(result['test_01'].appname, 'test')

    def test_filter_empty_08(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(0, 9)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {'test_01': '1.0'}
        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_09(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader['UpdateNotifier'].pluginPath
        controller = UpdateController(self.application, pluginPath)

        latestVersion = Version(1, 1)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {'test_01': '1.0',
                               'test_02': '2.0',
                               }

        latestVersionsDict = {
            'test_01': AppInfo('test',
                               None,
                               versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(len(result), 1)
        self.assertEqual(result['test_01'].appname, 'test')
