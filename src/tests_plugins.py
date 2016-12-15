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
    Application.init("../test/testconfig.ini")

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.plugins.test_template import TemplateTest
    from test.plugins.testplugin.test_testpage import TestPageTest
    from test.plugins.testplugin.test_testwikicommand import PluginWikiCommandTest

    from test.plugins.style.test_loading import StyleLoadingTest
    from test.plugins.style.test_style import StylePluginTest

    from test.plugins.export2html.test_export2html import Export2HtmlTest
    from test.plugins.export2html.test_loading import Export2HtmlLoadingTest

    from test.plugins.spoiler.test_loading import SpoilerLoadingTest
    from test.plugins.spoiler.test_spoiler import SpoilerPluginTest

    from test.plugins.livejournal.test_loading import LivejournalLoadingTest
    from test.plugins.livejournal.test_livejournal import LivejournalPluginTest

    from test.plugins.lightbox.test_loading import LightboxLoadingTest
    from test.plugins.lightbox.test_lightbox import LightboxPluginTest

    from test.plugins.thumbgallery.test_loading import ThumbGalleryLoadingTest
    from test.plugins.thumbgallery.test_thumblist import ThumbListPluginTest

    from test.plugins.statistics.test_loading import StatisticsLoadingTest
    from test.plugins.statistics.test_pagestatistics import PageStatisticsTest
    from test.plugins.statistics.test_treestatistics import TreeStatisticsTest

    from test.plugins.updatenotifier.test_loading import UpdateNotifierLoadingTest
    from test.plugins.updatenotifier.test_updatenotifier import UpdateNotifierTest

    from test.plugins.counter.test_counter import CounterTest
    from test.plugins.counter.test_counterdialog import CounterDialogTest
    from test.plugins.counter.test_loading import CounterLoadingTest

    from test.plugins.htmlheads.test_loading import HtmlHeadsLoadingTest
    from test.plugins.htmlheads.test_htmlheads import HtmlHeadsTest

    from test.plugins.changepageuid.test_changepageuid import ChangePageUidTest
    from test.plugins.changepageuid.test_loading import ChangePageUIDLoadingTest

    from test.plugins.sessions.test_loading import SessionsLoadingTest
    from test.plugins.sessions.test_sessions import SessionsTest

    from test.plugins.diagrammer.test_diagrammer import DiagrammerTest
    from test.plugins.diagrammer.test_insertnode import InsertNodeTest
    from test.plugins.diagrammer.test_insertdiagram import InsertDiagramTest
    from test.plugins.diagrammer.test_insertedge import InsertEdgeTest
    from test.plugins.diagrammer.test_insertgroup import InsertGroupTest
    from test.plugins.diagrammer.test_loading import DiagrammerLoadingTest

    from test.plugins.tableofcontents.test_toc_parser import TOC_ParserTest
    from test.plugins.tableofcontents.test_toc_generator import TOC_GeneratorTest
    from test.plugins.tableofcontents.test_toc_wikimaker import TOC_WikiMakerTest
    from test.plugins.tableofcontents.test_loading import TOCLoadingTest

    from test.plugins.source.test_source import SourcePluginTest
    from test.plugins.source.test_sourceencoding import SourceEncodingPluginTest
    from test.plugins.source.test_sourcefile import SourceFilePluginTest
    from test.plugins.source.test_sourcegui import SourceGuiPluginTest
    from test.plugins.source.test_sourceattachment import SourceAttachmentPluginTest
    from test.plugins.source.test_sourcestyle import SourceStyleTest
    from test.plugins.source.test_loading import SourceLoadingTest

    from test.plugins.datagraph.test_loading import DataGraphLoadingTest
    from test.plugins.datagraph.test_paramsparsing import ParamsParsingTest
    from test.plugins.datagraph.test_graphbuilder import GraphBuilderTest
    from test.plugins.datagraph.test_datasources import StringSourceTest, FileSourceTest
    from test.plugins.datagraph.test_command_plot_highcharts import CommandPlotHighchartsTest

    from test.plugins.htmlformatter.test_htmlformatter import HtmlFormatterTest
    from test.plugins.htmlformatter.test_htmlimproverp import ParagraphHtmlImproverTest

    from test.plugins.externaltools.test_loading import ExternalToolsLoadingTest
    from test.plugins.externaltools.test_commandexec import CommandExecTest
    from test.plugins.externaltools.test_commandexecparser import CommandExecParserTest
    from test.plugins.externaltools.test_commandexeccontroller import CommandExecControllerTest
    from test.plugins.externaltools.test_execdialog import ExecDialogTest

    from test.plugins.texequation.test_texequation import TexEquationTest

    from test.plugins.webpage.test_webpage import WebPageTest
    from test.plugins.webpage.test_downloader import DownloaderTest
    from test.plugins.webpage.test_real import RealTest
    from test.plugins.webpage.test_loading import WebPageLoadingTest

    from test.plugins.organizer.test_organizer import OrganizerTest
    from test.plugins.organizer.test_loading import OrganizerLoadingTest

    from test.plugins.markdown.test_markdown import MarkdownTest
    from test.plugins.markdown.test_loading import MarkdownLoadingTest
    from test.plugins.markdown.test_linkcreator import LinkCreatorTest
    from test.plugins.markdown.test_markdown_polyactions import MarkdownPolyactionsTest
    from test.plugins.markdown.test_imagedialog import MarkdownImageDialogTest

    from test.plugins.snippets.test_loading import SnippetsLoadingTest
    from test.plugins.snippets.test_snippetsloader import SnippetsLoaderTest
    from test.plugins.snippets.test_snippetparser import SnippetParserTest
    from test.plugins.snippets.test_varpanel import VarPanelTest
    from test.plugins.snippets.test_vardialog import VarDialogTest
    from test.plugins.snippets.test_vardialogcontroller import VarDialogControllerTest
    from test.plugins.snippets.test_utils import SnippetsUtilsTest

    unittest.main()
