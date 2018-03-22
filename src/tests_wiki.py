#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""
from gettext import NullTranslations

import wx


if __name__ == '__main__':
    NullTranslations().install()

    from outwiker.core.application import Application
    Application.init("../test/testconfig.ini")

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.GUIEventLoop()
    wx.GUIEventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.wikipage.parsertests.test_tokennames import TokenNamesTest
    from test.wikipage.parsertests.test_parserfont import ParserFontTest
    from test.wikipage.parsertests.test_parserformat import ParserFormatTest
    from test.wikipage.parsertests.test_parsermisc import ParserMiscTest
    from test.wikipage.parsertests.test_parserlink import ParserLinkTest
    from test.wikipage.parsertests.test_parserattach import ParserAttachTest
    from test.wikipage.parsertests.test_parserimages import ParserImagesTest
    from test.wikipage.parsertests.test_parserheading import ParserHeadingTest
    from test.wikipage.parsertests.test_parserthumb import ParserThumbTest
    from test.wikipage.parsertests.test_parseralign import ParserAlignTest
    from test.wikipage.parsertests.test_parserlist import ParserListTest
    from test.wikipage.parsertests.test_parsertable import ParserTableTest
    from test.wikipage.parsertests.test_parseradhoc import ParserAdHocTest
    from test.wikipage.parsertests.test_parserurl import ParserUrlTest
    from test.wikipage.parsertests.test_parserlinebreak import ParserLineBreakTest
    from test.wikipage.parsertests.test_parserquote import ParserQuoteTest

    from test.wikipage.parsertests.test_wikicommands import WikiCommandsTest
    from test.wikipage.parsertests.test_wikicommandinclude import WikiIncludeCommandTest
    from test.wikipage.parsertests.test_wikicommandchildlist import WikiChildListCommandTest
    from test.wikipage.parsertests.test_wikicommandattachlist import WikiAttachListCommandTest
    from test.wikipage.parsertests.test_wikicommanddates import WikiCommandDatesTest
    from test.wikipage.parsertests.test_wikicommandtable import WikiCommandTableTest

    from test.wikipage.test_wikihtmlcache import WikiHtmlCacheTest
    from test.wikipage.test_wikihtmlgenerator import WikiHtmlGeneratorTest
    from test.wikipage.test_wikihash import WikiHashTest
    from test.wikipage.test_wikilinkcreator import WikiLinkCreatorTest
    from test.wikipage.test_wikiutils import WikiUtilsTest

    unittest.main()
