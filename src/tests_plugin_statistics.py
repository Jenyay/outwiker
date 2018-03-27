#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.statistics.test_loading import StatisticsLoadingTest
from test.plugins.statistics.test_pagestatistics import PageStatisticsTest
from test.plugins.statistics.test_treestatistics import TreeStatisticsTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
