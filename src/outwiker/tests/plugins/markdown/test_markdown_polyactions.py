# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader

from outwiker.tests.actions.test_editor_polyactions import BaseEditorPolyactionsFixture


class MarkdownPolyactionsTest(BaseEditorPolyactionsFixture, unittest.TestCase):
    """Test polyactions for Markdown pages"""

    def setUp(self):
        super().setUp()

    def _postInitApplication(self):
        dirlist = ["plugins/markdown"]
        self.loader = PluginsLoader(self.application)
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
        return self.application.mainWindow.pagePanel.pageView.codeEditor
