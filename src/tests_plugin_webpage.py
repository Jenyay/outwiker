#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import NullTranslations
import unittest

from test.plugins.webpage.test_loading import WebPageLoadingTest
from test.plugins.webpage.test_downloader import DownloaderTest
from test.plugins.webpage.test_webpage import WebPageTest
from test.plugins.webpage.test_real import RealTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
