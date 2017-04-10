# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.application import Application
from outwiker.core.config import StringOption
from outwiker.core.pluginsloader import PluginsLoader


class PageTypeColor_ColorsListTest(unittest.TestCase):
    def setUp(self):
        plugins_dirs = [u"../plugins/pagetypecolor"]
        self._application = Application

        self.loader = PluginsLoader(self._application)
        self.loader.load(plugins_dirs)
        self._clearConfig()

    def tearDown(self):
        self._clearConfig()
        self.loader.clear()

    def test_empty(self):
        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        pagetype = u'wiki'

        colorslist = ColorsList(self._application)

        color_param = StringOption(self._application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        self.assertIsNone(color_param.value)

        self.assertEqual(colorslist.getPageTypes(), [])

    def test_init(self):
        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self._application)
        colorslist.load()

        pageTypeList = colorslist.getPageTypes()

        self.assertIn(u'wiki', pageTypeList)
        self.assertIn(u'html', pageTypeList)
        self.assertIn(u'text', pageTypeList)
        self.assertIn(u'search', pageTypeList)

    def test_init_markdown(self):
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self._application)
        colorslist.load()

        pageTypeList = colorslist.getPageTypes()

        self.assertIn(u'markdown', pageTypeList)

    def test_init_markdown_config(self):
        pagetype = u'markdown'
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        colorslist = ColorsList(self._application)
        colorslist.load()

        color_param = StringOption(self._application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        self.assertIsNotNone(color_param.value)

    def test_setColor_manual(self):
        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        color = u'#AABBCC'
        pagetype = u'wiki'

        color_param = StringOption(self._application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        color_param.value = color

        colorslist = ColorsList(self._application)
        colorslist.load()

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_01(self):
        from pagetypecolor.colorslist import ColorsList

        color = u'#AABBCC'
        pagetype = u'wiki'

        colorslist = ColorsList(self._application)
        colorslist.load()
        colorslist.setColor(pagetype, color)

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_02(self):
        from pagetypecolor.colorslist import ColorsList

        color = u'#AABBCC'
        pagetype = u'wiki'

        colorslist = ColorsList(self._application)
        colorslist.setColor(pagetype, color)

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_03(self):
        from pagetypecolor.colorslist import ColorsList

        color = u'#AABBCC'
        pagetype = u'wiki'

        colorslist = ColorsList(self._application)
        colorslist.setColor(pagetype, color)

        colorslist_new = ColorsList(self._application)
        colorslist_new.load()

        self.assertEqual(colorslist_new.getColor(pagetype), color)

    def test_markdown_default(self):
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList

        pagetype = u'markdown'

        colorslist = ColorsList(self._application)
        colorslist.load()
        color_param = colorslist.getColor(pagetype)

        self.assertIsNotNone(color_param)
        self.assertNotEqual(color_param, u'white')

    def _clearConfig(self):
        from pagetypecolor.config import PageTypeColorConfig

        self._application.config.remove_section(PageTypeColorConfig.SECTION)

    def _loadMarkdownPlugin(self):
        self.loader.clear()

        plugins_dirs = [u"../plugins/pagetypecolor",
                        u"../plugins/markdown",
                        ]
        self.loader.load(plugins_dirs)
