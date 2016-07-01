# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader

from test.actions.test_editor_polyactions import BaseEditorPolyactionsTest


class MarkdownPolyactionsTest (BaseEditorPolyactionsTest):
    """Test polyactions for Markdown pages"""
    def setUp(self):
        dirlist = [u"../plugins/markdown"]
        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)
        super(MarkdownPolyactionsTest, self).setUp()

    def tearDown(self):
        self.loader.clear()
        super(MarkdownPolyactionsTest, self).tearDown()

    def _createPage(self):
        from markdown.markdownpage import MarkdownPageFactory
        return MarkdownPageFactory().create(self.wikiroot,
                                            u"Markdown-страница",
                                            [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor
