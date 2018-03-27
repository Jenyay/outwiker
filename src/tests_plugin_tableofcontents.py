#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.tableofcontents.test_toc_parser import TOC_ParserTest
from test.plugins.tableofcontents.test_toc_generator import TOC_GeneratorTest
from test.plugins.tableofcontents.test_toc_wikimaker import TOC_WikiMakerTest
from test.plugins.tableofcontents.test_loading import TOCLoadingTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
