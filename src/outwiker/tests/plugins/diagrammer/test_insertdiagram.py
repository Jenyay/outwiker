"""Tests for the dialog inserting a diagram."""

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture
def dialog(plugin_loader: PluginsLoader, main_window: MainWindow):
    """Dialog for inserting a diagram with the default parameters."""
    from diagrammer.gui.insertdiagramdialog import InsertDiagramDialog

    diagram_dialog = InsertDiagramDialog(main_window)

    yield diagram_dialog

    diagram_dialog.Destroy()


@pytest.fixture
def controller(dialog):
    """Controller building the diagram code from the dialog parameters."""
    from diagrammer.gui.insertdiagramdialog import InsertDiagramController

    return InsertDiagramController(dialog)


def test_default(controller):
    assert controller.getResult() == ("(:diagram:)\n", "\n(:diagramend:)")


@pytest.mark.parametrize(
    "selection, expected",
    [
        pytest.param(0, "(:diagram:)\ndefault_shape = actor;\n", id="actor"),
        pytest.param(1, "(:diagram:)\ndefault_shape = beginpoint;\n", id="beginpoint"),
        pytest.param(2, "(:diagram:)\n", id="default_shape"),
    ],
)
def test_shape(controller, dialog, selection, expected):
    dialog.setShapeSelection(selection)

    assert controller.getResult() == (expected, "\n(:diagramend:)")


@pytest.mark.parametrize(
    "is_changed, color, expected",
    [
        pytest.param(
            True,
            "white",
            '(:diagram:)\ndefault_node_color = "white";\n',
            id="color_name",
        ),
        pytest.param(False, "black", "(:diagram:)\n", id="color_not_changed"),
        pytest.param(
            True,
            "#AAAAAA",
            '(:diagram:)\ndefault_node_color = "#AAAAAA";\n',
            id="color_code",
        ),
    ],
)
def test_node_color(controller, dialog, is_changed, color, expected):
    dialog.isBackColorChanged = is_changed
    dialog.backColor = color

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_node_color_with_shape(controller, dialog):
    dialog.isBackColorChanged = True
    dialog.backColor = "#AAAAAA"
    dialog.setShapeSelection(0)

    assert controller.getResult() == (
        '(:diagram:)\ndefault_shape = actor;\ndefault_node_color = "#AAAAAA";\n',
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, color, expected",
    [
        pytest.param(
            True,
            "white",
            '(:diagram:)\ndefault_textcolor = "white";\n',
            id="color_name",
        ),
        pytest.param(False, "black", "(:diagram:)\n", id="color_not_changed"),
        pytest.param(
            True,
            "#AAAAAA",
            '(:diagram:)\ndefault_textcolor = "#AAAAAA";\n',
            id="color_code",
        ),
    ],
)
def test_text_color(controller, dialog, is_changed, color, expected):
    dialog.isTextColorChanged = is_changed
    dialog.textColor = color

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_text_color_with_shape(controller, dialog):
    dialog.isTextColorChanged = True
    dialog.textColor = "#AAAAAA"
    dialog.setShapeSelection(0)

    assert controller.getResult() == (
        '(:diagram:)\ndefault_shape = actor;\ndefault_textcolor = "#AAAAAA";\n',
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, expected",
    [
        pytest.param(True, "(:diagram:)\ndefault_fontsize = 20;\n", id="size_changed"),
        pytest.param(False, "(:diagram:)\n", id="size_not_changed"),
    ],
)
def test_font_size(controller, dialog, is_changed, expected):
    dialog.isFontSizeChanged = is_changed
    dialog.fontSize = 20

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_font_size_with_shape(controller, dialog):
    dialog.setShapeSelection(0)
    dialog.isFontSizeChanged = True
    dialog.fontSize = 20

    assert controller.getResult() == (
        "(:diagram:)\ndefault_shape = actor;\ndefault_fontsize = 20;\n",
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, expected",
    [
        pytest.param(True, "(:diagram:)\nnode_width = 200;\n", id="width_changed"),
        pytest.param(False, "(:diagram:)\n", id="width_not_changed"),
    ],
)
def test_width(controller, dialog, is_changed, expected):
    dialog.isWidthChanged = is_changed
    dialog.width = 200

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_width_with_shape(controller, dialog):
    dialog.setShapeSelection(0)
    dialog.isWidthChanged = True
    dialog.width = 200

    assert controller.getResult() == (
        "(:diagram:)\ndefault_shape = actor;\nnode_width = 200;\n",
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, expected",
    [
        pytest.param(True, "(:diagram:)\nnode_height = 200;\n", id="height_changed"),
        pytest.param(False, "(:diagram:)\n", id="height_not_changed"),
    ],
)
def test_height(controller, dialog, is_changed, expected):
    dialog.isHeightChanged = is_changed
    dialog.height = 200

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_height_with_shape(controller, dialog):
    dialog.setShapeSelection(0)
    dialog.isHeightChanged = True
    dialog.height = 200

    assert controller.getResult() == (
        "(:diagram:)\ndefault_shape = actor;\nnode_height = 200;\n",
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "orientation_index, expected",
    [
        pytest.param(0, "(:diagram:)\n", id="landscape"),
        pytest.param(1, "(:diagram:)\norientation = portrait;\n", id="portrait"),
    ],
)
def test_orientation(controller, dialog, orientation_index, expected):
    dialog.orientationIndex = orientation_index

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_orientation_with_shape(controller, dialog):
    dialog.orientationIndex = 1
    dialog.setShapeSelection(0)

    assert controller.getResult() == (
        "(:diagram:)\norientation = portrait;\ndefault_shape = actor;\n",
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, expected",
    [
        pytest.param(True, "(:diagram:)\nspan_width = 200;\n", id="span_width_changed"),
        pytest.param(False, "(:diagram:)\n", id="span_width_not_changed"),
    ],
)
def test_span_width(controller, dialog, is_changed, expected):
    dialog.isSpanWidthChanged = is_changed
    dialog.spanWidth = 200

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_span_width_with_shape(controller, dialog):
    dialog.setShapeSelection(0)
    dialog.isSpanWidthChanged = True
    dialog.spanWidth = 200

    assert controller.getResult() == (
        "(:diagram:)\ndefault_shape = actor;\nspan_width = 200;\n",
        "\n(:diagramend:)",
    )


@pytest.mark.parametrize(
    "is_changed, expected",
    [
        pytest.param(
            True, "(:diagram:)\nspan_height = 200;\n", id="span_height_changed"
        ),
        pytest.param(False, "(:diagram:)\n", id="span_height_not_changed"),
    ],
)
def test_span_height(controller, dialog, is_changed, expected):
    dialog.isSpanHeightChanged = is_changed
    dialog.spanHeight = 200

    assert controller.getResult() == (expected, "\n(:diagramend:)")


def test_span_height_with_shape(controller, dialog):
    dialog.setShapeSelection(0)
    dialog.isSpanHeightChanged = True
    dialog.spanHeight = 200

    assert controller.getResult() == (
        "(:diagram:)\ndefault_shape = actor;\nspan_height = 200;\n",
        "\n(:diagramend:)",
    )
