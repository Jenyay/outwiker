# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.version import Version


class UpdateNotifierTest (unittest.TestCase):
    """Tests for the UpdateNotifier plugin."""
    def setUp(self):
        self.loader = PluginsLoader(Application)
        self.loader.load([u"../plugins/updatenotifier"])

    def tearDown(self):
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
