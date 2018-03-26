#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.htmlformatter.test_htmlformatter import HtmlFormatterTest
from test.plugins.htmlformatter.test_htmlimproverp import ParagraphHtmlImproverTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
