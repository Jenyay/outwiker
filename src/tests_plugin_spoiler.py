#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import NullTranslations
import unittest

from test.plugins.spoiler.test_loading import SpoilerLoadingTest
from test.plugins.spoiler.test_spoiler import SpoilerPluginTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
