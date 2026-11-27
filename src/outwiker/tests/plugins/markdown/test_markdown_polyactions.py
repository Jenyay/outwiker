"""Tests for editor polyactions on Markdown pages."""

from collections.abc import Iterator

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.gui.texteditor import TextEditor
from outwiker.tests.actions.test_editor_polyactions import EditorPolyactionsTests


@pytest.fixture
def editor(
    application: Application,
    wikiroot: WikiDocument,
    main_window: MainWindow,
    markdown_loader: PluginsLoader,
) -> Iterator[TextEditor]:
    from markdown.markdownpage import MarkdownPageFactory

    page = MarkdownPageFactory().create(wikiroot, "Markdown-страница", [])
    application.wikiroot = wikiroot
    application.selectedPage = page

    yield main_window.pagePanel.pageView.codeEditor

    application.selectedPage = None
    application.wikiroot = None


class TestMarkdownPolyactions(EditorPolyactionsTests):
    """Test polyactions for Markdown pages"""
