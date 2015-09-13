#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

import os
from outwiker.core.defines import WX_VERSION

import wxversion

try:
    wxversion.select(WX_VERSION)
except wxversion.VersionError:
    if os.name == "nt":
        pass
    else:
        raise

import wx


if __name__ == '__main__':
    from outwiker.core.application import Application
    Application.init ("../test/testconfig.ini")

    app = wx.PySimpleApp(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)

    import unittest

    from test.wikipage.parsertests.tokennames import TokenNamesTest
    from test.wikipage.parsertests.parserfont import ParserFontTest
    from test.wikipage.parsertests.parserformat import ParserFormatTest
    from test.wikipage.parsertests.parsermisc import ParserMiscTest
    from test.wikipage.parsertests.parserlink import ParserLinkTest
    from test.wikipage.parsertests.parserattach import ParserAttachTest
    from test.wikipage.parsertests.parserimages import ParserImagesTest
    from test.wikipage.parsertests.parserheading import ParserHeadingTest
    from test.wikipage.parsertests.parserthumb import ParserThumbTest
    from test.wikipage.parsertests.parseralign import ParserAlignTest
    from test.wikipage.parsertests.parserlist import ParserListTest
    from test.wikipage.parsertests.parsertable import ParserTableTest
    from test.wikipage.parsertests.parseradhoc import ParserAdHocTest
    from test.wikipage.parsertests.parserurl import ParserUrlTest
    from test.wikipage.parsertests.parsertex import ParserTexTest
    from test.wikipage.parsertests.parserlinebreak import ParserLineBreakTest
    from test.wikipage.parsertests.parserquote import ParserQuoteTest

    from test.wikipage.parsertests.wikicommands import WikiCommandsTest
    from test.wikipage.parsertests.wikicommandinclude import WikiIncludeCommandTest
    from test.wikipage.parsertests.wikicommandchildlist import WikiChildListCommandTest
    from test.wikipage.parsertests.wikicommandattachlist import WikiAttachListCommandTest
    from test.wikipage.parsertests.wikicommanddates import WikiCommandDatesTest
    from test.wikipage.parsertests.wikicommandtable import WikiCommandTableTest

    from test.wikipage.wikihtmlcache import WikiHtmlCacheTest
    from test.wikipage.wikihtmlgenerator import WikiHtmlGeneratorTest
    from test.wikipage.wikihash import WikiHashTest
    from test.wikipage.wikilinkcreator import WikiLinkCreatorTest
    from test.wikipage.wikiutils import WikiUtilsTest

    unittest.main()
