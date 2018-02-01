#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-tests
"""

if __name__ == '__main__':
    from outwiker.core.application import Application
    Application.init("../test/testconfig.ini")

    import unittest

    from test.test_treeloading import (WikiPagesTest,
                                       SubWikiTest,
                                       TextPageAttachmentTest)
    from test.test_treeloading_readonly import ReadonlyLoadTest, ReadonlyChangeTest
    from test.test_treecreation import TextPageCreationTest
    from test.test_treemanualedit import ManualEditTest
    from test.test_bookmarks import BookmarksTest
    from test.test_treeconfigpages import ConfigPagesTest
    from test.test_invalidwiki import InvalidWikiTest
    from test.test_factory import FactorySelectorTest
    from test.test_titletester import PageTitleTesterTest
    from test.test_tags import TagsListTest
    from test.test_pagedatetime import PageDateTimeTest

    from test.test_pagemove import MoveTest
    from test.test_attachment import AttachmentTest
    from test.test_pagerename import RenameTest
    from test.test_pageremove import RemovePagesTest
    from test.test_pageorder import PageOrderTest
    from test.test_pagealias import PageAliasTest

    from test.test_thumbmakerwx import ThumbmakerWxTest
    from test.test_thumbmakerpil import ThumbmakerPilTest
    from test.test_pagethumbmaker import PageThumbmakerTest
    from test.test_thumbnails import ThumbnailsTest
    from test.test_htmlimproverbr import BrHtmlImproverTest
    from test.test_htmlimproverfactory import HtmlImproverFactoryTest
    from test.test_htmltemplate import HtmlTemplateTest
    from test.htmlpage.test_htmlpages import HtmlPagesTest

    from test.test_event import EventTest, EventsTest
    from test.test_config import (ConfigTest,
                                  ConfigOptionsTest,
                                  TrayConfigTest,
                                  EditorConfigTest)

    from test.test_recent import RecentWikiTest
    from test.test_search import SearcherTest, SearchPageTest
    from test.test_localsearch import LocalSearchTest
    from test.test_i18n import I18nTest
    from test.test_version import VersionTest, StatusTest
    from test.test_treesort import TreeSortTest
    from test.test_emptycontent import EmptyContentTest
    from test.test_hotkey import HotKeyTest
    from test.test_hotkeyparser import HotKeyParserTest
    from test.test_hotkeyconfig import HotKeyConfigTest
    from test.test_history import HistoryTest
    from test.test_commandline import CommandLineTest
    from test.test_pageuiddepot import PageUidDepotTest
    from test.test_pluginsloader import PluginsLoaderTest
    from test.test_iconscollection import IconsCollectionTest
    from test.test_iconmaker import IconMakerTest
    from test.test_iconcontroller import IconControllerTest
    from test.test_recenticonslist import RecentIconsListTest
    from test.test_dicttostr import DictToStrTest

    from test.spellchecker.test_dictsfinder import DictsFinderTest
    from test.spellchecker.test_spellchecker import SpellCheckerTest

    from test.styles.test_styles import StylesTest
    from test.styles.test_styleslist import StylesListTest

    from test.test_xmlversionparser import XmlVersionParserTest
    from test.test_packageversion import (PackageCheckVersionTest,
                                          PackageCheckVersionAnyTest)

    unittest.main()
