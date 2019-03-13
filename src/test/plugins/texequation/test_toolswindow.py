# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class TexEquationToolsWindowTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])

        self.filesPath = "../test/samplefiles/"
        dirlist = ["../plugins/texequation"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_equationExtract_empty(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = ''
        position = 0

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, '')
        self.assertFalse(blockMode)

    def test_equationExtract_miss_01(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$a=b$}'
        position = 0

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, '')
        self.assertFalse(blockMode)

    def test_equationExtract_inline_01(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$a=b$}'
        position = 2

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, 'a=b')
        self.assertFalse(blockMode)

    def test_equationExtract_block_01(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$$a=b$$}'
        position = 3

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, 'a=b')
        self.assertTrue(blockMode)

    def test_equationExtract_block_02(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$$a=b$$}'
        position = 6

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, 'a=b')
        self.assertTrue(blockMode)

    def test_equationExtract_block_03(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$$a=b$$}'
        position = 7

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, 'a=b')
        self.assertTrue(blockMode)

    def test_equationExtract_block_miss_02(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$$a=b$$}'
        position = 9

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, '')
        self.assertFalse(blockMode)

    def test_equationExtract_inline_02(self):
        from texequation.toolswindowcontroller import ToolsWindowController

        text = '{$...$} {$a=b$} {$...$}'
        position = 10

        equation, blockMode = ToolsWindowController.extractEquation(text,
                                                                    position)
        self.assertEqual(equation, 'a=b')
        self.assertFalse(blockMode)
