# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class TexEquationTest(unittest.TestCase):
    def setUp(self):
        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/texequation"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.testPage = self.wikiroot[u"Страница 1"]
        self.parser = ParserFactory().make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir(self.path)

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def test_inline_01(self):
        eqn = u"y = f(x)"
        text = u"{{$ {eqn} $}}".format(eqn=eqn)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), 'katex')

        result_lines = [
            u'<span class="texequation-inline" id="texequation-inline-0"></span>',
        ]

        footer_lines = [
            u'var element_0 = document.getElementById("texequation-inline-0");',
            u'katex.render("{}",'.format(eqn),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_inline_02(self):
        eqn1 = u"y = f1(x)"
        eqn2 = u"y = f2(x)"
        text = u"{{$ {eqn1} $}} {{$ {eqn2} $}}".format(eqn1=eqn1, eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), 'katex')

        result_lines = [
            u'<span class="texequation-inline" id="texequation-inline-0"></span>',
            u'<span class="texequation-inline" id="texequation-inline-1"></span>',
        ]

        footer_lines = [
            u'var element_0 = document.getElementById("texequation-inline-0");',
            u'var element_1 = document.getElementById("texequation-inline-1");',
            u'katex.render("{}",'.format(eqn1),
            u'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_inline_03(self):
        eqn = u"y = f(x)"
        text = u"Это строчная формула. {{$ {eqn} $}} Она не разрывает строку.".format(eqn=eqn)

        result = self.parser.toHtml(text)

        self.assertIn(u'Это строчная формула. <span class="texequation-inline" id="texequation-inline-0"></span> Она не разрывает строку.',
                      result)

    def test_block_01(self):
        eqn = u"y = f(x)"
        text = u"{{$$ {eqn} $$}}".format(eqn=eqn)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), 'katex')

        result_lines = [
            u'<span class="texequation-block" id="texequation-block-0"></span>',
        ]

        footer_lines = [
            u'var element_0 = document.getElementById("texequation-block-0");',
            u'katex.render("{}",'.format(eqn),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_block_02(self):
        eqn1 = u"y = f1(x)"
        eqn2 = u"y = f2(x)"

        text = u"{{$$ {eqn1} $$}} {{$$ {eqn2} $$}}".format(eqn1=eqn1,
                                                           eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), 'katex')

        result_lines = [
            u'<span class="texequation-block" id="texequation-block-0"></span>',
            u'<span class="texequation-block" id="texequation-block-1"></span>',
        ]

        footer_lines = [
            u'var element_0 = document.getElementById("texequation-block-0");',
            u'var element_1 = document.getElementById("texequation-block-1");',
            u'katex.render("{}",'.format(eqn1),
            u'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)

    def test_mixed_01(self):
        eqn1 = u"y = f1(x)"
        eqn2 = u"y = f2(x)"

        text = u"{{$$ {eqn1} $$}} {{$ {eqn2} $}}".format(eqn1=eqn1,
                                                         eqn2=eqn2)

        path = os.path.join(Thumbnails.getRelativeThumbDir(), 'katex')

        result_lines = [
            u'<span class="texequation-block" id="texequation-block-0"></span>',
            u'<span class="texequation-inline" id="texequation-inline-0"></span>',
        ]

        footer_lines = [
            u'var element_0 = document.getElementById("texequation-block-0");',
            u'var element_0 = document.getElementById("texequation-inline-0");',
            u'katex.render("{}",'.format(eqn1),
            u'katex.render("{}",'.format(eqn2),
        ]

        result = self.parser.toHtml(text)

        for line in result_lines:
            self.assertIn(line, result)

        for line in footer_lines:
            self.assertIn(line, self.parser.footer)

        full_path = os.path.join(self.parser.page.path, path)
        self.assertTrue(os.path.exists(full_path), full_path)
