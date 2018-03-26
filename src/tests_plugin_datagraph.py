#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations

import unittest

from test.plugins.datagraph.test_loading import DataGraphLoadingTest
from test.plugins.datagraph.test_paramsparsing import ParamsParsingTest
from test.plugins.datagraph.test_graphbuilder import GraphBuilderTest
from test.plugins.datagraph.test_datasources import StringSourceTest, FileSourceTest
from test.plugins.datagraph.test_command_plot_highcharts import CommandPlotHighchartsTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
