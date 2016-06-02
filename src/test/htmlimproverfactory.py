# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import BrHtmlImprover
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.application import Application
from outwiker.core.htmlimprover import HtmlImprover


class TestImprover1(HtmlImprover):
    def _appendLineBreaks(self, text):
        pass


class TestImprover2(HtmlImprover):
    def _appendLineBreaks(self, text):
        pass


class HtmlImproverFactoryTest(unittest.TestCase):
    def setUp(self):
        Application.onPrepareHtmlImprovers.clear()


    def tearDown(self):
        Application.onPrepareHtmlImprovers.clear()


    def test_type(self):
        factory = HtmlImproverFactory(Application)
        self.assertEqual(type(factory['brimprover']), BrHtmlImprover)
        self.assertEqual(type(factory['pimprover']), BrHtmlImprover)
        self.assertEqual(type(factory['test1']), BrHtmlImprover)
        self.assertEqual(type(factory['test2']), BrHtmlImprover)


    def test_type_default(self):
        improver = HtmlImproverFactory(Application)['']
        self.assertEqual(type(improver), BrHtmlImprover)


    def test_type_None(self):
        improver = HtmlImproverFactory(Application)[None]
        self.assertEqual(type(improver), BrHtmlImprover)


    def test_add_improvers(self):
        Application.onPrepareHtmlImprovers += self._addTestImprovers
        factory = HtmlImproverFactory(Application)

        self.assertEqual(type(factory[u'test1']), TestImprover1)
        self.assertEqual(type(factory[u'test2']), TestImprover2)


    def _addTestImprovers(self, factory):
        factory.add(u'test1', TestImprover1(), u'')
        factory.add(u'test2', TestImprover2(), u'')
