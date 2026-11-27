# -*- coding: utf-8 -*-

"""Tests for the wiki page view."""

from collections.abc import Iterator
from tempfile import mkdtemp

import pytest
import wx

from outwiker.api.core.tree import WikiDocument, createNotesTree, loadNotesTree
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.application import Application
from outwiker.core.defines import PAGE_MODE_HTML, PAGE_MODE_PREVIEW, PAGE_MODE_TEXT
from outwiker.gui.rootpagepanel import RootPagePanel
from outwiker.gui.texteditor import TextEditor
from outwiker.pages.wiki.listautocomplete import listComplete_wiki
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikipageview import WikiPageView
from outwiker.tests.utils import removeDir


@pytest.fixture(autouse=True)
def reset_state(
    application: Application, main_window: MainWindow
) -> Iterator[None]:
    """
    Reset the application state shared between the tests.

    The application is created once per module, so the event handlers and
    the page view settings changed by a test should be reset between tests.
    """
    application.onPostprocessing.clear()
    application.onPreprocessing.clear()
    WikiConfig(application.config).showHtmlCodeOptions.value = False

    yield

    application.onPostprocessing.clear()
    application.onPreprocessing.clear()


@pytest.fixture
def wiki(application: Application) -> Iterator[WikiDocument]:
    """Wiki with the pages used by the tests. It is not opened."""
    path = mkdtemp(prefix="outwiker_wikipageview")
    wikiroot = createNotesTree(path)

    WikiPageFactory().create(wikiroot, "Викистраница", [])
    WikiPageFactory().create(wikiroot, "Викистраница 2", [])

    yield wikiroot

    application.selectedPage = None
    application.wikiroot = None
    removeDir(path)


@pytest.fixture
def editor(application: Application, wiki: WikiDocument) -> TextEditor:
    """Code editor of the first wiki page opened in the application."""
    page = wiki["Викистраница"]
    application.wikiroot = wiki
    application.selectedPage = page

    return _get_code_editor(application)


def _get_page_view(application: Application):
    return application.mainWindow.pagePanel.pageView


def _get_code_editor(application: Application) -> TextEditor:
    return _get_page_view(application).codeEditor


def _on_postprocessing(page, params) -> None:
    params.result += " 111"


def _on_postprocessing2(page, params) -> None:
    params.result += " 222"


def _on_preprocessing(page, params) -> None:
    params.result += " 000"


def test_type(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    assert isinstance(_get_page_view(application), RootPagePanel)

    application.selectedPage = wiki["Викистраница"]
    assert isinstance(_get_page_view(application), WikiPageView)

    application.selectedPage = wiki["Викистраница 2"]
    assert isinstance(_get_page_view(application), WikiPageView)

    application.selectedPage = None
    assert isinstance(_get_page_view(application), RootPagePanel)


def test_switch(application: Application, wiki: WikiDocument):
    WikiConfig(application.config).showHtmlCodeOptions.value = True

    application.wikiroot = wiki
    assert isinstance(_get_page_view(application), RootPagePanel)

    application.selectedPage = wiki["Викистраница"]
    assert isinstance(_get_page_view(application), WikiPageView)

    application.selectedPage = wiki["Викистраница 2"]
    assert isinstance(_get_page_view(application), WikiPageView)

    application.selectedPage = None
    assert isinstance(_get_page_view(application), RootPagePanel)


def test_default_selected_page(application: Application, wiki: WikiDocument):
    """Default page mode is selected depending on the page content."""
    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]

    # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    wiki["Викистраница 2"].content = "Бла-бла-бла"
    application.selectedPage = wiki["Викистраница 2"]

    # Т.к. страница НЕ пустая, то по умолчанию выбирается
    # вкладка с просмотром
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW


def test_selected_page(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]

    # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    _get_page_view(application).SetPageMode(PAGE_MODE_PREVIEW)

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    _get_page_view(application).SetPageMode(PAGE_MODE_TEXT)

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    _get_page_view(application).SetPageMode(PAGE_MODE_HTML)

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_HTML


def test_result_html_page_1(application: Application, wiki: WikiDocument):
    """The HTML code tab is shown only if it is enabled in the settings."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = False

    application.wikiroot = wiki

    application.selectedPage = wiki["Викистраница"]
    assert _get_page_view(application).pageCount == 2

    application.selectedPage = None
    config.showHtmlCodeOptions.value = True

    application.selectedPage = wiki["Викистраница"]
    assert _get_page_view(application).pageCount == 3


def test_result_html_page_2(application: Application, wiki: WikiDocument):
    """The HTML code tab appears when the page mode is switched to HTML."""
    application.wikiroot = wiki

    application.selectedPage = wiki["Викистраница"]
    assert _get_page_view(application).pageCount == 2

    _get_page_view(application).SetPageMode(PAGE_MODE_HTML)

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_HTML
    assert _get_page_view(application).pageCount == 3


def test_invalid_page_index(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]

    # Т.к. страница пустая, то по умолчанию выбирается вкладка с кодом
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    _get_page_view(application)._selectedPageIndex = 100

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    _get_page_view(application)._selectedPageIndex = -1

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    _get_page_view(application).SetPageMode(PAGE_MODE_PREVIEW)

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    _get_page_view(application)._selectedPageIndex = 1000

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    _get_page_view(application)._selectedPageIndex = -1

    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW


def test_save_page_index_1(application: Application, wiki: WikiDocument):
    """The selected page mode is saved for each page."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    wiki["Викистраница"].content = "Бла-бла-бла"
    wiki["Викистраница 2"].content = "Бла-бла-бла 2"
    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]
    wx.GetApp().Yield()

    # В начале по умолчанию выбирается вкладка с просмотром
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    # Переключимся на вкладку с кодом
    _get_page_view(application).SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
    application.selectedPage = wiki["Викистраница 2"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    # Переключимся на результирующий HTML
    _get_page_view(application).SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    # А при возврате на предыдущую страницу, должна быть выбрана страница с кодом
    application.selectedPage = wiki["Викистраница"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    # При переключении на другую страницу, выбирается вкладка с результирующим HTML
    application.selectedPage = wiki["Викистраница 2"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_HTML


def test_save_page_index_2(application: Application, wiki: WikiDocument):
    """The selected page mode is saved for each page."""
    wiki["Викистраница"].content = "Бла-бла-бла"
    wiki["Викистраница 2"].content = "Бла-бла-бла 2"
    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    # Переключимся на вкладку с кодом
    _get_page_view(application).SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    # Переключимся на другую страницу. Опять должна быть выбрана вкладка с просмотром
    application.selectedPage = wiki["Викистраница 2"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_PREVIEW

    # Переключимся на результирующий HTML
    _get_page_view(application).SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    # А при возврате на предыдущую страницу, должна быть выбрана страница с кодом
    application.selectedPage = wiki["Викистраница"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_TEXT

    # При переключении на другую страницу, выбирается вкладка с результирующим HTML
    application.selectedPage = wiki["Викистраница 2"]

    wx.GetApp().Yield()
    assert _get_page_view(application).GetPageMode() == PAGE_MODE_HTML


def test_cursor_position_01(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    application.selectedPage = None

    wiki["Викистраница"].content = "Бла-бла-бла"
    application.selectedPage = wiki["Викистраница"]
    _get_code_editor(application).SetSelection(3, 3)

    application.selectedPage = None
    application.selectedPage = wiki["Викистраница"]
    assert _get_code_editor(application).GetCurrentPosition() == 3


def test_cursor_position_02(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    application.selectedPage = None

    wiki["Викистраница"].content = "Бла-бла-бла"
    application.selectedPage = wiki["Викистраница"]
    _get_code_editor(application).SetSelection(0, 0)

    application.selectedPage = None
    application.selectedPage = wiki["Викистраница"]
    assert _get_code_editor(application).GetCurrentPosition() == 0


def test_cursor_position_readonly_01(application: Application, wiki: WikiDocument):
    application.wikiroot = wiki
    application.selectedPage = None

    # В исходном файле установим курсор на 3-ю позицию
    wiki["Викистраница"].content = "Бла-бла-бла"
    application.selectedPage = wiki["Викистраница"]
    _get_code_editor(application).SetSelection(3, 3)
    application.selectedPage = None

    # Теперь загрузим эту вики в режиме только для чтения и поменяем позицию
    wikiroot_ro = loadNotesTree(wiki.path, readonly=True)
    application.wikiroot = wikiroot_ro
    application.selectedPage = wikiroot_ro["Викистраница"]
    assert _get_code_editor(application).GetCurrentPosition() == 3
    _get_code_editor(application).SetSelection(0, 0)

    # После возвращения на страницу положение курсора не должно поменяться
    application.selectedPage = None
    application.selectedPage = wikiroot_ro["Викистраница"]
    assert _get_code_editor(application).GetCurrentPosition() == 3


def test_postprocessing_01(application: Application, wiki: WikiDocument):
    """The postprocessing handlers are applied to the result HTML."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]
    application.onPostprocessing += _on_postprocessing

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    # Переключимся на вкладку с кодом
    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Переключимся на результирующий HTML
    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    application.onPostprocessing -= _on_postprocessing

    result = page_view.htmlCodeWindow.GetText()

    assert result.endswith(" 111")


def test_postprocessing_02(application: Application, wiki: WikiDocument):
    """All the postprocessing handlers are applied in the registration order."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]

    application.onPostprocessing += _on_postprocessing
    application.onPostprocessing += _on_postprocessing2

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    # Переключимся на вкладку с кодом
    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Переключимся на результирующий HTML
    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    application.onPostprocessing -= _on_postprocessing
    application.onPostprocessing -= _on_postprocessing2

    result = page_view.htmlCodeWindow.GetText()

    assert result.endswith(" 111 222")


def test_postprocessing_03(application: Application, wiki: WikiDocument):
    """The postprocessing is applied only once per HTML result."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]
    application.onPostprocessing += _on_postprocessing

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    # Переключимся на вкладку с кодом
    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Попереключаемся по вкладкам и проверим, что результат
    # постпроцессинга применен однократно
    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    application.onPostprocessing -= _on_postprocessing

    result = page_view.htmlCodeWindow.GetText()

    assert result.endswith(" 111")
    assert not result.endswith(" 111 111")


def test_preprocessing_01(application: Application, wiki: WikiDocument):
    """The preprocessing handlers are applied to the page content."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    application.wikiroot = wiki
    application.selectedPage = wiki["Викистраница"]
    application.onPreprocessing += _on_preprocessing

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    # Переключимся на вкладку с кодом
    page_view.SetPageMode(PAGE_MODE_TEXT)
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Переключимся на результирующий HTML
    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    application.onPreprocessing -= _on_preprocessing

    result = page_view.htmlCodeWindow.GetText()

    assert "Абырвалг 000" in result


def test_save_01(application: Application, wiki: WikiDocument):
    """The page content is saved when the HTML code tab is selected."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    page = wiki["Викистраница"]
    page.content = ""

    application.wikiroot = wiki
    application.selectedPage = page

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Переключимся на результирующий HTML
    page_view.SetPageMode(PAGE_MODE_HTML)
    wx.GetApp().Yield()

    assert page.content == "Абырвалг"


def test_save_02(application: Application, wiki: WikiDocument):
    """The page content is saved when the preview tab is selected."""
    config = WikiConfig(application.config)
    config.showHtmlCodeOptions.value = True

    page = wiki["Викистраница"]
    page.content = ""

    application.wikiroot = wiki
    application.selectedPage = page

    page_view = _get_page_view(application)

    # В начале по умолчанию выбирается вкладка с просмотром
    wx.GetApp().Yield()

    page_view.codeEditor.SetText("Абырвалг")

    # Переключимся на просмотр
    page_view.SetPageMode(PAGE_MODE_PREVIEW)
    wx.GetApp().Yield()

    assert page.content == "Абырвалг"


def test_list_autocomplete_none_01(editor: TextEditor):
    text = ""
    editor.SetText(text)
    editor.GotoPos(0)

    result = listComplete_wiki(editor)
    assert not result
    assert editor.GetText() == text


def test_list_autocomplete_none_02(editor: TextEditor):
    text = "** бла-бла-бла"
    editor.SetText(text)
    editor.GotoPos(1)

    result = listComplete_wiki(editor)
    assert not result
    assert editor.GetText() == text


def test_list_autocomplete_none_03(editor: TextEditor):
    text = "** бла-бла-бла"
    editor.SetText(text)
    editor.SetSelection(5, 8)

    result = listComplete_wiki(editor)
    assert not result
    assert editor.GetText() == text


def test_list_autocomplete_none_04(editor: TextEditor):
    text = "** бла-бла-бла\n** бла-бла-бла"
    editor.SetText(text)
    editor.GotoPos(16)

    result = listComplete_wiki(editor)
    assert not result
    assert editor.GetText() == text


def test_list_autocomplete_01(editor: TextEditor):
    text = "* бла-бла-бла"
    text_result = "* бла-бла-бла\n* "

    editor.SetText(text)
    editor.GotoPos(len(text))

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == len(text_result)


def test_list_autocomplete_02(editor: TextEditor):
    text = "* бла-бла-бла"
    text_result = "* бла\n* -бла-бла"

    editor.SetText(text)
    editor.GotoPos(5)

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == 8


def test_list_autocomplete_03(editor: TextEditor):
    text = "** бла-бла-бла"
    text_result = "** бла-бла-бла\n** "

    editor.SetText(text)
    editor.GotoPos(len(text))

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == len(text_result)


def test_list_autocomplete_04(editor: TextEditor):
    text = "** бла-бла-бла"
    text_result = "** бла\n** -бла-бла"

    editor.SetText(text)
    editor.GotoPos(6)

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == 10


def test_list_autocomplete_05(editor: TextEditor):
    text = "# бла-бла-бла"
    text_result = "# бла-бла-бла\n# "

    editor.SetText(text)
    editor.GotoPos(len(text))

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == len(text_result)


def test_list_autocomplete_06(editor: TextEditor):
    text = "## бла-бла-бла"
    text_result = "## бла-бла-бла\n## "

    editor.SetText(text)
    editor.GotoPos(len(text))

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == len(text_result)


def test_list_autocomplete_07(editor: TextEditor):
    text = "* бла-бла-бла"
    text_result = "*\n*  бла-бла-бла"

    editor.SetText(text)
    editor.GotoPos(1)

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == 4


def test_list_autocomplete_remove_01(editor: TextEditor):
    text = "* "
    text_result = ""

    editor.SetText(text)
    editor.GotoPos(len(text))

    result = listComplete_wiki(editor)
    assert result
    assert editor.GetText() == text_result
    assert editor.GetSelectionStart() == len(text_result)
