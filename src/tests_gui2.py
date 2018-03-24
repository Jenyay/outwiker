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
    from test.guitests.test_textpageview import TextPageViewTest
    from test.guitests.test_actioncontroller import ActionControllerTest
    from test.guitests.test_mainpanes import MainPanesTest
    from test.guitests.test_fullscreen import FullScreenTest
    from test.guitests.test_texteditor import TextEditorTest
    from test.guitests.test_fileicons import FileIconsTestUnix, FileIconsTestWindows
    from test.guitests.test_stcstyleparser import StcStyleParserTest
    from test.guitests.test_childlistdialog import ChildListDialogTest
    from test.guitests.test_attachlistdialog import AttachListDialogTest
    from test.guitests.test_includedialog import IncludeDialogTest
    from test.guitests.test_removepage import RemovePageGuiTest
    from test.guitests.test_renamepage import RenamePageGuiTest

    unittest.main()
