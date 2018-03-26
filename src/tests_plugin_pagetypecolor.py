#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.pagetypecolor.test_loading import PageTypeColor_LoadingTest
from test.plugins.pagetypecolor.test_colorslist import PageTypeColor_ColorsListTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
