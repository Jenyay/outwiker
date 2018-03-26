#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.lightbox.test_loading import LightboxLoadingTest
from test.plugins.lightbox.test_lightbox import LightboxPluginTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
