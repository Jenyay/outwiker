# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class LinkCreatorTest (BaseOutWikerGUIMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        dirlist = ["plugins/markdown"]
        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self) -> None:
        self.destroyApplication()

    def test_empty_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create('', '', '')
        link_right = '[]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_empty_02(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create('   ', '', '')
        link_right = '[]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_empty_03(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create('', '   ', '')
        link_right = '[   ]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_link_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create('http://jenyay.net',
                                         'Комментарий',
                                         '')
        link_right = '[Комментарий](http://jenyay.net)'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_title_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create('http://jenyay.net',
                                         'Комментарий',
                                         'Заголовок')
        link_right = '[Комментарий](http://jenyay.net "Заголовок")'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)
