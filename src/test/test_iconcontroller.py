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
        self.path = mkdtemp(prefix=u'Абырвалг абыр')
        self.eventcount = 0

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        self._page = factory.create(self.wikiroot, u"Страница 1", [])

    def tearDown(self):
        removeDir(self.path)

    def _create_file(self, fname):
        fp = open(fname, 'w')
        fp.close()

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

    def test_is_builtin_invalid_fname_01(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)
        fname = u''

        self.assertRaises(ValueError, controller.is_builtin_icon, fname)

    def test_is_builtin_invalid_fname_02(self):
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

    def test_get_icon_01(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon = controller.get_icon(self._page)
        self.assertIsNone(icon)

    def test_get_icon_02(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = u'example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, icon_fname)

        self.assertEqual(result, result_right)

    def test_get_icon_03(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = u'subdir/example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, u'subdir', u'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_04(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = u'subdir\\example.png'
        self._page.params.iconOption.value = icon_fname

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, u'subdir', u'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_05(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.png')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_06(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.jpg')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_07(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.jpeg')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_08(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.gif')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_09(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.bmp')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_10(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.xxx')
        self._create_file(icon_fname)

        result = controller.get_icon(self._page)
        result_right = None

        self.assertEqual(result, result_right)

    def test_get_icon_11(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.xxx')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = u'subdir\\example.png'

        result = controller.get_icon(self._page)
        result_right = os.path.join(path_main, u'subdir', u'example.png')

        self.assertEqual(result, result_right)

    def test_get_icon_12(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.png')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = u'subdir\\example.png'

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_get_icon_13(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(self._page.path, PAGE_ICON_NAME + u'.png')
        self._create_file(icon_fname)

        self._page.params.iconOption.value = u'subdir/example.png'

        result = controller.get_icon(self._page)
        result_right = icon_fname

        self.assertEqual(result, result_right)

    def test_set_icon_builtin_01(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = ICONS_STD_PREFIX + u'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, u'')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_02(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = ICONS_STD_PREFIX + u'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        icon_path = os.path.abspath(icon_path)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, u'')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_03(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(
            u'подпапка',
            ICONS_STD_PREFIX + u'icon.png')

        icon_path = os.path.join(path_main, icon_fname)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, u'')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    def test_set_icon_builtin_04(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = os.path.join(
            u'подпапка',
            ICONS_STD_PREFIX + u'icon.png')

        icon_path = os.path.join(path_main, icon_fname)
        icon_path = os.path.abspath(icon_path)

        controller.set_icon(self._page, icon_path)

        self.assertNotEqual(self._page.params.iconOption.value, u'')
        self.assertEqual(icon_fname, self._page.params.iconOption.value)

    # def test_set_icon_custom_01(self):
    #     path_main = u'tmp'
    #     icons_paths = [path_main]
    #     controller = IconController(icons_paths)
    #
    #     icon_fname = u'../test/images/16x16.png'

    def test_set_icon_builtin_remove_files(self):
        path_main = u'tmp'
        icons_paths = [path_main]

        # Create icons files in the page folder
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + u'.' + extension)
            self._create_file(icon_fname)

        controller = IconController(icons_paths)

        icon_fname = os.path.join(
            u'подпапка',
            ICONS_STD_PREFIX + u'icon.png')

        icon_path = os.path.join(path_main, icon_fname)
        controller.set_icon(self._page, icon_path)

        # Checking custom icon files
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + u'.' + extension)
            self.assertFalse(os.path.exists(icon_fname), icon_fname)

    def test_set_icon_invalid_extension(self):
        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = ICONS_STD_PREFIX + u'icon.xxx'
        icon_path = os.path.join(path_main, icon_fname)

        icon_path = os.path.abspath(icon_path)

        self.assertRaises(ValueError,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_set_icon_readonly(self):
        self._page.readonly = True

        path_main = u'tmp'
        icons_paths = [path_main]
        controller = IconController(icons_paths)

        icon_fname = ICONS_STD_PREFIX + u'icon.png'
        icon_path = os.path.join(path_main, icon_fname)

        icon_path = os.path.abspath(icon_path)

        self.assertRaises(ReadonlyException,
                          controller.set_icon,
                          self._page,
                          icon_path)

    def test_remove_icon_01(self):
        path_main = u'tmp'
        icons_paths = [path_main]

        # Create icons files in the page folder
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + u'.' + extension)
            self._create_file(icon_fname)

        controller = IconController(icons_paths)
        controller.remove_icon(self._page)

        # Checking custom icon files
        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(self._page.path,
                                      PAGE_ICON_NAME + u'.' + extension)
            self.assertFalse(os.path.exists(icon_fname), icon_fname)

    def test_remove_icon_02(self):
        path_main = u'tmp'
        icons_paths = [path_main]

        self._page.params.iconOption.value = u'icon.png'

        controller = IconController(icons_paths)
        controller.remove_icon(self._page)

        # Checking built-in icon
        self.assertEqual(self._page.params.iconOption.value, u'')
