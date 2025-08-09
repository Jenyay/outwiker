from typing import List
from outwiker.app.gui.tabsctrl import TabsGeometryCalculator, TabInfo

import pytest

from outwiker.gui.theme import Theme


@pytest.fixture
def calculator() -> TabsGeometryCalculator:
    calculator = TabsGeometryCalculator(Theme())
    calculator.min_width = 25 - calculator.horizontal_gap_between_tabs
    calculator.max_width = 100 - calculator.horizontal_gap_between_tabs
    return calculator


def test_empty(calculator: TabsGeometryCalculator):
    text_height = 12
    parent_width = 5 * calculator.max_width
    tabs: List[TabInfo] = []
    result = calculator.calc(tabs, parent_width, text_height)

    assert len(result) == 0


@pytest.mark.parametrize("tabs_count", [1, 2, 3, 4])
def test_single_line_max_width(calculator: TabsGeometryCalculator, tabs_count: int):
    text_height = 12
    parent_width = 4 * calculator.max_width
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    min_width = calculator.max_width - calculator.horizontal_gap_between_tabs
    for n in range(tabs_count):
        assert result[n].width <= calculator.max_width and result[n].width >= min_width
        assert result[n].top == result[0].top


def test_single_line_small_width(calculator: TabsGeometryCalculator):
    tabs_count = 5
    text_height = 12
    parent_width = (tabs_count - 1) * calculator.max_width
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    for n in range(tabs_count):
        assert (result[n].right - result[n].left) < calculator.max_width
        assert result[n].top == result[0].top


def test_right_border(calculator: TabsGeometryCalculator):
    tabs_count = 8
    text_height = 12
    parent_width = 5 * calculator.max_width
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    assert result[0].top == result[-1].top
    assert result[-1].right <= parent_width


def test_two_rows(calculator: TabsGeometryCalculator):
    tabs_count = 3
    text_height = 12
    parent_width = 55
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    assert len(result) == 3

    # Check vertical positioning
    assert result[0].top == result[1].top
    assert result[2].top > result[1].bottom
