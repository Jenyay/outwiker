#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI unit tests
"""

import unittest
from gettext import NullTranslations


if __name__ == '__main__':
    NullTranslations().install()

    from test.guitests.test_mainwnd import MainWndTest
    from test.guitests.test_bookmarks import BookmarksGuiTest
    from test.guitests.test_attach import AttachPanelTest
    from test.guitests.test_tree import TreeTest

    unittest.main()
