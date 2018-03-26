#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.htmlheads.test_loading import HtmlHeadsLoadingTest
from test.plugins.htmlheads.test_htmlheads import HtmlHeadsTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
