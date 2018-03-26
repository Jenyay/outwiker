#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.export2html.test_export2html import Export2HtmlTest
from test.plugins.export2html.test_loading import Export2HtmlLoadingTest

if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
