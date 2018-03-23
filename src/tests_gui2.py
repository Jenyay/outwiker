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
    from test.guitests.test_pagepanel import PagePanelTest
    from test.guitests.test_tagspanel import TagsPanelTest
    from test.guitests.test_tabs import TabsTest
    from test.guitests.test_linkdialogcontrollertest import LinkDialogControllerTest
    from test.guitests.test_thumbdialogcontrollertest import ThumbDialogControllerTest

    unittest.main()
