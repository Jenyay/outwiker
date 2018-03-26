# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.htmlimproverfactory import HtmlImproverFactory


class HtmlFormatterTest (unittest.TestCase):
    """Тесты плагина HtmlFormatter"""

    def setUp(self):
        dirlist = ["../plugins/htmlformatter"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testFactory(self):
        from htmlformatter.paragraphimprover import ParagraphHtmlImprover
        factory = HtmlImproverFactory(Application)

        self.assertEqual(type(factory['pimprover']), ParagraphHtmlImprover)
