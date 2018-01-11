# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir


class PluginNameTest(unittest.TestCase):
    """Тесты плагина PluginName"""
    def setUp(self):
        self.__createWiki()

        dirlist = [u"../plugins/pluginname"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir(self.path)

        self.rootwiki = WikiDocument.create(self.path)

        WikiPageFactory().create(self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
