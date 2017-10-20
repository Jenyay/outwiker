# -*- coding=utf-8 -*-

from tempfile import NamedTemporaryFile, mkdtemp
from unittest import TestCase

from outwiker.core.recenticonslist import RecentIconsList
from outwiker.core.config import Config
from test.utils import removeDir, createFile


class RecentIconsListTest(TestCase):
    def setUp(self):
        self.config_file = NamedTemporaryFile()
        self.config = Config(self.config_file.name)
        self.icons_path = mkdtemp(suffix=u'значки', prefix=u'outwiker')

    def tearDown(self):
        self.config_file.close()
        removeDir(self.icons_path)

    def test_empty_01(self):
        controller = RecentIconsList(10, self.config, self.icons_path)
        icons_list = controller.getRecentIcons()

        self.assertEqual(icons_list, [])

    def test_empty_02(self):
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        icons_list = controller.getRecentIcons()

        self.assertEqual(icons_list, [])