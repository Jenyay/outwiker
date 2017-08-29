# -*- coding: UTF-8 -*-

import unittest
import logging

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.appinfo import AppInfo, VersionInfo
from outwiker.core.application import Application
from outwiker.core.version import Version
from test.utils import SkipLogFilter


logger = logging.getLogger('UpdateNotifierPlugin')
logger.addFilter(SkipLogFilter())


class UpdateControllerTest(unittest.TestCase):
    """Tests for the UpdateNotifier plugin."""
    def setUp(self):
        self.loader = PluginsLoader(Application)
        self.loader.load([u"../plugins/updatenotifier"])

    def tearDown(self):
        self.loader.clear()

    def test_filter_empty_01(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        currentVersionsDict = {}
        latestVersionsDict = {}

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_02(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        currentVersionsDict = {u'test_01': u'0.1'}
        latestVersionsDict = {}

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_03(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        currentVersionsDict = {}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test', None),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_04(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_05(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {u'test_02': u'1.0'}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_empty_06(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(1, 0)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {u'test_01': u'1.0'}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_07(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(1, 1)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {u'test_01': u'1.0'}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[u'test_01'].appname, u'test')

    def test_filter_empty_08(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(0, 9)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {u'test_01': u'1.0'}
        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(result, {})

    def test_filter_09(self):
        from updatenotifier.updatecontroller import UpdateController

        pluginPath = self.loader[u'UpdateNotifier'].pluginPath
        controller = UpdateController(Application, pluginPath)

        latestVersion = Version(1, 1)
        latestVersionInfo = VersionInfo(latestVersion)

        currentVersionsDict = {u'test_01': u'1.0',
                               u'test_02': u'2.0',
                               }

        latestVersionsDict = {
            u'test_01': AppInfo(u'test',
                                None,
                                versionsList=[latestVersionInfo]),
        }

        result = controller.filterUpdatedApps(currentVersionsDict,
                                              latestVersionsDict)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[u'test_01'].appname, u'test')
