# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class TemplateTest(BaseOutWikerGUIMixin, unittest.TestCase):
    """Тесты плагина Template"""

    def setUp(self):
        self.initApplication()
        self.__createWiki()

        dirlist = ["plugins/template"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        removeDir(self.path)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)
