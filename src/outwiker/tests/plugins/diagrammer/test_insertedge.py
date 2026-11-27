"""Tests for the dialog inserting an edge between the diagram nodes."""

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture
def dialog(plugin_loader: PluginsLoader, main_window: MainWindow):
    """Dialog for inserting an edge with the filled node names."""
    from diagrammer.gui.insertedgedialog import InsertEdgeDialog

    edge_dialog = InsertEdgeDialog(main_window)
    edge_dialog.firstName = "А"
    edge_dialog.secondName = "Б"

    yield edge_dialog

    edge_dialog.Destroy()


@pytest.fixture
def controller(dialog):
    """Controller building the edge with the arrow pointing to the second node."""
    from diagrammer.gui.insertedgedialog import InsertEdgeControllerRight

    return InsertEdgeControllerRight(dialog)


@pytest.fixture
def controller_both(dialog):
    """Controller building the edge with the arrows on the both ends."""
    from diagrammer.gui.insertedgedialog import InsertEdgeControllerBoth

    return InsertEdgeControllerBoth(dialog)


@pytest.mark.parametrize(
    "controller_name, expected",
    [
        pytest.param("InsertEdgeControllerNone", "А -- Б", id="none"),
        pytest.param("InsertEdgeControllerLeft", "А <- Б", id="left"),
        pytest.param("InsertEdgeControllerRight", "А -> Б", id="right"),
        pytest.param("InsertEdgeControllerBoth", "А <-> Б", id="both"),
    ],
)
def test_arrows(dialog, controller_name, expected):
    from diagrammer.gui import insertedgedialog

    controller = getattr(insertedgedialog, controller_name)(dialog)

    assert controller.getResult() == expected


def test_empty_names(dialog, controller_both):
    dialog.firstName = ""
    dialog.secondName = ""

    result = controller_both.getResult()

    assert "1" in result
    assert "2" in result


def test_empty_second_name(dialog, controller_both):
    dialog.secondName = ""

    result = controller_both.getResult()

    assert "1" not in result
    assert "А" in result
    assert "2" in result


def test_empty_first_name(dialog, controller_both):
    dialog.firstName = ""

    result = controller_both.getResult()

    assert "1" in result
    assert "2" not in result
    assert "Б" in result


def test_label(controller, dialog):
    dialog.label = "Абырвалг"

    assert controller.getResult() == 'А -> Б [label = "Абырвалг"]'


@pytest.mark.parametrize(
    "selection, expected",
    [
        pytest.param(0, "А -> Б", id="default"),
        pytest.param(1, "А -> Б [style = solid]", id="solid"),
        pytest.param(2, "А -> Б [style = dotted]", id="dotted"),
        pytest.param(3, "А -> Б [style = dashed]", id="dashed"),
    ],
)
def test_border_style(controller, dialog, selection, expected):
    dialog.setStyleIndex(selection)

    assert controller.getResult() == expected


def test_border_style_with_label(controller, dialog):
    dialog.label = "Абырвалг"
    dialog.setStyleIndex(3)

    assert controller.getResult() == 'А -> Б [label = "Абырвалг", style = dashed]'


@pytest.mark.parametrize(
    "selection, expected",
    [
        pytest.param(0, "А -> Б", id="default"),
        pytest.param(1, "А -> Б [hstyle = generalization]", id="generalization"),
        pytest.param(2, "А -> Б [hstyle = composition]", id="composition"),
        pytest.param(3, "А -> Б [hstyle = aggregation]", id="aggregation"),
    ],
)
def test_arrow_style(controller, dialog, selection, expected):
    dialog.setArrowStyleIndex(selection)

    assert controller.getResult() == expected


def test_arrow_style_with_border_style(controller, dialog):
    dialog.setStyleIndex(3)
    dialog.setArrowStyleIndex(3)

    assert controller.getResult() == "А -> Б [style = dashed, hstyle = aggregation]"


@pytest.mark.parametrize(
    "is_changed, color, selection, expected",
    [
        pytest.param(True, "yellow", 0, 'А -> Б [color = "yellow"]', id="color_name"),
        pytest.param(False, "yellow", 0, "А -> Б", id="color_not_changed"),
        pytest.param(True, "#AAAAAA", 0, 'А -> Б [color = "#AAAAAA"]', id="color_code"),
        pytest.param(
            True,
            "#AAAAAA",
            3,
            'А -> Б [hstyle = aggregation, color = "#AAAAAA"]',
            id="color_code_with_arrow_style",
        ),
    ],
)
def test_line_color(controller, dialog, is_changed, color, selection, expected):
    dialog.isLineColorChanged = is_changed
    dialog.lineColor = color
    dialog.setArrowStyleIndex(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "is_changed, font_size, expected",
    [
        pytest.param(True, 11, "А -> Б [fontsize = 11]", id="size_changed"),
        pytest.param(False, 15, "А -> Б", id="size_not_changed"),
    ],
)
def test_font_size(controller, dialog, is_changed, font_size, expected):
    dialog.isFontSizeChanged = is_changed
    dialog.fontSize = font_size

    assert controller.getResult() == expected


def test_font_size_with_label(controller, dialog):
    dialog.isFontSizeChanged = True
    dialog.fontSize = 11
    dialog.label = "Абырвалг"

    assert controller.getResult() == 'А -> Б [label = "Абырвалг", fontsize = 11]'


@pytest.mark.parametrize(
    "is_changed, color, selection, expected",
    [
        pytest.param(
            True, "yellow", 0, 'А -> Б [textcolor = "yellow"]', id="color_name"
        ),
        pytest.param(False, "yellow", 0, "А -> Б", id="color_not_changed"),
        pytest.param(
            True, "#AAAAAA", 0, 'А -> Б [textcolor = "#AAAAAA"]', id="color_code"
        ),
        pytest.param(
            True,
            "#AAAAAA",
            3,
            'А -> Б [hstyle = aggregation, textcolor = "#AAAAAA"]',
            id="color_code_with_arrow_style",
        ),
    ],
)
def test_text_color(controller, dialog, is_changed, color, selection, expected):
    dialog.isTextColorChanged = is_changed
    dialog.textColor = color
    dialog.setArrowStyleIndex(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "thick, expected",
    [
        pytest.param(True, "А -> Б [thick]", id="thick"),
        pytest.param(False, "А -> Б", id="not_thick"),
    ],
)
def test_thick(controller, dialog, thick, expected):
    dialog.thick = thick

    assert controller.getResult() == expected


def test_thick_with_border_style(controller, dialog):
    dialog.thick = True
    dialog.setStyleIndex(1)

    assert controller.getResult() == "А -> Б [style = solid, thick]"


@pytest.mark.parametrize(
    "folded, expected",
    [
        pytest.param(True, "А -> Б [folded]", id="folded"),
        pytest.param(False, "А -> Б", id="not_folded"),
    ],
)
def test_folded(controller, dialog, folded, expected):
    dialog.folded = folded

    assert controller.getResult() == expected


def test_folded_with_border_style(controller, dialog):
    dialog.folded = True
    dialog.setStyleIndex(1)

    assert controller.getResult() == "А -> Б [style = solid, folded]"
