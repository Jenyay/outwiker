# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.basetestcases import BaseOutWikerGUITest


class TexEquationTest(BaseOutWikerGUITest):
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
        self.parser = ParserFactory().make(self.testPage, self.application.config)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def test_inline_01(self):
        from texequation.defines import KATEX_DIR_NAME
        eqn = "y = f(x)"
        text = "{{$ {eqn} $}}".format(eqn=eqn)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), KATEX_DIR_NAME)

        result_lines = [
            '<span class="texequation-inline" id="texequation-inline-0"></span>',
        ]

        footer_lines = [
            'var element_0 = document.getElementById("texequation-inline-0");',
            'katex.render("{}",'.format(eqn),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_inline_02(self):
        from texequation.defines import KATEX_DIR_NAME
        eqn1 = "y = f1(x)"
        eqn2 = "y = f2(x)"
        text = "{{$ {eqn1} $}} {{$ {eqn2} $}}".format(eqn1=eqn1, eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), KATEX_DIR_NAME)

        result_lines = [
            '<span class="texequation-inline" id="texequation-inline-0"></span>',
            '<span class="texequation-inline" id="texequation-inline-1"></span>',
        ]

        footer_lines = [
            'var element_0 = document.getElementById("texequation-inline-0");',
            'var element_1 = document.getElementById("texequation-inline-1");',
            'katex.render("{}",'.format(eqn1),
            'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_inline_03(self):
        eqn = "y = f(x)"
        text = "Это строчная формула. {{$ {eqn} $}} Она не разрывает строку.".format(eqn=eqn)

        result = self.parser.toHtml(text)

        self.assertIn('Это строчная формула. <span class="texequation-inline" id="texequation-inline-0"></span> Она не разрывает строку.',
                      result)

    def test_block_01(self):
        from texequation.defines import KATEX_DIR_NAME
        eqn = "y = f(x)"
        text = "{{$$ {eqn} $$}}".format(eqn=eqn)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), KATEX_DIR_NAME)

        result_lines = [
            '<span class="texequation-block" id="texequation-block-0"></span>',
        ]

        footer_lines = [
            'var element_0 = document.getElementById("texequation-block-0");',
            'katex.render("{}",'.format(eqn),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_block_02(self):
        from texequation.defines import KATEX_DIR_NAME
        eqn1 = "y = f1(x)"
        eqn2 = "y = f2(x)"

        text = "{{$$ {eqn1} $$}} {{$$ {eqn2} $$}}".format(eqn1=eqn1,
                                                          eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), KATEX_DIR_NAME)

        result_lines = [
            '<span class="texequation-block" id="texequation-block-0"></span>',
            '<span class="texequation-block" id="texequation-block-1"></span>',
        ]

        footer_lines = [
            'var element_0 = document.getElementById("texequation-block-0");',
            'var element_1 = document.getElementById("texequation-block-1");',
            'katex.render("{}",'.format(eqn1),
            'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_mixed_01(self):
        from texequation.defines import KATEX_DIR_NAME
        eqn1 = "y = f1(x)"
        eqn2 = "y = f2(x)"

        text = "{{$$ {eqn1} $$}} {{$ {eqn2} $}}".format(eqn1=eqn1,
                                                        eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), KATEX_DIR_NAME)

        result_lines = [
            '<span class="texequation-block" id="texequation-block-0"></span>',
            '<span class="texequation-inline" id="texequation-inline-0"></span>',
        ]

        footer_lines = [
            'var element_0 = document.getElementById("texequation-block-0");',
            'var element_0 = document.getElementById("texequation-inline-0");',
            'katex.render("{}",'.format(eqn1),
            'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)
