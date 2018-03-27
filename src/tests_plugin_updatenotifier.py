#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.updatenotifier.test_loading import UpdateNotifierLoadingTest
from test.plugins.updatenotifier.test_versionlist import VersionListTest
from test.plugins.updatenotifier.test_updatecontroller import UpdateControllerTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
