# -*- coding: utf-8 -*-


import os
import unittest

from outwiker.core.defines import ICONS_STD_PREFIX
from outwiker.core.iconcontroller import IconController


class IconControllerTest(unittest.TestCase):
    def test_init_01(self):
        paths = []
        self.assertRaises(ValueError, IconController, paths)

    def test_init_02(self):
        paths = None
        self.assertRaises(ValueError, IconController, paths)

    def test_display_name_01(self):
        fname = u''
        self.assertRaises(ValueError, IconController.display_name, fname)

    def test_display_name_02(self):
        fname = None
        self.assertRaises(ValueError, IconController.display_name, fname)

    def test_display_name_03(self):
        fname = u'fname'
        display_name_right = u'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_04(self):
        fname = u'fname.png'
        display_name_right = u'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_05(self):
        fname = u'fname.jpeg'
        display_name_right = u'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_06(self):
        fname = u'fname.'
        display_name_right = u'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_07(self):
        fname = u'fname.title.png'
        display_name_right = u'fname.title'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_08(self):
        fname = ICONS_STD_PREFIX + u'fname.png'
        display_name_right = u'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_is_builtin_01(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)
        fname = u''

        self.assertRaises(ValueError, controller.is_builtin_icon, fname)

    def test_is_builtin_02(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)
        fname = None

        self.assertRaises(ValueError, controller.is_builtin_icon, fname)

    def test_is_builtin_03(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)
        fname = os.path.join(path_main, ICONS_STD_PREFIX + u'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))

    def test_is_builtin_04(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)
        fname = os.path.join(path_main, u'icon.png')

        self.assertFalse(controller.is_builtin_icon(fname))

    def test_is_builtin_05(self):
        path_main = u'tmp'
        path_second = u'tmp_2'
        icons_paths = [path_main, path_second]
        controller = IconController(icons_paths)
        fname = os.path.join(path_second, u'icon.png')

        self.assertFalse(controller.is_builtin_icon(fname))

    def test_is_builtin_06(self):
        path_main = u'tmp'
        path_second = u'tmp_2'
        icons_paths = [path_main, path_second]
        controller = IconController(icons_paths)
        fname = os.path.join(path_second, ICONS_STD_PREFIX + u'icon.png')

        self.assertFalse(controller.is_builtin_icon(fname))

    def test_is_builtin_07(self):
        path_main = u'tmp'
        path_second = u'tmp_2'
        icons_paths = [path_main, path_second]
        controller = IconController(icons_paths)
        fname = os.path.join(path_second,
                             u'qqq',
                             ICONS_STD_PREFIX + u'icon.png')

        self.assertFalse(controller.is_builtin_icon(fname))

    def test_is_builtin_08(self):
        path_main = u'tmp'
        path_second = u'tmp_2'
        icons_paths = [path_main, path_second]
        controller = IconController(icons_paths)
        fname = os.path.join(path_main,
                             u'qqq',
                             ICONS_STD_PREFIX + u'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))

    def test_is_builtin_09(self):
        path_main = u'tmp'
        path_second = u'tmp_2'
        icons_paths = [path_main, path_second]
        controller = IconController(icons_paths)
        fname = os.path.join(path_main,
                             u'абыр',
                             u'абырвалг',
                             ICONS_STD_PREFIX + u'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))
