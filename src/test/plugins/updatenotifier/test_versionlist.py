# -*- coding: UTF-8 -*-

import unittest
import logging

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import SkipLogFilter


logger = logging.getLogger('UpdateNotifierPlugin')
logger.addFilter(SkipLogFilter())


class VersionListTest (unittest.TestCase):
    """Tests for the UpdateNotifier plugin."""
    def setUp(self):
        self.loader = PluginsLoader(Application)
        self.loader.load(["../plugins/updatenotifier"])

    def tearDown(self):
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def test_empty(self):
        from updatenotifier.versionlist import VersionList

        updateUrls = {}
        versionList = VersionList(updateUrls)
        result = versionList.loadAppInfo()

        self.assertEqual(result, {})

    def test_loadAppInfo_invalid_01(self):
        from updatenotifier.versionlist import VersionList

        updateUrls = {
            'test_01': 'http://example.com/',
        }
        versionList = VersionList(updateUrls)
        result = versionList.loadAppInfo()

        self.assertEqual(result, {})

    def test_loadAppInfo_invalid_02(self):
        from updatenotifier.versionlist import VersionList

        updateUrls = {
            'test_01': 'invalid_file_name.txt',
        }
        versionList = VersionList(updateUrls)
        result = versionList.loadAppInfo()

        self.assertEqual(result, {})

    def test_loadAppInfo_file_01(self):
        from updatenotifier.versionlist import VersionList

        updateUrls = {
            'test_01': '../test/updatenotifier_data/testplugin_01.xml',
        }
        versionList = VersionList(updateUrls)
        result = versionList.loadAppInfo()

        self.assertIn('test_01', result)
        self.assertEqual(str(result['test_01'].currentVersion), '0.1')

    def test_loadAppInfo_file_02(self):
        from updatenotifier.versionlist import VersionList

        updateUrls = {
            'test_01': '../test/updatenotifier_data/testplugin_01.xml',
            'test_02': '../test/updatenotifier_data/testplugin_02.xml',
        }
        versionList = VersionList(updateUrls)
        result = versionList.loadAppInfo()

        self.assertIn('test_01', result)
        self.assertIn('test_02', result)
        self.assertEqual(str(result['test_01'].currentVersion), '0.1')
        self.assertEqual(str(result['test_02'].currentVersion), '0.2')

    def test_getAppInfo_file_01(self):
        from updatenotifier.versionlist import VersionList

        url = '../test/updatenotifier_data/testplugin_01.xml'
        versionList = VersionList({})
        appInfo = versionList.getAppInfoFromUrl(url)

        self.assertEqual(str(appInfo.currentVersion), '0.1')

    def test_getAppInfo_file_invalid_01(self):
        from updatenotifier.versionlist import VersionList

        url = 'invalid_path.xml'
        versionList = VersionList({})
        appInfo = versionList.getAppInfoFromUrl(url)

        self.assertEqual(appInfo, None)

    def test_getAppInfo_file_invalid_02(self):
        from updatenotifier.versionlist import VersionList

        url = 'http://example.com'
        versionList = VersionList({})
        appInfo = versionList.getAppInfoFromUrl(url)

        self.assertEqual(appInfo, None)

    def test_getAppInfo_file_invalid_03(self):
        from updatenotifier.versionlist import VersionList

        versionList = VersionList({})
        appInfo = versionList.getAppInfoFromUrl(None)

        self.assertEqual(appInfo, None)
