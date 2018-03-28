# -*- coding: utf-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from test.basetestcases import BaseOutWikerTest


class HtmlFormatterTest (BaseOutWikerTest):
    """Тесты плагина HtmlFormatter"""

    def setUp(self):
        self.initApplication()
        dirlist = ["../plugins/htmlformatter"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testFactory(self):
        from htmlformatter.paragraphimprover import ParagraphHtmlImprover
        factory = HtmlImproverFactory(self.application)

        self.assertEqual(type(factory['pimprover']), ParagraphHtmlImprover)
