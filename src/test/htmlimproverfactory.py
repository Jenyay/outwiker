# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import BrHtmlImprover, ParagraphHtmlImprover
from outwiker.core.htmlimproverfactory import HtmlImproverFactory


class HtmlImproverFactoryTest (unittest.TestCase):
    def test_type_br (self):
        improver = HtmlImproverFactory().get ('brimprover')
        self.assertEqual (type (improver), BrHtmlImprover)


    def test_type_p (self):
        improver = HtmlImproverFactory().get ('pimprover')
        self.assertEqual (type (improver), ParagraphHtmlImprover)


    def test_type_default (self):
        improver = HtmlImproverFactory().get ('')
        self.assertEqual (type (improver), BrHtmlImprover)


    def test_type_None (self):
        improver = HtmlImproverFactory().get (None)
        self.assertEqual (type (improver), BrHtmlImprover)


    def test_dict (self):
        improvers = HtmlImproverFactory().getDict()

        self.assertIn ('brimprover', improvers)
        self.assertIn ('pimprover', improvers)

        self.assertEqual (type (improvers['brimprover'].obj), BrHtmlImprover)
        self.assertEqual (type (improvers['pimprover'].obj), ParagraphHtmlImprover)
