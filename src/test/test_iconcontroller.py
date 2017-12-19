# -*- coding: utf-8 -*-


import os
import unittest
from tempfile import mkdtemp

from outwiker.core.defines import (ICONS_STD_PREFIX,
                                   PAGE_ICON_NAME,
                                   ICONS_EXTENSIONS)
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.iconcontroller import IconController
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory

from test.utils import removeDir


class IconControllerTest(unittest.TestCase):
    def setUp(self):
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.eventcount = 0

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        self._page = factory.create(self.wikiroot, "Страница 1", [])
        self._page.root.onPageUpdate += self._onPageUpdate

    def tearDown(self):
        self._page.root.onPageUpdate -= self._onPageUpdate
        removeDir(self.path)

    def _create_file(self, fname):
        fp = open(fname, 'w')
        fp.close()

    def _onPageUpdate(self, page, change):
        self.eventcount += 1

    def test_display_name_01(self):
        fname = ''
        self.assertRaises(ValueError, IconController.display_name, fname)

    def test_display_name_02(self):
        fname = None
        self.assertRaises(ValueError, IconController.display_name, fname)

    def test_display_name_03(self):
        fname = 'fname'
        display_name_right = 'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_04(self):
        fname = 'fname.png'
        display_name_right = 'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_05(self):
        fname = 'fname.jpeg'
        display_name_right = 'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_06(self):
        fname = 'fname.'
        display_name_right = 'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_07(self):
        fname = 'fname.title.png'
        display_name_right = 'fname.title'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_display_name_08(self):
        fname = ICONS_STD_PREFIX + 'fname.png'
        display_name_right = 'fname'

        result = IconController.display_name(fname)
        self.assertEqual(result, display_name_right)

    def test_is_builtin_invalid_fname_01(self):
        icons_path = 'tmp'
        controller = IconController(icons_path)
        fname = ''

        self.assertRaises(ValueError, controller.is_builtin_icon, fname)

    def test_is_builtin_invalid_fname_02(self):
        icons_path = 'tmp'
        controller = IconController(icons_path)
        fname = None

        self.assertRaises(ValueError, controller.is_builtin_icon, fname)

    def test_is_builtin_03(self):
        path_main = 'tmp'
        controller = IconController(path_main)
        fname = os.path.join(path_main, ICONS_STD_PREFIX + 'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))

    def test_is_builtin_04(self):
        path_main = 'tmp'
        controller = IconController(path_main)
        fname = os.path.join(path_main, 'icon.png')

        self.assertFalse(controller.is_builtin_icon(fname))

    def test_is_builtin_08(self):
        path_main = 'tmp'
        controller = IconController(path_main)
        fname = os.path.join(path_main,
                             'qqq',
                             ICONS_STD_PREFIX + 'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))

    def test_is_builtin_09(self):
        path_main = 'tmp'
        controller = IconController(path_main)
        fname = os.path.join(path_main,
                             'абыр',
                             'абырвалг',
                             ICONS_STD_PREFIX + 'icon.png')

        self.assertTrue(controller.is_builtin_icon(fname))

    def test_get_icon_01(self):
        icons_path = 'tmp'
        controller = IconController(icons_path)

        icon = controller.get_icon(self._page)
        self.assertIsNone(icon)

    def test_get_icon_02(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = 'example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, icon_fname)

        self.assertEqual(result, result_right)

    def test_get_icon_03(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = 'subdir/example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, 'subdir', 'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_04(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = 'subdir\\example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, 'subdir', 'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_05(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.png')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_06(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.jpg')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_07(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.jpeg')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_08(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.gif')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_09(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.bmp')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_10(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.xxx')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = None

        self.assertEqual(result, result_right)

    def test_get_icon_11(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.xxx')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = 'subdir\\example.png'

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, 'subdir', 'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_12(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.png')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = 'subdir\\example.png'

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_13(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + '.png')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = 'subdir/example.png'

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_set_icon_builtin_01(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = ICONS_STD_PREFIX + 'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, '')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_02(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = ICONS_STD_PREFIX + 'icon.png'
        icon_path = os.path.join(path_main, icon_fname)
        icon_path = os.path.abspath(icon_path)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, '')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_03(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(
            'подпапка',
            ICONS_STD_PREFIX + 'icon.png')

        icon_path = os.path.join(path_main, icon_fname)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, '')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_04(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = os.path.join(
            'подпапка',
            ICONS_STD_PREFIX + 'icon.png')

        icon_path = os.path.join(path_main, icon_fname)
        icon_path = os.path.abspath(icon_path)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, '')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_event(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = ICONS_STD_PREFIX + 'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        self.assertEqual(self.eventcount, 0)

        controller.set_icon(self._page, icon_path)
        self.assertEqual(self.eventcount, 1)

        controller.set_icon(self._page, icon_path)
        self.assertEqual(self.eventcount, 2)

    def test_set_icon_custom_png(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.png'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.png'))
        )

    def test_set_icon_custom_gif(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.gif'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.gif'))
        )

    def test_set_icon_custom_bmp(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.bmp'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.bmp'))
        )

    def test_set_icon_custom_jpg(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.jpg'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.jpg'))
        )

    def test_set_icon_custom_jpeg(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.jpeg'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.jpeg'))
        )

    def test_set_icon_custom_ico(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.ico'

        controller.set_icon(self._page, icon_path)

        self.assertTrue(os.path.exists(
            os.path.join(self._page.path, PAGE_ICON_NAME + '.ico'))
        )

    def test_set_icon_custom_remove_param(self):
        self._page.params.iconOption.value = 'icon.png'

        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.png'
        controller.set_icon(self._page, icon_path)

        self.assertEqual(self._page.params.iconOption.value, '')

    def test_set_icon_custom_event(self):
        self._page.params.iconOption.value = 'icon.png'

        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/icon.png'

        self.assertEqual(self.eventcount, 0)

        controller.set_icon(self._page, icon_path)
        self.assertEqual(self.eventcount, 1)

        controller.set_icon(self._page, icon_path)
        self.assertEqual(self.eventcount, 2)

    def test_set_icon_builtin_remove_files(self):
        path_main = 'tmp'

        # Create icons files in the page folder
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + '.' + extension)
            self._create_file(icon_fname)

        controller = IconController(path_main)

        icon_fname = os.path.join(
            'подпапка',
            ICONS_STD_PREFIX + 'icon.png')

        icon_path = os.path.join(path_main, icon_fname)
        controller.set_icon(self._page, icon_path)

        # Checking custom icon files
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + '.' + extension)
            self.assertFalse(os.path.exists(icon_fname), icon_fname)

    def test_set_icon_invalid_extension_01(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = ICONS_STD_PREFIX + 'icon.xxx'
        icon_path = os.path.join(path_main, icon_fname)

        icon_path = os.path.abspath(icon_path)

        self.assertRaises(ValueError,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_set_icon_invalid_extension_02(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/16x16.xxx'

        self.assertRaises(ValueError,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_set_icon_custom_invalid_fname(self):
        path_main = 'tmp'
        controller = IconController(path_main)

        icon_path = '../test/images/16x16_invalid.png'

        self.assertRaises(IOError,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_set_icon_readonly(self):
        self._page.readonly = True

        path_main = 'tmp'
        controller = IconController(path_main)

        icon_fname = ICONS_STD_PREFIX + 'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        icon_path = os.path.abspath(icon_path)

        self.assertRaises(ReadonlyException,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_remove_icon_01(self):
        path_main = 'tmp'

        # Create icons files in the page folder
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + '.' + extension)
            self._create_file(icon_fname)

        controller = IconController(path_main)
        controller.remove_icon(self._page)

        # Checking custom icon files
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + '.' + extension)
            self.assertFalse(os.path.exists(icon_fname), icon_fname)

    def test_remove_icon_02(self):
        path_main = 'tmp'

        self._page.params.iconOption.value = 'icon.png'

        controller = IconController(path_main)
        controller.remove_icon(self._page)

        # Checking built-in icon
        self.assertEqual(self._page.params.iconOption.value, '')

    def test_remove_icon_event(self):
        path_main = 'tmp'

        self._page.params.iconOption.value = 'icon.png'

        controller = IconController(path_main)

        self.assertEqual(self.eventcount, 0)

        controller.remove_icon(self._page)
        self.assertEqual(self.eventcount, 1)

        controller.remove_icon(self._page)
        self.assertEqual(self.eventcount, 2)

    def test_remove_icon_readonly(self):
        self._page.readonly = True

        path_main = 'tmp'
        controller = IconController(path_main)

        self.assertRaises(ReadonlyException,
                          controller.remove_icon,
                          self._page)
