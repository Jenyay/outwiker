# -*- coding: utf-8 -*-

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.tree import WikiPage
from outwiker.pages.text.textpageeditor import TextPageEditor


@pytest.fixture
def editor(main_window: MainWindow, selected_page: WikiPage) -> TextPageEditor:
    """Text editor of the page opened and selected for the test.

    ``selected_page`` is not used here, but requesting it makes the fixture
    depend on the text page being opened and selected before the editor is
    accessed.
    """
    return main_window.pagePanel.pageView.textEditor


def test_get_set_text(editor: TextPageEditor):
    source_text = "000 Проверка 111"

    editor.SetText(source_text)

    text = editor.GetText()

    assert text == source_text
    assert text[:10] == source_text[:10]


def test_get_text_empty(editor: TextPageEditor):
    assert len(editor.GetText()) == 0


def test_add_text(editor: TextPageEditor):
    editor.AddText("Абырвалг")
    assert editor.GetText() == "Абырвалг"

    editor.AddText("\nРаз два три")
    assert editor.GetText() == "Абырвалг\nРаз два три"


def test_get_selection_empty(editor: TextPageEditor):
    assert len(editor.GetText()) == 0


def test_selection(editor: TextPageEditor):
    text = """Абырвалг
проверка
раз два три
четыре
"""
    editor.SetText(text)
    assert len(editor.GetSelectedText()) == 0

    editor.SetSelection(0, 0)
    assert len(editor.GetSelectedText()) == 0

    editor.SetSelection(0, 1)
    assert editor.GetSelectedText() == "А"

    editor.SetSelection(0, -1)
    assert editor.GetSelectedText() == text[0:-1]

    editor.SetSelection(0, len(text))
    assert editor.GetSelectedText() == text

    editor.SetSelection(11, 16)
    assert editor.GetSelectedText() == text[11:16]


def test_replace_text(editor: TextPageEditor):
    text = """Абырвалг
проверка
раз два три
четыре
"""

    # Replace text in an empty editor
    editor.replaceText("Абырвалг")
    assert editor.GetText() == "Абырвалг"

    editor.SetText(text)
    editor.replaceText("Абырвалг")
    assert (
        editor.GetText()
        == """АбырвалгАбырвалг
проверка
раз два три
четыре
"""
    )

    editor.SetText(text)
    editor.SetSelection(0, 3)
    editor.replaceText("Замена")
    assert (
        editor.GetText()
        == """Заменарвалг
проверка
раз два три
четыре
"""
    )

    editor.SetText(text)
    editor.SetSelection(1, 5)
    editor.replaceText("Замена")
    assert (
        editor.GetText()
        == """АЗаменаалг
проверка
раз два три
четыре
"""
    )


def test_escape_html_empty(editor: TextPageEditor):
    editor.escapeHtml()
    assert len(editor.GetText()) == 0


def test_escape_html(editor: TextPageEditor):
    text = "Проверка > тест < 1234"

    editor.SetText(text)
    editor.escapeHtml()
    assert editor.GetText() == text

    editor.SetText(text)
    editor.SetSelection(0, 10)
    editor.escapeHtml()
    assert editor.GetText() == "Проверка &gt; тест < 1234"

    editor.SetText(text)
    editor.SetSelection(0, -1)
    editor.escapeHtml()
    assert editor.GetText() == "Проверка &gt; тест &lt; 1234"


def test_turn_text_empty(editor: TextPageEditor):
    editor.turnText("Лево", "Право")
    assert editor.GetText() == "ЛевоПраво"


def test_turn_text(editor: TextPageEditor):
    text = "Проверка абырвалг"

    editor.SetText(text)
    editor.SetSelection(0, 1)
    editor.turnText("Лево", "Право")
    assert editor.GetText() == "ЛевоППравороверка абырвалг"

    editor.SetText(text)
    editor.SetSelection(1, 3)
    editor.turnText("Лево", "Право")
    assert editor.GetText() == "ПЛевороПравоверка абырвалг"

    editor.SetText(text)
    editor.SetSelection(0, len(text))
    editor.turnText("Лево", "Право")
    assert editor.GetText() == "ЛевоПроверка абырвалгПраво"


def test_turn_text_selection_01(editor: TextPageEditor):
    text = "Проверка абырвалг"

    editor.SetText(text)
    editor.SetSelection(9, 17)

    assert editor.GetSelectedText() == "абырвалг"

    editor.turnText("Лево ", " Право")

    assert editor.GetSelectedText() == "абырвалг"

    assert editor.GetText() == "Проверка Лево абырвалг Право"


def test_turn_text_selection_02(editor: TextPageEditor):
    text = "Проверка  абырвалг"

    editor.SetText(text)
    editor.SetSelection(9, 9)

    assert editor.GetSelectedText() == ""

    editor.turnText("Лево ", " Право")

    assert editor.GetSelectedText() == ""

    assert editor.GetText() == "Проверка Лево  Право абырвалг"


def test_get_current_position_empty(editor: TextPageEditor):
    assert editor.GetCurrentPosition() == 0


def test_get_current_position(editor: TextPageEditor):
    text = "Проверка абырвалг"
    editor.SetText(text)

    editor.SetSelection(0, 1)
    assert editor.GetCurrentPosition() == 1

    editor.SetSelection(1, 0)
    assert editor.GetCurrentPosition() == 0

    editor.SetSelection(10, 10)
    assert editor.GetCurrentPosition() == 10


def test_get_selection_pos_empty(editor: TextPageEditor):
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 0


def test_get_selection_pos(editor: TextPageEditor):
    text = "Проверка абырвалг"
    editor.SetText(text)

    editor.SetSelection(0, 0)
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 0

    editor.SetSelection(0, 1)
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 1

    editor.SetSelection(10, 10)
    assert editor.GetSelectionStart() == 10
    assert editor.GetSelectionEnd() == 10

    editor.SetSelection(0, len(text))
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == len(text)
    assert editor.GetSelectedText() == text


def test_get_set_search_phrase(editor: TextPageEditor):
    search_controller = editor.searchPanel

    search_controller.setSearchPhrase("Абырвалг")
    assert search_controller.getSearchPhrase() == "Абырвалг"


def test_search_next(editor: TextPageEditor):
    editor.SetText("Абырвалг проверка абырвалг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel

    search_controller.setSearchPhrase("абырвалг")
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 8

    search_controller.nextSearch()
    assert editor.GetSelectionStart() == 18
    assert editor.GetSelectionEnd() == 26

    search_controller.nextSearch()
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 8


def test_search_prev(editor: TextPageEditor):
    editor.SetText("Абырвалг проверка абырвалг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel

    search_controller.setSearchPhrase("абырвалг")

    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 18
    assert editor.GetSelectionEnd() == 26

    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 8

    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 18
    assert editor.GetSelectionEnd() == 26


def test_search_siblings_next(editor: TextPageEditor):
    editor.SetText("ыыыыыыыыы")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel

    search_controller.setSearchPhrase("ыыы")
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 3

    search_controller.nextSearch()
    assert editor.GetSelectionStart() == 3
    assert editor.GetSelectionEnd() == 6

    search_controller.nextSearch()
    assert editor.GetSelectionStart() == 6
    assert editor.GetSelectionEnd() == 9

    search_controller.nextSearch()
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 3


def test_search_siblings_prev(editor: TextPageEditor):
    editor.SetText("ыыыыыыыыы")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel

    search_controller.setSearchPhrase("ыыы")
    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 6
    assert editor.GetSelectionEnd() == 9

    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 3
    assert editor.GetSelectionEnd() == 6

    search_controller.prevSearch()
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 3


def test_get_set_replace_phrase(editor: TextPageEditor):
    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()

    assert search_controller.getReplacePhrase() == ""

    search_controller.setReplacePhrase("Абырвалг")
    assert search_controller.getReplacePhrase() == "Абырвалг"


def test_replace_1(editor: TextPageEditor):
    editor.SetText("Абырвалг проверка абырвалг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("Проверка")
    search_controller.replace()

    assert editor.GetText() == "Абырвалг проверка абырвалг"


def test_replace_2(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("Проверка111")
    search_controller.setSearchPhrase("абырвалг")
    search_controller.replace()

    assert editor.GetText() == "Проверка111 проверка абыРВАлг"
    assert editor.GetSelectionStart() == 21
    assert editor.GetSelectionEnd() == 29

    search_controller.replace()
    assert editor.GetText() == "Проверка111 проверка Проверка111"
    assert editor.GetSelectionStart() == 32
    assert editor.GetSelectionEnd() == 32


def test_replace_3(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(1, 1)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("Проверка111")
    search_controller.setSearchPhrase("абырвалг")

    assert editor.GetSelectionStart() == 18
    assert editor.GetSelectionEnd() == 26

    search_controller.replace()

    assert editor.GetText() == "АбыРваЛг проверка Проверка111"
    assert editor.GetSelectionStart() == 0
    assert editor.GetSelectionEnd() == 8

    search_controller.replace()
    assert editor.GetText() == "Проверка111 проверка Проверка111"
    assert editor.GetSelectionStart() == 11
    assert editor.GetSelectionEnd() == 11


def test_replace_4(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("")
    search_controller.setSearchPhrase("абырвалг")
    search_controller.replace()

    assert editor.GetText() == " проверка абыРВАлг"
    assert editor.GetSelectionStart() == 10
    assert editor.GetSelectionEnd() == 18

    search_controller.replace()
    assert editor.GetText() == " проверка "
    assert editor.GetSelectionStart() == 10
    assert editor.GetSelectionEnd() == 10


def test_replace_all_1(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(0, 0)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("Проверка111")
    search_controller.setSearchPhrase("абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "Проверка111 проверка Проверка111"


def test_replace_all_2(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setReplacePhrase("Проверка111")
    search_controller.setSearchPhrase("абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "Проверка111 проверка Проверка111"


def test_replace_all_3(editor: TextPageEditor):
    editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("Абырвалг111")
    search_controller.replaceAll()

    assert editor.GetText() == "qqq Абырвалг111 проверка Абырвалг111 qqq"


def test_replace_all_4(editor: TextPageEditor):
    editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("111Абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "qqq 111Абырвалг проверка 111Абырвалг qqq"


def test_replace_all_5(editor: TextPageEditor):
    editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("Абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "qqq Абырвалг проверка Абырвалг qqq"


def test_replace_all_6(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг qqq")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("111Абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "111Абырвалг проверка 111Абырвалг qqq"


def test_replace_all_7(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг qqq")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("Абырвалг111")
    search_controller.replaceAll()

    assert editor.GetText() == "Абырвалг111 проверка Абырвалг111 qqq"


def test_replace_all_8(editor: TextPageEditor):
    editor.SetText("ыыы АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("111Абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "ыыы 111Абырвалг проверка 111Абырвалг"


def test_replace_all_9(editor: TextPageEditor):
    editor.SetText("ыыы АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("Абырвалг111")
    search_controller.replaceAll()

    assert editor.GetText() == "ыыы Абырвалг111 проверка Абырвалг111"


def test_replace_all_10(editor: TextPageEditor):
    editor.SetText("АбыРваЛг проверка абыРВАлг")
    editor.SetSelection(10, 10)

    search_controller = editor.searchPanel
    search_controller.switchToReplaceMode()
    search_controller.setSearchPhrase("абырвалг")
    search_controller.setReplacePhrase("Абырвалг")
    search_controller.replaceAll()

    assert editor.GetText() == "Абырвалг проверка Абырвалг"


def test_set_line_01(editor: TextPageEditor):
    editor.SetText("Абырвалг Абырвалг")
    editor.SetLine(0, "Проверка")

    assert editor.GetText() == "Проверка"


def test_set_line_02(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    editor.SetLine(0, "Проверка\n")

    assert (
        editor.GetText()
        == """Проверка
Строка 2
Строка 3"""
    )


def test_set_line_03(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    editor.SetLine(1, "Проверка\n")

    assert (
        editor.GetText()
        == """Строка 1
Проверка
Строка 3"""
    )


def test_set_line_04(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    editor.SetLine(2, "Проверка")

    assert (
        editor.GetText()
        == """Строка 1
Строка 2
Проверка"""
    )


def test_set_line_05(editor: TextPageEditor):
    editor.SetText("")
    editor.SetLine(0, "Проверка")
    assert editor.GetText() == "Проверка"


def test_set_line_06(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    editor.SetLine(0, "Проверка")

    assert (
        editor.GetText()
        == """ПроверкаСтрока 2
Строка 3"""
    )


def test_set_line_07(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    editor.SetLine(2, "Проверка")

    assert (
        editor.GetText()
        == """Строка 1
Строка 2
Проверка"""
    )


def test_get_line_01(editor: TextPageEditor):
    editor.SetText("""Строка 1
Строка 2
Строка 3""")
    assert editor.GetLine(0) == "Строка 1\n"
    assert editor.GetLine(1) == "Строка 2\n"
    assert editor.GetLine(2) == "Строка 3"


def test_get_selection_lines_01(editor: TextPageEditor):
    editor.SetText("")
    editor.SetSelection(0, 0)
    start, end = editor.GetSelectionLines()
    assert start == 0
    assert end == 0


def test_get_selection_lines_02(editor: TextPageEditor):
    editor.SetText("""Проверка\n""")
    editor.SetSelection(0, 8)
    start, end = editor.GetSelectionLines()
    assert start == 0
    assert end == 0


def test_get_selection_lines_03(editor: TextPageEditor):
    editor.SetText("""Проверка\n""")
    editor.SetSelection(0, 9)
    start, end = editor.GetSelectionLines()
    assert start == 0
    assert end == 1


def test_get_selection_lines_04(editor: TextPageEditor):
    editor.SetText("""Проверка\nПроверка\nПроверка""")
    editor.SetSelection(9, 18)
    start, end = editor.GetSelectionLines()
    assert start == 1
    assert end == 2


def test_toddle_line_prefix_01(editor: TextPageEditor):
    editor.SetText("")

    editor.toddleLinePrefix(0, "Тест ")
    assert editor.GetText() == "Тест "

    editor.toddleLinePrefix(0, "Тест ")
    assert editor.GetText() == ""


def test_toddle_line_prefix_02(editor: TextPageEditor):
    editor.SetText("Проверка")

    editor.toddleLinePrefix(0, "Тест ")
    assert editor.GetText() == "Тест Проверка"

    editor.toddleLinePrefix(0, "Тест ")
    assert editor.GetText() == "Проверка"


def test_toddle_line_prefix_03(editor: TextPageEditor):
    editor.SetText("""Проверка
Проверка
Проверка""")

    editor.toddleLinePrefix(0, "Тест ")
    assert (
        editor.GetText()
        == """Тест Проверка
Проверка
Проверка"""
    )

    editor.toddleLinePrefix(0, "Тест ")
    assert (
        editor.GetText()
        == """Проверка
Проверка
Проверка"""
    )


def test_toddle_line_prefix_04(editor: TextPageEditor):
    editor.SetText("""Проверка
Проверка
Проверка""")

    editor.toddleLinePrefix(1, "Тест ")
    assert (
        editor.GetText()
        == """Проверка
Тест Проверка
Проверка"""
    )

    editor.toddleLinePrefix(1, "Тест ")
    assert (
        editor.GetText()
        == """Проверка
Проверка
Проверка"""
    )


def test_toddle_line_prefix_05(editor: TextPageEditor):
    editor.SetText("""Проверка
Проверка
Проверка""")

    editor.toddleLinePrefix(2, "Тест ")
    assert (
        editor.GetText()
        == """Проверка
Проверка
Тест Проверка"""
    )

    editor.toddleLinePrefix(2, "Тест ")
    assert (
        editor.GetText()
        == """Проверка
Проверка
Проверка"""
    )


def test_get_line_start_position_01(editor: TextPageEditor):
    editor.SetText("")
    line_start = editor.GetLineStartPosition(0)
    assert line_start == 0


def test_get_line_start_position_02(editor: TextPageEditor):
    editor.SetText("Проверка")
    line_start = editor.GetLineStartPosition(0)
    assert line_start == 0


def test_get_line_start_position_03(editor: TextPageEditor):
    editor.SetText("Проверка\nПроверка")
    line_start = editor.GetLineStartPosition(1)
    assert line_start == 9


def test_get_line_end_position_01(editor: TextPageEditor):
    editor.SetText("")
    line_end = editor.GetLineEndPosition(0)
    assert line_end == 0


def test_get_line_end_position_02(editor: TextPageEditor):
    editor.SetText("Проверка")
    line_end = editor.GetLineEndPosition(0)
    assert line_end == 8


def test_get_line_end_position_03(editor: TextPageEditor):
    editor.SetText("Проверка\n")
    line_end = editor.GetLineEndPosition(0)
    assert line_end == 8


def test_get_line_end_position_04(editor: TextPageEditor):
    editor.SetText("Проверка\nПроверка")
    line_end = editor.GetLineEndPosition(1)
    assert line_end == 17


def test_toddle_selected_lines_prefix_01(editor: TextPageEditor):
    editor.SetText("")
    editor.SetSelection(0, 0)

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Тест "

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == ""


def test_toddle_selected_lines_prefix_02(editor: TextPageEditor):
    editor.SetText("Проверка")
    editor.SetSelection(0, 0)

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Тест Проверка"

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Проверка"


def test_toddle_selected_lines_prefix_03(editor: TextPageEditor):
    editor.SetText("Проверка\nПроверка")
    editor.SetSelection(2, 5)

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Тест Проверка\nПроверка"

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Проверка\nПроверка"


def test_toddle_selected_lines_prefix_04(editor: TextPageEditor):
    editor.SetText("Проверка\nПроверка")
    editor.SetSelection(2, 9)

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Тест Проверка\nТест Проверка"

    editor.toddleSelectedLinesPrefix("Тест ")
    assert editor.GetText() == "Проверка\nПроверка"


def test_move_selected_lines_down_01(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 0)

    editor.MoveSelectedLinesDown()
    assert editor.GetText() == "Строка 2\nСтрока 1\nСтрока 3\nСтрока 4"


def test_move_selected_lines_down_02(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(9, 9)

    editor.MoveSelectedLinesDown()
    assert editor.GetText() == "Строка 1\nСтрока 3\nСтрока 2\nСтрока 4"


def test_move_selected_lines_down_03(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 10)

    editor.MoveSelectedLinesDown()
    assert editor.GetText() == "Строка 3\nСтрока 1\nСтрока 2\nСтрока 4"


def test_move_selected_lines_down_04(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 18)

    editor.MoveSelectedLinesDown()
    assert editor.GetText() == "Строка 3\nСтрока 1\nСтрока 2\nСтрока 4"


def test_move_selected_lines_up_01(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(9, 9)

    editor.MoveSelectedLinesUp()
    assert editor.GetText() == "Строка 2\nСтрока 1\nСтрока 3\nСтрока 4"


def test_move_selected_lines_up_02(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(9, 23)

    editor.MoveSelectedLinesUp()
    assert editor.GetText() == "Строка 2\nСтрока 3\nСтрока 1\nСтрока 4"


def test_line_duplicate_01(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 0)

    editor.LineDuplicate()
    assert (
        editor.GetText().replace("\r\n", "\n")
        == "Строка 1\nСтрока 1\nСтрока 2\nСтрока 3\nСтрока 4"
    )


def test_line_duplicate_02(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(9, 9)

    editor.LineDuplicate()
    assert (
        editor.GetText().replace("\r\n", "\n")
        == "Строка 1\nСтрока 2\nСтрока 2\nСтрока 3\nСтрока 4"
    )


def test_line_delete_01(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 0)

    editor.LineDelete()
    assert editor.GetText().replace("\r\n", "\n") == "Строка 2\nСтрока 3\nСтрока 4"


def test_line_delete_02(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(10, 10)

    editor.LineDelete()
    assert editor.GetText().replace("\r\n", "\n") == "Строка 1\nСтрока 3\nСтрока 4"


def test_line_delete_03_empty(editor: TextPageEditor):
    editor.SetText("")
    editor.SetSelection(0, 0)

    editor.LineDelete()
    assert editor.GetText().replace("\r\n", "\n") == ""


def test_join_lines_01(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 0)

    editor.JoinLines()
    assert (
        editor.GetText().replace("\r\n", "\n")
        == "Строка 1Строка 2\nСтрока 3\nСтрока 4"
    )


def test_join_lines_02(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 13)

    editor.JoinLines()
    assert (
        editor.GetText().replace("\r\n", "\n")
        == "Строка 1Строка 2\nСтрока 3\nСтрока 4"
    )


def test_join_lines_03(editor: TextPageEditor):
    editor.SetText("Строка 1\nСтрока 2\nСтрока 3\nСтрока 4")
    editor.SetSelection(0, 20)

    editor.JoinLines()
    assert (
        editor.GetText().replace("\r\n", "\n") == "Строка 1Строка 2Строка 3\nСтрока 4"
    )


def test_join_lines_04(editor: TextPageEditor):
    text = "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
    editor.SetText(text)
    editor.SetSelection(len(text) - 1, len(text) - 1)

    editor.JoinLines()
    assert (
        editor.GetText().replace("\r\n", "\n")
        == "Строка 1\nСтрока 2\nСтрока 3\nСтрока 4"
    )


def test_go_to_word_start_01(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    editor.GotoPos(0)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 0


def test_go_to_word_start_02(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(0)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 0


def test_go_to_word_start_03(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(3)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 0


def test_go_to_word_start_04(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(5)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 0


def test_go_to_word_start_05(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(6)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 6


def test_go_to_word_start_06(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(7)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 6


def test_go_to_word_start_07(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(13)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 13


def test_go_to_word_start_08(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(14)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 13


def test_go_to_word_start_09(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(25)

    editor.GotoWordStart()
    assert editor.GetCurrentPosition() == 13


def test_go_to_word_end_01(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    editor.GotoPos(0)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 0


def test_go_to_word_end_02(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(0)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 5


def test_go_to_word_end_03(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(1)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 5


def test_go_to_word_end_04(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(6)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 12


def test_go_to_word_end_05(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(12)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 12


def test_go_to_word_end_06(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(13)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 25


def test_go_to_word_end_07(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(14)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 25


def test_go_to_word_end_08(editor: TextPageEditor):
    text = "слово слово2 ещеоднослово"
    editor.SetText(text)
    editor.GotoPos(25)

    editor.GotoWordEnd()
    assert editor.GetCurrentPosition() == 25


def test_word_start_position_01(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    word_start = editor.WordStartPosition(0)

    assert word_start == 0


def test_word_start_position_02(editor: TextPageEditor):
    text = "слово"
    editor.SetText(text)
    word_start = editor.WordStartPosition(0)

    assert word_start == 0


def test_word_start_position_03(editor: TextPageEditor):
    text = "слово"
    editor.SetText(text)
    word_start = editor.WordStartPosition(3)

    assert word_start == 0


def test_word_start_position_04(editor: TextPageEditor):
    text = " слово"
    editor.SetText(text)
    word_start = editor.WordStartPosition(3)

    assert word_start == 1


def test_word_start_position_05(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word_start = editor.WordStartPosition(7)

    assert word_start == 7


def test_word_start_position_06(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word_start = editor.WordStartPosition(9)

    assert word_start == 7


def test_word_end_position_01(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    word_end = editor.WordEndPosition(0)

    assert word_end == 0


def test_word_end_position_02(editor: TextPageEditor):
    text = "слово"
    editor.SetText(text)
    word_end = editor.WordEndPosition(0)

    assert word_end == 5


def test_word_end_position_03(editor: TextPageEditor):
    text = "слово"
    editor.SetText(text)
    word_end = editor.WordEndPosition(3)

    assert word_end == 5


def test_word_end_position_04(editor: TextPageEditor):
    text = " слово"
    editor.SetText(text)
    word_end = editor.WordEndPosition(3)

    assert word_end == 6


def test_word_end_position_05(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word_end = editor.WordEndPosition(7)

    assert word_end == 13


def test_word_end_position_06(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word_end = editor.WordEndPosition(9)

    assert word_end == 13


def test_get_word_01(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    word = editor.GetWord(0)

    assert word == ""


def test_get_word_02(editor: TextPageEditor):
    text = ""
    editor.SetText(text)
    word = editor.GetWord(10)

    assert word == ""


def test_get_word_03(editor: TextPageEditor):
    text = "слово"
    editor.SetText(text)
    word = editor.GetWord(0)

    assert word == "слово"


def test_get_word_04(editor: TextPageEditor):
    text = " слово "
    editor.SetText(text)
    word = editor.GetWord(1)

    assert word == "слово"


def test_get_word_05(editor: TextPageEditor):
    text = " слово "
    editor.SetText(text)
    word = editor.GetWord(6)

    assert word == "слово"


def test_get_word_06(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word = editor.GetWord(7)

    assert word == "слово2"


def test_get_word_07(editor: TextPageEditor):
    text = " слово слово2"
    editor.SetText(text)
    word = editor.GetWord(13)

    assert word == "слово2"


def test_get_word_08(editor: TextPageEditor):
    text = " слово слово2 "
    editor.SetText(text)
    word = editor.GetWord(13)

    assert word == "слово2"


def test_get_word_09(editor: TextPageEditor):
    text = " слово слово2 "
    editor.SetText(text)
    word = editor.GetWord(100)

    assert word == ""
