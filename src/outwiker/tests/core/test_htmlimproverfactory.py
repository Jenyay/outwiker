# -*- coding: utf-8 -*-

import unittest

from outwiker.core.htmlimprover import BrHtmlImprover
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class ExampleImprover1(HtmlImprover):
    def _appendLineBreaks(self, text):
        pass


class ExampleImprover2(HtmlImprover):
    def _appendLineBreaks(self, text):
        pass


class HtmlImproverFactoryTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def test_type(self):
        factory = HtmlImproverFactory(self.application)
        self.assertEqual(type(factory['brimprover']), BrHtmlImprover)
        self.assertEqual(type(factory['pimprover']), BrHtmlImprover)
        self.assertEqual(type(factory['test1']), BrHtmlImprover)
        self.assertEqual(type(factory['test2']), BrHtmlImprover)

    def test_type_default(self):
        improver = HtmlImproverFactory(self.application)['']
        self.assertEqual(type(improver), BrHtmlImprover)

    def test_type_None(self):
        improver = HtmlImproverFactory(self.application)[None]
        self.assertEqual(type(improver), BrHtmlImprover)

    def test_add_improvers(self):
        self.application.onPrepareHtmlImprovers += self._addTestImprovers
        factory = HtmlImproverFactory(self.application)

        self.assertEqual(type(factory['test1']), ExampleImprover1)
        self.assertEqual(type(factory['test2']), ExampleImprover2)

    def _addTestImprovers(self, factory):
        factory.add('test1', ExampleImprover1(), '')
        factory.add('test2', ExampleImprover2(), '')
