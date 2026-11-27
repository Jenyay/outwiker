# -*- coding: utf-8 -*-

"""Tests for the actions of the wiki page editor."""

from collections.abc import Iterator
from tempfile import mkdtemp

import pytest

from outwiker.actions.polyactionsid import (
    ALIGN_CENTER_STR_ID,
    ALIGN_JUSTIFY_STR_ID,
    ALIGN_LEFT_STR_ID,
    ALIGN_RIGHT_STR_ID,
    ANCHOR_STR_ID,
    BOLD_ITALIC_STR_ID,
    BOLD_STR_ID,
    CODE_STR_ID,
    HEADING_1_STR_ID,
    HEADING_2_STR_ID,
    HEADING_3_STR_ID,
    HEADING_4_STR_ID,
    HEADING_5_STR_ID,
    HEADING_6_STR_ID,
    HORLINE_STR_ID,
    ITALIC_STR_ID,
    LIST_BULLETS_STR_ID,
    LIST_NUMBERS_STR_ID,
    PREFORMAT_STR_ID,
    QUOTE_STR_ID,
    STRIKE_STR_ID,
    SUBSCRIPT_STR_ID,
    SUPERSCRIPT_STR_ID,
    UNDERLINE_STR_ID,
)
from outwiker.api.core.tree import createNotesTree
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument, WikiPage
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.texteditor import TextEditor
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir

# Actions that wrap the text with the opening and closing syntax
_TURN_SYNTAX = [
    (BOLD_STR_ID, "'''", "'''"),
    (ITALIC_STR_ID, "''", "''"),
    (BOLD_ITALIC_STR_ID, "''''", "''''"),
    (UNDERLINE_STR_ID, "{+", "+}"),
    (STRIKE_STR_ID, "{-", "-}"),
    (SUBSCRIPT_STR_ID, "'_", "_'"),
    (SUPERSCRIPT_STR_ID, "'^", "^'"),
    (ALIGN_LEFT_STR_ID, "%left%", ""),
    (ALIGN_CENTER_STR_ID, "%center%", ""),
    (ALIGN_RIGHT_STR_ID, "%right%", ""),
    (ALIGN_JUSTIFY_STR_ID, "%justify%", ""),
    (PREFORMAT_STR_ID, "[@", "@]"),
    (CODE_STR_ID, "@@", "@@"),
    (ANCHOR_STR_ID, "[[#", "]]"),
    (QUOTE_STR_ID, "[>", "<]"),
]

# Actions that replace the selected text
_REPLACE_SYNTAX = [
    (HORLINE_STR_ID, "----"),
]

# Actions that set the heading level
_HEADINGS_SYNTAX = [
    (HEADING_1_STR_ID, "!!"),
    (HEADING_2_STR_ID, "!!!"),
    (HEADING_3_STR_ID, "!!!!"),
    (HEADING_4_STR_ID, "!!!!!"),
    (HEADING_5_STR_ID, "!!!!!!"),
    (HEADING_6_STR_ID, "!!!!!!!"),
]


@pytest.fixture
def wiki(application: Application, main_window: MainWindow) -> Iterator[WikiDocument]:
    """
    Wiki with the pages used by the tests, opened in the application.

    The main window is created before the wiki is opened.
    """
    path = mkdtemp(prefix="outwiker_wikiactions")
    root = createNotesTree(path)
    factory = WikiPageFactory()
    factory.create(root, "Викистраница", [])
    factory.create(root, "temp", [])

    application.wikiroot = root
    application.selectedPage = root["Викистраница"]

    yield root

    application.selectedPage = None
    application.wikiroot = None
    removeDir(path)


@pytest.fixture
def test_page(wiki: WikiDocument) -> WikiPage:
    """Page whose content is changed by the tests."""
    return wiki["Викистраница"]


@pytest.fixture
def temp_page(wiki: WikiDocument) -> WikiPage:
    """Page used to switch away from the test page."""
    return wiki["temp"]


@pytest.fixture
def editor(application: Application, wiki: WikiDocument) -> TextEditor:
    """Code editor of the test page."""
    return _get_editor(application)


@pytest.fixture
def action_controller(application: Application) -> ActionController:
    """Controller of the application actions."""
    return application.actionController


def _get_editor(application: Application) -> TextEditor:
    """Editor of the currently opened page."""
    return application.mainWindow.pagePanel.pageView.codeEditor


def _get_text(editor: TextEditor) -> str:
    """Text of the editor with the normalized line endings."""
    return editor.GetText().replace("\r\n", "\n")


def _run_action(action_controller: ActionController, action_str: str) -> None:
    """Run the action with the given identifier."""
    action_controller.getAction(action_str).run(None)


def _select_test_page(
    application: Application,
    test_page: WikiPage,
    temp_page: WikiPage,
    content: str,
) -> None:
    """Set the content of the test page and make it current."""
    application.selectedPage = temp_page
    test_page.content = content
    application.selectedPage = test_page


def test_turn_syntax_empty(application, test_page, temp_page, action_controller):
    for action_str, begin, end in _TURN_SYNTAX:
        _select_test_page(application, test_page, temp_page, "")

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == begin + end


def test_turn_syntax_selected_all(
    application, test_page, temp_page, action_controller
):
    text = "Бла-бла-бла"

    for action_str, begin, end in _TURN_SYNTAX:
        _select_test_page(application, test_page, temp_page, text)

        _get_editor(application).SetSelection(0, len(text))

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == begin + text + end


def test_turn_syntax_selected_part(
    application, test_page, temp_page, action_controller
):
    text = "Бла-бла-бла"

    for action_str, begin, end in _TURN_SYNTAX:
        _select_test_page(application, test_page, temp_page, text)

        _get_editor(application).SetSelection(4, 7)

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == f"Бла-{begin}бла{end}-бла"


def test_replace_syntax_empty(application, test_page, temp_page, action_controller):
    for action_str, syntax in _REPLACE_SYNTAX:
        _select_test_page(application, test_page, temp_page, "")

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == syntax


def test_replace_syntax_selected_all(
    application, test_page, temp_page, action_controller
):
    text = "Бла-бла-бла"

    for action_str, syntax in _REPLACE_SYNTAX:
        _select_test_page(application, test_page, temp_page, text)

        _get_editor(application).SetSelection(0, len(text))

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == syntax


def test_replace_syntax_selected_part(
    application, test_page, temp_page, action_controller
):
    text = "Бла-бла-бла"

    for action_str, syntax in _REPLACE_SYNTAX:
        _select_test_page(application, test_page, temp_page, text)

        _get_editor(application).SetSelection(4, 7)

        _run_action(action_controller, action_str)
        assert _get_editor(application).GetText() == f"Бла-{syntax}-бла"


def test_list_bullets_empty(application, test_page, temp_page, action_controller):
    _select_test_page(application, test_page, temp_page, "")

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == "* "


def test_list_numbers_empty(application, test_page, temp_page, action_controller):
    _select_test_page(application, test_page, temp_page, "")

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == "# "


def test_list_bullets_selected_all(
    application, test_page, temp_page, action_controller
):
    text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """* йцкуйцук
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(0, len(text))

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_all(
    application, test_page, temp_page, action_controller
):
    text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """# йцкуйцук
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(0, len(text))

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_01(
    application, test_page, temp_page, action_controller
):
    text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """* йцкуйцук
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    start = 3
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_01(
    application, test_page, temp_page, action_controller
):
    text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """# йцкуйцук
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    start = 3
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_02(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    start = 7
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_03(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    start = 10
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_02(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    start = 7
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_03(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    start = 10
    end = len(text) - 3

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_04(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """* йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 0
    end = 0

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_04(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """# йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 0
    end = 0

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_05(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
* укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 7
    end = 7

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_05(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
# укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 7
    end = 7

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_06(
    application, test_page, temp_page, action_controller
):
    text = """* йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    result = """** йцукен
** укеуке
** ывапвыап
** ывапвыапыап
** ывапываппа"""

    start = 0
    end = len(text)

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_06(
    application, test_page, temp_page, action_controller
):
    text = """# йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    result = """## йцукен
## укеуке
## ывапвыап
## ывапвыапыап
## ывапываппа"""

    start = 0
    end = len(text)

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_07(
    application, test_page, temp_page, action_controller
):
    text = """# йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

    result = """* # йцукен
* # укеуке
* # ывапвыап
* # ывапвыапыап
* # ывапываппа"""

    start = 0
    end = len(text)

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_07(
    application, test_page, temp_page, action_controller
):
    text = """* йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

    result = """# * йцукен
# * укеуке
# * ывапвыап
# * ывапвыапыап
# * ывапываппа"""

    start = 0
    end = len(text)

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_bullets_selected_part_08(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
* укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
** укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 7
    end = 7

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_BULLETS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_list_numbers_selected_part_08(
    application, test_page, temp_page, action_controller
):
    text = """йцукен
# укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    result = """йцукен
## укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

    start = 7
    end = 7

    _select_test_page(application, test_page, temp_page, text)

    _get_editor(application).SetSelection(start, end)

    _run_action(action_controller, LIST_NUMBERS_STR_ID)
    assert _get_editor(application).GetText() == result


def test_heading_1_01(editor, action_controller):
    text = ""

    for action_str, syntax in _HEADINGS_SYNTAX:
        result = f"{syntax} "

        editor.SetText(text)
        editor.SetSelection(0, 0)

        _run_action(action_controller, action_str)
        assert _get_text(editor) == result

        _run_action(action_controller, action_str)
        assert _get_text(editor) == text


def test_heading_1_02(editor, action_controller):
    text = "Строка 1\nСтрока 2\nСтрока 3"

    for action_str, syntax in _HEADINGS_SYNTAX:
        result = f"{syntax} Строка 1\nСтрока 2\nСтрока 3"

        editor.SetText(text)
        editor.SetSelection(5, 5)

        _run_action(action_controller, action_str)
        assert _get_text(editor) == result

        _run_action(action_controller, action_str)
        assert _get_text(editor) == text


def test_heading_1_03(editor, action_controller):
    text = "Строка 1\nСтрока 2\nСтрока 3"

    for action_str, syntax in _HEADINGS_SYNTAX:
        result = f"Строка 1\n{syntax} Строка 2\nСтрока 3"

        editor.SetText(text)
        editor.SetSelection(10, 10)

        _run_action(action_controller, action_str)
        assert _get_text(editor) == result

        _run_action(action_controller, action_str)
        assert _get_text(editor) == text


def test_heading_1_04(editor, action_controller):
    text = "Строка 1\nСтрока 2\nСтрока 3"

    for action_str, syntax in _HEADINGS_SYNTAX:
        result = f"{syntax} Строка 1\n{syntax} Строка 2\nСтрока 3"

        editor.SetText(text)
        editor.SetSelection(0, 10)

        _run_action(action_controller, action_str)
        assert _get_text(editor) == result

        _run_action(action_controller, action_str)
        assert _get_text(editor) == text


def test_heading_switch_01(editor, action_controller):
    text = "Строка 1\nСтрока 2\nСтрока 3"

    editor.SetText(text)
    editor.SetSelection(0, 0)

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == "!! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_2_STR_ID)
    assert _get_text(editor) == "!!! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == "!! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_6_STR_ID)
    assert _get_text(editor) == "!!!!!!! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_5_STR_ID)
    assert _get_text(editor) == "!!!!!! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_5_STR_ID)
    assert _get_text(editor) == text


def test_heading_switch_02(editor, action_controller):
    text = "Строка 1\nСтрока 2\nСтрока 3"

    editor.SetText(text)
    editor.SetSelection(0, 12)

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == "!! Строка 1\n!! Строка 2\nСтрока 3"

    _run_action(action_controller, HEADING_2_STR_ID)
    assert _get_text(editor) == "!!! Строка 1\n!!! Строка 2\nСтрока 3"

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == "!! Строка 1\n!! Строка 2\nСтрока 3"

    _run_action(action_controller, HEADING_6_STR_ID)
    assert _get_text(editor) == "!!!!!!! Строка 1\n!!!!!!! Строка 2\nСтрока 3"

    _run_action(action_controller, HEADING_5_STR_ID)
    assert _get_text(editor) == "!!!!!! Строка 1\n!!!!!! Строка 2\nСтрока 3"

    _run_action(action_controller, HEADING_5_STR_ID)
    assert _get_text(editor) == text


def test_heading_switch_03(editor, action_controller):
    text = "! Строка 1\nСтрока 2\nСтрока 3"

    editor.SetText(text)
    editor.SetSelection(0, 0)

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == "!! ! Строка 1\nСтрока 2\nСтрока 3"

    _run_action(action_controller, HEADING_1_STR_ID)
    assert _get_text(editor) == text
