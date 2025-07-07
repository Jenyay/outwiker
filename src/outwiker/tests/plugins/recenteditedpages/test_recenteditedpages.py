# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.pages.wiki.wikipage import createWikiPage
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class PluginNameTest(BaseOutWikerGUIMixin, unittest.TestCase):
    """Tests for the RecentEditedPages plug-in"""

    def setUp(self):
        self.initApplication()
        self.__createWiki()

        dirlist = ["plugins/recenteditedpages"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        removeDir(self.path)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = self.path = mkdtemp(prefix='Абырвалг абыр RecentEditedPages')
        removeDir(self.path)

        self.rootwiki = WikiDocument.create(self.path)

        createWikiPage(self.rootwiki, "Страница 1", [])
        self.testPage = self.rootwiki["Страница 1"]

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
