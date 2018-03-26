#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.sessions.test_loading import SessionsLoadingTest
from test.plugins.sessions.test_sessions import SessionsTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
