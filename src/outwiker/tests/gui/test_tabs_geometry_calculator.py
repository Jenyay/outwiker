from typing import List
from outwiker.app.gui.tabsctrl import TabsGeometryCalculator, TabInfo

import pytest


@pytest.fixture
def calculator() -> TabsGeometryCalculator:
    calculator = TabsGeometryCalculator()
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

    for n in range(tabs_count):
        assert (result[0][n].right - result[0][n].left) == calculator.max_width
        assert result[0][n].top == result[0][0].top


def test_single_line_small_width(calculator: TabsGeometryCalculator):
    tabs_count = 5
    text_height = 12
    parent_width = (tabs_count - 1) * calculator.max_width
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    for n in range(tabs_count):
        assert (result[0][n].right - result[0][n].left) < calculator.max_width
        assert result[0][n].top == result[0][0].top


def test_two_rows(calculator: TabsGeometryCalculator):
    tabs_count = 3
    text_height = 12
    parent_width = 55
    tabs: List[TabInfo] = []
    for _ in range(tabs_count):
        tabs.append(TabInfo(None, "title"))

    result = calculator.calc(tabs, parent_width, text_height)

    assert len(result) == 2
    assert len(result[0]) == 2
    assert len(result[1]) == 1

    # Check vertical positioning
    assert result[1][0].top > result[0][0].bottom
