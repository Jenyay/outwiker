#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.markdown.test_markdown import MarkdownTest
from test.plugins.markdown.test_loading import MarkdownLoadingTest
from test.plugins.markdown.test_linkcreator import LinkCreatorTest
from test.plugins.markdown.test_markdown_polyactions import MarkdownPolyactionsTest
from test.plugins.markdown.test_imagedialog import MarkdownImageDialogTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
