
"""Tests for the dialog inserting a diagram group."""

import pytest

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture
def dialog(diagrammer_loader: PluginsLoader, main_window: MainWindow):
    """Dialog for inserting a group with the default parameters."""
    from diagrammer.gui.insertgroupdialog import InsertGroupDialog

    group_dialog = InsertGroupDialog(main_window)

    yield group_dialog

    group_dialog.Destroy()


@pytest.fixture
def controller(dialog):
    """Controller building the group code from the dialog parameters."""
    from diagrammer.gui.insertgroupdialog import InsertGroupController

    return InsertGroupController(dialog)


def test_default(controller):
    assert controller.getResult() == ("group {\n    ", "\n}")


def test_name(controller, dialog):
    dialog.name = "Абырвалг"

    assert controller.getResult() == ("group Абырвалг {\n    ", "\n}")


@pytest.mark.parametrize(
    "is_changed, color, expected",
    [
        pytest.param(
            True, "blue", 'group {\n    color = "blue";\n\n    ', id="color_name"
        ),
        pytest.param(False, "blue", "group {\n    ", id="color_not_changed"),
        pytest.param(
            True, "#AAAAAA", 'group {\n    color = "#AAAAAA";\n\n    ', id="color_code"
        ),
    ],
)
def test_back_color(controller, dialog, is_changed, color, expected):
    dialog.isBackColorChanged = is_changed
    dialog.backColor = color

    assert controller.getResult() == (expected, "\n}")


@pytest.mark.parametrize(
    "is_changed, orientation_index, expected",
    [
        pytest.param(
            True,
            0,
            "group {\n    orientation = landscape;\n\n    ",
            id="landscape",
        ),
        pytest.param(
            True, 1, "group {\n    orientation = portrait;\n\n    ", id="portrait"
        ),
        pytest.param(False, 1, "group {\n    ", id="orientation_not_changed"),
    ],
)
def test_orientation(controller, dialog, is_changed, orientation_index, expected):
    dialog.isOrientationChanged = is_changed
    dialog.orientationIndex = orientation_index

    assert controller.getResult() == (expected, "\n}")


def test_orientation_with_back_color(controller, dialog):
    dialog.isOrientationChanged = True
    dialog.orientationIndex = 1
    dialog.isBackColorChanged = True
    dialog.backColor = "blue"

    assert controller.getResult() == (
        'group {\n    color = "blue";\n    orientation = portrait;\n\n    ',
        "\n}",
    )


@pytest.mark.parametrize(
    "label, expected",
    [
        pytest.param(
            "Абырвалг", 'group {\n    label = "Абырвалг";\n\n    ', id="label"
        ),
        pytest.param("", "group {\n    ", id="empty_label"),
    ],
)
def test_label(controller, dialog, label, expected):
    dialog.label = label

    assert controller.getResult() == (expected, "\n}")


@pytest.mark.parametrize(
    "is_changed, color, expected",
    [
        pytest.param(
            True, "blue", 'group {\n    textcolor = "blue";\n\n    ', id="color_name"
        ),
        pytest.param(False, "blue", "group {\n    ", id="color_not_changed"),
        pytest.param(
            True,
            "#AAAAAA",
            'group {\n    textcolor = "#AAAAAA";\n\n    ',
            id="color_code",
        ),
    ],
)
def test_text_color(controller, dialog, is_changed, color, expected):
    dialog.isTextColorChanged = is_changed
    dialog.textColor = color

    assert controller.getResult() == (expected, "\n}")


@pytest.mark.parametrize(
    "is_changed, shape_index, expected",
    [
        pytest.param(True, 0, "group {\n    shape = box;\n\n    ", id="box"),
        pytest.param(True, 1, "group {\n    shape = line;\n\n    ", id="line"),
        pytest.param(False, 1, "group {\n    ", id="shape_not_changed"),
    ],
)
def test_border_shape(controller, dialog, is_changed, shape_index, expected):
    dialog.isBorderShapeChanged = is_changed
    dialog.borderShapeIndex = shape_index

    assert controller.getResult() == (expected, "\n}")


@pytest.mark.parametrize(
    "style_index, expected",
    [
        pytest.param(
            1,
            "group {\n    shape = line;\n    style = solid;\n\n    ",
            id="solid",
        ),
        pytest.param(
            2,
            "group {\n    shape = line;\n    style = dotted;\n\n    ",
            id="dotted",
        ),
        pytest.param(
            3,
            "group {\n    shape = line;\n    style = dashed;\n\n    ",
            id="dashed",
        ),
    ],
)
def test_border_style(controller, dialog, style_index, expected):
    dialog.isBorderShapeChanged = True
    dialog.borderShapeIndex = 1
    dialog.setStyleIndex(style_index)

    assert controller.getResult() == (expected, "\n}")


def test_border_style_without_border_shape(controller, dialog):
    dialog.isBorderShapeChanged = False
    dialog.borderShapeIndex = 1
    dialog.setStyleIndex(1)

    assert controller.getResult() == ("group {\n    ", "\n}")


def test_border_style_with_box_shape(controller, dialog):
    dialog.isBorderShapeChanged = True
    dialog.borderShapeIndex = 0
    dialog.setStyleIndex(1)

    assert controller.getResult() == ("group {\n    shape = box;\n\n    ", "\n}")


@pytest.mark.parametrize(
    "style",
    [
        pytest.param("1,2,3,4", id="list"),
        pytest.param(" 1, 2, 3, 4 ", id="list_with_spaces"),
    ],
)
def test_border_style_list(controller, dialog, style):
    dialog.isBorderShapeChanged = True
    dialog.borderShapeIndex = 1
    dialog.style = style

    assert controller.getResult() == (
        'group {\n    shape = line;\n    style = "1,2,3,4";\n\n    ',
        "\n}",
    )
