#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.organizer.test_organizer import OrganizerTest
from test.plugins.organizer.test_loading import OrganizerLoadingTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
