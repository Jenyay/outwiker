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

    def tearDown(self):
        self._clearConfig()
        self.loader.clear()

    def test_empty(self):
        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self._application)

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
        self.loader.clear()

        plugins_dirs = [u"../plugins/pagetypecolor",
                        u"../plugins/markdown",
                        ]
        self.loader.load(plugins_dirs)

        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self._application)
        colorslist.load()

        pageTypeList = colorslist.getPageTypes()

        self.assertIn(u'markdown', pageTypeList)

    def test_setColor(self):
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

    def _clearConfig(self):
        from pagetypecolor.config import PageTypeColorConfig

        self._application.config.remove_section(PageTypeColorConfig.SECTION)
