# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir


class TemplateTest (unittest.TestCase):
    """Тесты плагина Template"""
    def setUp (self):
        self.__createWiki()

        dirlist = ["../plugins/template"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        removeDir (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
