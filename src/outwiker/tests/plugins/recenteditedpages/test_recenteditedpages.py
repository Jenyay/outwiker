# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.pages.wiki.wikipage import createWikiPage
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.tests.utils import removeDir


class PluginNameTest(unittest.TestCase):
    """Tests for the RecentEditedPages plug-in"""

    def setUp(self):
        self.__createWiki()

        dirlist = ["plugins/recenteditedpages"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = self.path = mkdtemp(prefix='Абырвалг абыр RecentEditedPages')
        removeDir(self.path)

        self.rootwiki = WikiDocument.create(self.path)

        createWikiPage(self.rootwiki, "Страница 1", [])
        self.testPage = self.rootwiki["Страница 1"]

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
