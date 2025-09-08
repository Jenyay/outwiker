from typing import List
from outwiker.app.gui.tabsctrl import TabsGeometryCalculator, TabInfo

import pytest

from outwiker.gui.theme import Theme


@pytest.fixture
def theme() -> Theme:
    theme = Theme()
    calculator = TabsGeometryCalculator(theme)
    theme.set(Theme.SECTION_TABS, Theme.TABS_MIN_WIDTH, 50 - calculator.horizontal_gap_after_tab)
    theme.set(Theme.SECTION_TABS, Theme.TABS_MAX_WIDTH, 150 - calculator.horizontal_gap_after_tab)
    return theme


@pytest.fixture
def calculator(theme: Theme) -> TabsGeometryCalculator:
    calculator = TabsGeometryCalculator(theme)
    return calculator


def test_empty(calculator: TabsGeometryCalculator, theme: Theme):
    text_height = 12
    parent_width = 5 * theme.get(Theme.SECTION_TABS, Theme.TABS_MAX_WIDTH)
    parent_height = 10
    tabs: List[TabInfo] = []
    result = calculator.calc(tabs, parent_width, parent_height, text_height)

    assert len(result) == 0


@pytest.mark.parametrize("tabs_count", [1, 2, 3, 4])
def test_single_line_max_width(
    calculator: TabsGeometryCalculator, theme: Theme, tabs_count: int
):
    theme_max_width = theme.get(Theme.SECTION_TABS, Theme.TABS_MAX_WIDTH)
    text_height = 12
    parent_width = (
        4 * theme_max_width
        + calculator.horizontal_gap_after_tab
        + theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
    )
    parent_height = 10
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)

    min_width = theme_max_width - calculator.horizontal_gap_after_tab
    for n in range(tabs_count):
        assert result[n].width <= theme_max_width and result[n].width >= min_width
        assert result[n].top == result[0].top


def test_single_line_small_width(calculator: TabsGeometryCalculator, theme: Theme):
    tabs_count = 5
    text_height = 12
    theme_max_width = theme.get(Theme.SECTION_TABS, Theme.TABS_MAX_WIDTH)
    parent_width = (tabs_count - 1) * theme_max_width
    parent_height = 10
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)

    for n in range(tabs_count):
        assert (result[n].right - result[n].left) < theme_max_width
        assert result[n].top == result[0].top


def test_right_border(calculator: TabsGeometryCalculator, theme: Theme):
    tabs_count = 8
    text_height = 12
    parent_width = 7 * theme.get(Theme.SECTION_TABS, Theme.TABS_MAX_WIDTH)
    parent_height = 10
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)

    assert result[0].top == result[-1].top
    assert result[-1].right <= parent_width


def test_two_rows(calculator: TabsGeometryCalculator, theme: Theme):
    tabs_count = 3
    text_height = 12
    parent_width = 155 + calculator.horizontal_gap_after_tab + theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
    parent_height = 10
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)

    assert len(result) == 3

    # Check vertical positioning
    assert result[0].top == result[1].top
    assert result[2].top > result[1].bottom


def test_single_line_full_height(
    calculator: TabsGeometryCalculator, theme: Theme):
    text_height = 12
    parent_width = (
        4 * theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
        + calculator.horizontal_gap_after_tab
        + theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
    )
    parent_height = 10
    tabs: List[TabInfo] = []
    tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)
    assert result[0].top == 0


def test_single_line_bottom_align(
    calculator: TabsGeometryCalculator, theme: Theme):
    text_height = 50
    parent_width = (
        4 * theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
        + calculator.horizontal_gap_after_tab
        + theme.get(Theme.SECTION_TABS, Theme.TABS_ADD_BUTTON_SIZE)
    )
    parent_height = 10
    tabs: List[TabInfo] = []
    tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, parent_height, text_height)
    assert result[0].top >= 0
