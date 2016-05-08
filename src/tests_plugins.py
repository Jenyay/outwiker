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

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)

    import unittest

    from test.plugins.template import TemplateTest
    from test.plugins.testplugin.testpage import TestPageTest
    from test.plugins.testplugin.testwikicommand import PluginWikiCommandTest

    from test.plugins.style.loading import StyleLoadingTest
    from test.plugins.style.style import StylePluginTest

    from test.plugins.export2html.export2html_test import Export2HtmlTest
    from test.plugins.export2html.loading import Export2HtmlLoadingTest

    from test.plugins.spoiler.loading import SpoilerLoadingTest
    from test.plugins.spoiler.spoiler import SpoilerPluginTest

    from test.plugins.livejournal.loading import LivejournalLoadingTest
    from test.plugins.livejournal.livejournal_test import LivejournalPluginTest

    from test.plugins.lightbox.loading import LightboxLoadingTest
    from test.plugins.lightbox.lightbox import LightboxPluginTest

    from test.plugins.thumbgallery.loading import ThumbGalleryLoadingTest
    from test.plugins.thumbgallery.thumblist import ThumbListPluginTest

    from test.plugins.statistics.loading import StatisticsLoadingTest
    from test.plugins.statistics.pagestatistics import PageStatisticsTest
    from test.plugins.statistics.treestatistics import TreeStatisticsTest

    from test.plugins.updatenotifier.loading import UpdateNotifierLoadingTest
    from test.plugins.updatenotifier.updatenotifier_test import UpdateNotifierTest

    from test.plugins.counter.counter_test import CounterTest
    from test.plugins.counter.counterdialog import CounterDialogTest
    from test.plugins.counter.loading import CounterLoadingTest

    from test.plugins.htmlheads.loading import HtmlHeadsLoadingTest
    from test.plugins.htmlheads.htmlheads import HtmlHeadsTest

    from test.plugins.changepageuid.changepageuid_test import ChangePageUidTest
    from test.plugins.changepageuid.loading import ChangePageUIDLoadingTest

    from test.plugins.sessions.loading import SessionsLoadingTest
    from test.plugins.sessions.sessions_test import SessionsTest

    from test.plugins.diagrammer.diagrammer_test import DiagrammerTest
    from test.plugins.diagrammer.insertnode import InsertNodeTest
    from test.plugins.diagrammer.insertdiagram import InsertDiagramTest
    from test.plugins.diagrammer.insertedge import InsertEdgeTest
    from test.plugins.diagrammer.insertgroup import InsertGroupTest
    from test.plugins.diagrammer.loading import DiagrammerLoadingTest

    from test.plugins.tableofcontents.toc_parser import TOC_ParserTest
    from test.plugins.tableofcontents.toc_generator import TOC_GeneratorTest
    from test.plugins.tableofcontents.toc_wikimaker import TOC_WikiMakerTest
    from test.plugins.tableofcontents.loading import TOCLoadingTest

    from test.plugins.source.source_test import SourcePluginTest
    from test.plugins.source.sourceencoding import SourceEncodingPluginTest
    from test.plugins.source.sourcefile import SourceFilePluginTest
    from test.plugins.source.sourcegui import SourceGuiPluginTest
    from test.plugins.source.sourceattachment import SourceAttachmentPluginTest
    from test.plugins.source.sourcestyle import SourceStyleTest
    from test.plugins.source.loading import SourceLoadingTest

    from test.plugins.datagraph.loading import DataGraphLoadingTest
    from test.plugins.datagraph.paramsparsing import ParamsParsingTest
    from test.plugins.datagraph.graphbuilder import GraphBuilderTest
    from test.plugins.datagraph.datasources import StringSourceTest, FileSourceTest
    from test.plugins.datagraph.command_plot_highcharts import CommandPlotHighchartsTest

    from test.plugins.htmlformatter.htmlformatter_test import HtmlFormatterTest
    from test.plugins.htmlformatter.htmlimproverp import ParagraphHtmlImproverTest

    from test.plugins.externaltools.loading import ExternalToolsLoadingTest
    from test.plugins.externaltools.commandexec import CommandExecTest
    from test.plugins.externaltools.commandexecparser import CommandExecParserTest
    from test.plugins.externaltools.commandexeccontroller import CommandExecControllerTest
    from test.plugins.externaltools.execdialog import ExecDialogTest

    from test.plugins.texequation.texequation_test import TexEquationTest

    from test.plugins.webpage.test_webpage import WebPageTest
    from test.plugins.webpage.test_downloader import DownloaderTest
    from test.plugins.webpage.test_real import RealTest
    from test.plugins.webpage.test_loading import WebPageLoadingTest

    from test.plugins.organizer.test_organizer import OrganizerTest
    from test.plugins.organizer.test_loading import OrganizerLoadingTest

    unittest.main()
