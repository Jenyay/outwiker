# -*- coding: utf-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader

from test.actions.test_editor_polyactions import BaseEditorPolyactionsTest


class MarkdownPolyactionsTest(BaseEditorPolyactionsTest):
    """Test polyactions for Markdown pages"""
    def setUp(self):
        super().setUp()

    def _postInitApplication(self):
        dirlist = ["../plugins/markdown"]
        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        super().tearDown()

    def _createPage(self):
        from markdown.markdownpage import MarkdownPageFactory
        return MarkdownPageFactory().create(self.wikiroot,
                                            "Markdown-страница",
                                            [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor
