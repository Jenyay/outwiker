# -*- coding: utf-8 -*-

"""Tests for editor polyactions on wiki, HTML, and text pages."""

from collections.abc import Iterator

import pytest

from outwiker.actions.polyactionsid import (
    CLIPBOARD_COPY_LINE,
    CLIPBOARD_COPY_WORD,
    CLIPBOARD_CUT_LINE,
    CLIPBOARD_CUT_WORD,
    DELETE_CURRENT_LINE,
    GOTO_NEXT_WORD,
    GOTO_PREV_WORD,
    GOTO_WORD_END,
    GOTO_WORD_START,
    LINE_DUPLICATE_ID,
    MOVE_SELECTED_LINES_DOWN_ID,
    MOVE_SELECTED_LINES_UP_ID,
)
from outwiker.api.app.clipboard import getClipboardText
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.texteditor import TextEditor
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


PAGE_TYPES = [
    pytest.param((WikiPageFactory, "Викистраница", "codeEditor"), id="wiki"),
    pytest.param((HtmlPageFactory, "HTML-страница", "codeEditor"), id="html"),
    pytest.param(
        (TextPageFactory, "Текстовая страница", "textEditor"), id="text"
    ),
]


@pytest.fixture(params=PAGE_TYPES)
def editor(
    request: pytest.FixtureRequest,
    application: Application,
    wikiroot: WikiDocument,
    main_window: MainWindow,
) -> Iterator[TextEditor]:
    page_factory, title, editor_attr = request.param
    page = page_factory().create(wikiroot, title, [])
    application.wikiroot = wikiroot
    application.selectedPage = page

    yield getattr(main_window.pagePanel.pageView, editor_attr)

    application.selectedPage = None
    application.wikiroot = None


@pytest.fixture
def action_controller(application: Application) -> ActionController:
    return application.actionController


class EditorPolyactionsTests:
    """
    Polyactions tests that do not depend on the page type.

    Modules for concrete page types inherit from this class and override the
    ``editor`` fixture (see the Markdown plugin tests).
    """

    def test_line_duplicate_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3"
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = "Строка 1\nСтрока 1\nСтрока 2\nСтрока 3"

        action_controller.getAction(LINE_DUPLICATE_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_line_duplicate_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3"
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = "Строка 1\nСтрока 2\nСтрока 2\nСтрока 3"

        action_controller.getAction(LINE_DUPLICATE_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_line_duplicate_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = "\n"

        action_controller.getAction(LINE_DUPLICATE_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_move_lines_down_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = "Строка 2\nСтрока 1\nСтрока 3\nСтрока 4"

        action_controller.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_move_lines_down_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(0, 15)

        result = "Строка 3\nСтрока 1\nСтрока 2\nСтрока 4"

        action_controller.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_move_lines_up_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = "Строка 2\nСтрока 1\nСтрока 3\nСтрока 4"

        action_controller.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_move_lines_up_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(10, 21)

        result = "Строка 2\nСтрока 3\nСтрока 1\nСтрока 4"

        action_controller.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_move_lines_up_down_empty(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = ""

        action_controller.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

        action_controller.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_delete_current_line_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = "Строка 2\nСтрока 3\nСтрока 4"

        action_controller.getAction(DELETE_CURRENT_LINE).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_delete_current_line_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
        editor.SetText(text)
        editor.SetSelection(10, 10)

        result = "Строка 1\nСтрока 3\nСтрока 4"

        action_controller.getAction(DELETE_CURRENT_LINE).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_delete_current_line_03_empty(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = ""

        action_controller.getAction(DELETE_CURRENT_LINE).run(None)
        assert editor.GetText().replace("\r\n", "\n") == result

    def test_goto_next_word_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_NEXT_WORD).run(None)
        assert editor.GetCurrentPosition() == 6

        action_controller.getAction(GOTO_NEXT_WORD).run(None)
        assert editor.GetCurrentPosition() == 13

        action_controller.getAction(GOTO_NEXT_WORD).run(None)
        assert editor.GetCurrentPosition() == 25

    def test_goto_prev_word_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(25)

        action_controller.getAction(GOTO_PREV_WORD).run(None)
        assert editor.GetCurrentPosition() == 13

        action_controller.getAction(GOTO_PREV_WORD).run(None)
        assert editor.GetCurrentPosition() == 6

        action_controller.getAction(GOTO_PREV_WORD).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_goto_word_empty(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_NEXT_WORD).run(None)
        assert editor.GetCurrentPosition() == 0

        action_controller.getAction(GOTO_PREV_WORD).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_start_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_start_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_start_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(3)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_start_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(5)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_start_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(6)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 6

    def test_go_to_word_start_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(7)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 6

    def test_go_to_word_start_07(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(13)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 13

    def test_go_to_word_start_08(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(14)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 13

    def test_go_to_word_start_09(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(25)

        action_controller.getAction(GOTO_WORD_START).run(None)
        assert editor.GetCurrentPosition() == 13

    def test_go_to_word_end_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 0

    def test_go_to_word_end_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 5

    def test_go_to_word_end_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(1)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 5

    def test_go_to_word_end_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(6)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 12

    def test_go_to_word_end_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(12)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 12

    def test_go_to_word_end_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(13)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 25

    def test_go_to_word_end_07(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(14)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 25

    def test_go_to_word_end_08(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2 ещеоднослово"
        editor.SetText(text)
        editor.GotoPos(25)

        action_controller.getAction(GOTO_WORD_END).run(None)
        assert editor.GetCurrentPosition() == 25

    def test_copy_line_to_clipboard_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text == ""

    def test_copy_line_to_clipboard_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "\n"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text.replace("\r\n", "\n") == "\n"

    def test_copy_line_to_clipboard_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text.replace("\r\n", "\n") == "Строка 1"

    def test_copy_line_to_clipboard_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\n"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text.replace("\r\n", "\n") == "Строка 1\n"

    def test_copy_line_to_clipboard_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2"
        editor.SetText(text)
        editor.GotoPos(9)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text.replace("\r\n", "\n") == "Строка 2"

    def test_copy_line_to_clipboard_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\n"
        editor.SetText(text)
        editor.GotoPos(9)

        action_controller.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        assert cb_text.replace("\r\n", "\n") == "Строка 2\n"

    def test_cut_line_to_clipboard_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText()
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == ""
        assert new_text == ""

    def test_cut_line_to_clipboard_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "Строка 1"
        assert new_text == ""

    def test_cut_line_to_clipboard_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\n"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "Строка 1\n"
        assert new_text == ""

    def test_cut_line_to_clipboard_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "Строка 1\n"
        assert new_text == "Строка 2"

    def test_cut_line_to_clipboard_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2"
        editor.SetText(text)
        editor.GotoPos(9)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "Строка 2"
        assert new_text == "Строка 1\n"

    def test_cut_line_to_clipboard_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "Строка 1\nСтрока 2\nСтрока 3"
        editor.SetText(text)
        editor.GotoPos(9)

        action_controller.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "Строка 2\n"
        assert new_text == "Строка 1\nСтрока 3"

    def test_copy_word_to_clipboard_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == ""

    def test_copy_word_to_clipboard_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == "слово"

    def test_copy_word_to_clipboard_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(2)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == "слово"

    def test_copy_word_to_clipboard_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(5)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == "слово"

    def test_copy_word_to_clipboard_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = " слово "
        editor.SetText(text)
        editor.GotoPos(1)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == "слово"

    def test_copy_word_to_clipboard_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = " слово слово2"
        editor.SetText(text)
        editor.GotoPos(7)

        action_controller.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        assert cb_text == "слово2"

    def test_cut_word_to_clipboard_01(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = ""
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == ""
        assert new_text == ""

    def test_cut_word_to_clipboard_02(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово"
        assert new_text == ""

    def test_cut_word_to_clipboard_03(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(2)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово"
        assert new_text == ""

    def test_cut_word_to_clipboard_04(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово"
        editor.SetText(text)
        editor.GotoPos(5)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово"
        assert new_text == ""

    def test_cut_word_to_clipboard_05(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2"
        editor.SetText(text)
        editor.GotoPos(0)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово"
        assert new_text == " слово2"

    def test_cut_word_to_clipboard_06(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2"
        editor.SetText(text)
        editor.GotoPos(5)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово"
        assert new_text == " слово2"

    def test_cut_word_to_clipboard_07(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2"
        editor.SetText(text)
        editor.GotoPos(6)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово2"
        assert new_text == "слово "

    def test_cut_word_to_clipboard_08(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2"
        editor.SetText(text)
        editor.GotoPos(8)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово2"
        assert new_text == "слово "

    def test_cut_word_to_clipboard_09(
        self, editor: TextEditor, action_controller: ActionController
    ):
        text = "слово слово2"
        editor.SetText(text)
        editor.GotoPos(12)

        action_controller.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace("\r\n", "\n")
        new_text = editor.GetText().replace("\r\n", "\n")

        assert cb_text == "слово2"
        assert new_text == "слово "


class TestEditorPolyactions(EditorPolyactionsTests):
    """Tests for polyactions on the pages built into OutWiker."""
