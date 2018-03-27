#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.thumbgallery.test_loading import ThumbGalleryLoadingTest
from test.plugins.thumbgallery.test_thumblist import ThumbListPluginTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
