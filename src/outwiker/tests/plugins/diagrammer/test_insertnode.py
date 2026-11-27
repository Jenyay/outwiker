"""Tests for the dialog inserting a node into a diagram."""

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture
def dialog(plugin_loader: PluginsLoader, main_window: MainWindow):
    """Dialog for inserting a node with the filled node name."""
    from diagrammer.gui.insertnodedialog import InsertNodeDialog

    node_dialog = InsertNodeDialog(main_window)
    node_dialog.name = "Абырвалг"

    yield node_dialog

    node_dialog.Destroy()


@pytest.fixture
def controller(dialog):
    """Controller building the node code from the dialog parameters."""
    from diagrammer.gui.insertnodedialog import InsertNodeController

    return InsertNodeController(dialog)


def test_name(controller):
    assert controller.getResult() == "Абырвалг"


def test_name_with_spaces(controller, dialog):
    dialog.name = "Абырвалг 111"

    assert controller.getResult() == '"Абырвалг 111"'


@pytest.mark.parametrize(
    "selection, expected",
    [
        pytest.param(0, "Абырвалг", id="default"),
        pytest.param(1, "Абырвалг [shape = actor];", id="actor"),
        pytest.param(10, "Абырвалг [shape = flowchart.database];", id="database"),
    ],
)
def test_shape_selection(controller, dialog, selection, expected):
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "selection, expected",
    [
        pytest.param(0, "Абырвалг", id="default"),
        pytest.param(1, "Абырвалг [style = solid];", id="solid"),
        pytest.param(2, "Абырвалг [style = dotted];", id="dotted"),
    ],
)
def test_border_style_selection(controller, dialog, selection, expected):
    dialog.setStyleIndex(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "style, expected",
    [
        pytest.param("", "Абырвалг", id="empty"),
        pytest.param("solid", "Абырвалг [style = solid];", id="solid"),
        pytest.param("Solid", "Абырвалг [style = solid];", id="solid_capitalized"),
        pytest.param(" Solid ", "Абырвалг [style = solid];", id="solid_with_spaces"),
        pytest.param("1,2,3", 'Абырвалг [style = "1,2,3"];', id="list"),
        pytest.param("1, 2, 3", 'Абырвалг [style = "1,2,3"];', id="list_with_spaces"),
        pytest.param(
            " 1, 2, 3 ",
            'Абырвалг [style = "1,2,3"];',
            id="list_with_outer_spaces",
        ),
        pytest.param('"1,2,3"', 'Абырвалг [style = "1,2,3"];', id="list_quoted"),
    ],
)
def test_border_style(controller, dialog, style, expected):
    dialog.style = style

    assert controller.getResult() == expected


def test_border_style_with_shape(controller, dialog):
    dialog.setShapeSelection(1)
    dialog.style = "dotted"

    assert controller.getResult() == "Абырвалг [shape = actor, style = dotted];"


def test_stacked(controller, dialog):
    dialog.stacked = True

    assert controller.getResult() == "Абырвалг [stacked];"


def test_stacked_with_shape(controller, dialog):
    dialog.stacked = True
    dialog.setShapeSelection(1)

    assert controller.getResult() == "Абырвалг [shape = actor, stacked];"


def test_label(controller, dialog):
    dialog.label = "Превед"

    assert controller.getResult() == 'Абырвалг [label = "Превед"];'


def test_label_with_shape(controller, dialog):
    dialog.setShapeSelection(1)
    dialog.label = "Превед"

    assert controller.getResult() == 'Абырвалг [shape = actor, label = "Превед"];'


def test_label_equal_to_name(controller, dialog):
    dialog.label = "Абырвалг"

    assert controller.getResult() == "Абырвалг"


@pytest.mark.parametrize(
    "is_changed, color, selection, expected",
    [
        pytest.param(True, "white", 0, 'Абырвалг [color = "white"];', id="color_name"),
        pytest.param(
            True, "#AAAAAA", 0, 'Абырвалг [color = "#AAAAAA"];', id="color_code"
        ),
        pytest.param(False, "#AAAAAA", 0, "Абырвалг", id="color_not_changed"),
        pytest.param(
            True,
            "#AAAAAA",
            1,
            'Абырвалг [shape = actor, color = "#AAAAAA"];',
            id="color_code_with_shape",
        ),
    ],
)
def test_back_color(controller, dialog, is_changed, color, selection, expected):
    dialog.isBackColorChanged = is_changed
    dialog.backColor = color
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "is_changed, color, selection, expected",
    [
        pytest.param(
            True, "black", 0, 'Абырвалг [textcolor = "black"];', id="color_name"
        ),
        pytest.param(
            True, "#AAAAAA", 0, 'Абырвалг [textcolor = "#AAAAAA"];', id="color_code"
        ),
        pytest.param(False, "#AAAAAA", 0, "Абырвалг", id="color_not_changed"),
        pytest.param(
            True,
            "#AAAAAA",
            1,
            'Абырвалг [shape = actor, textcolor = "#AAAAAA"];',
            id="color_code_with_shape",
        ),
    ],
)
def test_text_color(controller, dialog, is_changed, color, selection, expected):
    dialog.isTextColorChanged = is_changed
    dialog.textColor = color
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "is_changed, selection, expected",
    [
        pytest.param(True, 0, "Абырвалг [fontsize = 20];", id="size_changed"),
        pytest.param(False, 0, "Абырвалг", id="size_not_changed"),
        pytest.param(
            True,
            1,
            "Абырвалг [shape = actor, fontsize = 20];",
            id="size_changed_with_shape",
        ),
    ],
)
def test_font_size(controller, dialog, is_changed, selection, expected):
    dialog.isFontSizeChanged = is_changed
    dialog.fontSize = 20
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "is_changed, selection, expected",
    [
        pytest.param(True, 0, "Абырвалг [width = 200];", id="width_changed"),
        pytest.param(False, 0, "Абырвалг", id="width_not_changed"),
        pytest.param(
            True,
            1,
            "Абырвалг [shape = actor, width = 200];",
            id="width_changed_with_shape",
        ),
    ],
)
def test_width(controller, dialog, is_changed, selection, expected):
    dialog.isWidthChanged = is_changed
    dialog.width = 200
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected


@pytest.mark.parametrize(
    "is_changed, selection, expected",
    [
        pytest.param(True, 0, "Абырвалг [height = 200];", id="height_changed"),
        pytest.param(False, 0, "Абырвалг", id="height_not_changed"),
        pytest.param(
            True,
            1,
            "Абырвалг [shape = actor, height = 200];",
            id="height_changed_with_shape",
        ),
    ],
)
def test_height(controller, dialog, is_changed, selection, expected):
    dialog.isHeightChanged = is_changed
    dialog.height = 200
    dialog.setShapeSelection(selection)

    assert controller.getResult() == expected
