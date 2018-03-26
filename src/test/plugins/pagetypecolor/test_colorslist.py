# -*- coding: utf-8 -*-

from outwiker.core.config import StringOption
from outwiker.core.pluginsloader import PluginsLoader
from test.basetestcases import BaseOutWikerGUITest


class PageTypeColor_ColorsListTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        plugins_dirs = ["../plugins/pagetypecolor"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(plugins_dirs)
        self._clearConfig()

    def tearDown(self):
        self._clearConfig()
        self.loader.clear()
        self.destroyApplication()

    def test_empty(self):
        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        pagetype = 'wiki'

        colorslist = ColorsList(self.application)

        color_param = StringOption(self.application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        self.assertIsNone(color_param.value)

        self.assertEqual(list(colorslist.getPageTypes()), [])

    def test_init(self):
        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self.application)
        colorslist.load()

        pageTypeList = colorslist.getPageTypes()

        self.assertIn('wiki', pageTypeList)
        self.assertIn('html', pageTypeList)
        self.assertIn('text', pageTypeList)
        self.assertIn('search', pageTypeList)

    def test_init_markdown(self):
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList

        colorslist = ColorsList(self.application)
        colorslist.load()

        pageTypeList = colorslist.getPageTypes()

        self.assertIn('markdown', pageTypeList)

    def test_init_markdown_config(self):
        pagetype = 'markdown'
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        colorslist = ColorsList(self.application)
        colorslist.load()

        color_param = StringOption(self.application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        self.assertIsNotNone(color_param.value)

    def test_setColor_manual(self):
        from pagetypecolor.colorslist import ColorsList
        from pagetypecolor.config import PageTypeColorConfig

        color = '#AABBCC'
        pagetype = 'wiki'

        color_param = StringOption(self.application.config,
                                   PageTypeColorConfig.SECTION,
                                   pagetype,
                                   None)
        color_param.value = color

        colorslist = ColorsList(self.application)
        colorslist.load()

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_01(self):
        from pagetypecolor.colorslist import ColorsList

        color = '#AABBCC'
        pagetype = 'wiki'

        colorslist = ColorsList(self.application)
        colorslist.load()
        colorslist.setColor(pagetype, color)

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_02(self):
        from pagetypecolor.colorslist import ColorsList

        color = '#AABBCC'
        pagetype = 'wiki'

        colorslist = ColorsList(self.application)
        colorslist.setColor(pagetype, color)

        self.assertEqual(colorslist.getColor(pagetype), color)

    def test_setColor_03(self):
        from pagetypecolor.colorslist import ColorsList

        color = '#AABBCC'
        pagetype = 'wiki'

        colorslist = ColorsList(self.application)
        colorslist.setColor(pagetype, color)

        colorslist_new = ColorsList(self.application)
        colorslist_new.load()

        self.assertEqual(colorslist_new.getColor(pagetype), color)

    def test_markdown_default(self):
        self._loadMarkdownPlugin()

        from pagetypecolor.colorslist import ColorsList

        pagetype = 'markdown'

        colorslist = ColorsList(self.application)
        colorslist.load()
        color_param = colorslist.getColor(pagetype)

        self.assertIsNotNone(color_param)
        self.assertNotEqual(color_param, 'white')

    def _clearConfig(self):
        from pagetypecolor.config import PageTypeColorConfig

        self.application.config.remove_section(PageTypeColorConfig.SECTION)

    def _loadMarkdownPlugin(self):
        self.loader.clear()

        plugins_dirs = ["../plugins/pagetypecolor",
                        "../plugins/markdown",
                        ]
        self.loader.load(plugins_dirs)
