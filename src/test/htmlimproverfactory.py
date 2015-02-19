# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import BrHtmlImprover, ParagraphHtmlImprover
from outwiker.core.htmlimproverfactory import HtmlImproverFactory


class HtmlImproverFactoryTest (unittest.TestCase):
    def test_type_br (self):
        improver = HtmlImproverFactory()['brimprover']
        self.assertEqual (type (improver), BrHtmlImprover)


    def test_type_p (self):
        improver = HtmlImproverFactory()['pimprover']
        self.assertEqual (type (improver), ParagraphHtmlImprover)


    def test_type_default (self):
        improver = HtmlImproverFactory()['']
        self.assertEqual (type (improver), BrHtmlImprover)


    def test_type_None (self):
        improver = HtmlImproverFactory()[None]
        self.assertEqual (type (improver), BrHtmlImprover)
