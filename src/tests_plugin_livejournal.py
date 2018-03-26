#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.livejournal.test_loading import LivejournalLoadingTest
from test.plugins.livejournal.test_livejournal import LivejournalPluginTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
