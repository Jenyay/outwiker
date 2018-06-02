# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
from unittest import TestCase

from outwiker.core.recenticonslist import RecentIconsList
from test.utils import removeDir, createFile
from test.basetestcases import BaseOutWikerMixin


class RecentIconsListTest(BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()
        self.config = self.application.config
        self.icons_path = mkdtemp(suffix='значки', prefix='outwiker')

    def tearDown(self):
        self.destroyApplication()
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

    def test_add_icons_01(self):
        count = 1
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 1)

    def test_add_icons_02(self):
        count = 2
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 2)

    def test_add_icons_03_limit(self):
        count = 2
        controller = RecentIconsList(1, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 1)

    def test_add_icons_04_limit(self):
        count = 1
        controller = RecentIconsList(1, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 1)

    def test_add_icons_05_limit(self):
        count = 10
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 10)

    def test_add_icons_06_limit(self):
        count = 11
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()
        self.assertEqual(len(icons_list), 10)

    def test_add_icons_07(self):
        count = 1
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()

        controller2 = RecentIconsList(10, self.config, self.icons_path)
        controller2.load()
        icons_list2 = controller2.getRecentIcons()

        self.assertEqual(icons_list, icons_list2)

    def test_add_icons_08(self):
        count = 10
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, count)
        icons_list = controller.getRecentIcons()

        controller2 = RecentIconsList(10, self.config, self.icons_path)
        controller2.load()
        icons_list2 = controller2.getRecentIcons()

        self.assertEqual(icons_list, icons_list2)

    def test_add_icons_09(self):
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, 2, 'xxx')
        self._add_icons(controller, 2, 'yyy')
        icons_list = controller.getRecentIcons()

        controller2 = RecentIconsList(10, self.config, self.icons_path)
        controller2.load()
        icons_list2 = controller2.getRecentIcons()

        self.assertEqual(len(icons_list), 4)
        self.assertEqual(icons_list, icons_list2)

    def test_add_icons_10(self):
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_invalid_icons(controller, 2)
        icons_list = controller.getRecentIcons()

        controller2 = RecentIconsList(10, self.config, self.icons_path)
        controller2.load()
        icons_list2 = controller2.getRecentIcons()

        self.assertEqual(len(icons_list), 2)
        self.assertEqual(len(icons_list2), 0)

    def test_add_icons_11(self):
        controller = RecentIconsList(10, self.config, self.icons_path)
        controller.load()
        self._add_icons(controller, 2, 'xxx')
        self._add_invalid_icons(controller, 2, 'yyy')
        icons_list = controller.getRecentIcons()

        controller2 = RecentIconsList(10, self.config, self.icons_path)
        controller2.load()
        icons_list2 = controller2.getRecentIcons()

        self.assertEqual(len(icons_list), 4)
        self.assertEqual(len(icons_list2), 2)

    def _add_icons(self, controller, count, suffix_fname=''):
        for n in range(count):
            fname = 'icon_{}_{}'.format(n, suffix_fname)
            icon_path = os.path.join(self.icons_path, fname)
            createFile(icon_path)
            controller.add(icon_path)

    def _add_invalid_icons(self, controller, count, suffix_fname=''):
        for n in range(count):
            fname = 'icon_{}_{}'.format(n, suffix_fname)
            icon_path = os.path.join(self.icons_path, fname)
            controller.add(icon_path)
