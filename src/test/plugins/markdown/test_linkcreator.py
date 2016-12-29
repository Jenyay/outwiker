# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class LinkCreatorTest (unittest.TestCase):

    def setUp(self):
        dirlist = [u"../plugins/markdown"]
        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def test_empty_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create(u'', u'', u'')
        link_right = u'[]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_empty_02(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create(u'   ', u'', u'')
        link_right = u'[]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_empty_03(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create(u'', u'   ', u'')
        link_right = u'[   ]()'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_link_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create(u'http://jenyay.net',
                                         u'Комментарий',
                                         u'')
        link_right = u'[Комментарий](http://jenyay.net)'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)

    def test_title_01(self):
        from markdown.links.linkcreator import LinkCreator
        creator = LinkCreator()
        link, reference = creator.create(u'http://jenyay.net',
                                         u'Комментарий',
                                         u'Заголовок')
        link_right = u'[Комментарий](http://jenyay.net "Заголовок")'

        self.assertEqual(link, link_right)
        self.assertIsNone(reference)
