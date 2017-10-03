# -*- coding: utf-8 -*-


import unittest

from outwiker.core.defines import ICONS_STD_PREFIX
from outwiker.core.iconcontroller import IconController


class IconControllerTest(unittest.TestCase):
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
