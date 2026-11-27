# -*- coding: utf-8 -*-

"""Tests for the GUI of the Source plugin."""

from pathlib import Path

import pytest
import wx

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.gui.tester import Tester


# Number of styles in the pygments' STYLE_MAP
STYLES_COUNT = 50


@pytest.fixture
def config(source_loader: PluginsLoader, ow_application):
    """Source plugin configuration with an empty config section."""
    plugin_config = source_loader["Source"].config
    application = ow_application.application

    application.config.remove_section(plugin_config.section)

    yield plugin_config

    application.config.remove_section(plugin_config.section)


@pytest.fixture
def dialog(source_loader: PluginsLoader, ow_application, main_window):
    """Dialog for inserting the (:source:) command."""
    from source.insertdialog import InsertDialog

    insert_dialog = InsertDialog(main_window, ow_application.application.theme)

    yield insert_dialog

    insert_dialog.Destroy()


@pytest.fixture
def controller(config, dialog, wikipage):
    """Controller of the dialog for inserting the (:source:) command."""
    from source.insertdialogcontroller import InsertDialogController

    Tester.dialogTester.clear()
    dialog_controller = InsertDialogController(wikipage, dialog, config)

    yield dialog_controller

    Tester.dialogTester.clear()


def test_dialog_controller1(controller):
    Tester.dialogTester.appendCancel()
    result = controller.showDialog()

    assert result == wx.ID_CANCEL


def test_dialog_controller2(controller):
    Tester.dialogTester.appendOk()
    result = controller.showDialog()

    assert result == wx.ID_OK


def test_dialog_controller_result1(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell", "text"]
    config.defaultLanguage.value = "text"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.tabWidthSpin.SetValue(4)
    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="text" tabwidth="4":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_controller_result2(config, dialog, controller):
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.tabWidthSpin.SetValue(8)
    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="python" tabwidth="8":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_controller_result3(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell", "text"]
    config.defaultLanguage.value = "text"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.tabWidthSpin.SetValue(4)
    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="text" tabwidth="4":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_controller_result4(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell", "text"]
    config.defaultLanguage.value = "text"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.tabWidthSpin.SetValue(0)
    result = controller.getCommandStrings()

    assert result == ('(:source lang="text":)\n', "\n(:sourceend:)")


def test_dialog_controller_result5(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell", "text"]
    config.defaultLanguage.value = "text"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.languageComboBox.SetSelection(0)
    dialog.tabWidthSpin.SetValue(0)
    result = controller.getCommandStrings()

    assert result == ('(:source lang="cpp":)\n', "\n(:sourceend:)")


def test_dialog_controller_result6(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell", "text"]
    config.defaultLanguage.value = "text"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.languageComboBox.SetSelection(1)
    dialog.tabWidthSpin.SetValue(0)
    result = controller.getCommandStrings()

    assert result == ('(:source lang="haskell":)\n', "\n(:sourceend:)")


def test_source_config1(config):
    config.defaultLanguage.value = "python"
    config.tabWidth.value = 8
    config.dialogWidth.value = 100
    config.dialogHeight.value = 200
    config.languageList.value = ["python", "cpp", "haskell"]

    assert config.defaultLanguage.value == "python"
    assert config.tabWidth.value == 8
    assert config.dialogWidth.value == 100
    assert config.dialogHeight.value == 200
    assert config.languageList.value == ["python", "cpp", "haskell"]


def test_dialog_language_values1(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "haskell"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.languageComboBox.GetItems() == [
        "C++",
        "Haskell",
        "Python",
        "Other...",
    ]

    assert dialog.languageComboBox.GetSelection() == 1
    assert dialog.languageComboBox.GetValue() == "Haskell"

    assert dialog.tabWidthSpin.GetValue() == 0


def test_dialog_language_values2(config, dialog, controller):
    config.languageList.value = []
    config.defaultLanguage.value = "haskell"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.languageComboBox.GetItems() == ["text", "Other..."]

    assert dialog.languageComboBox.GetSelection() == 0
    assert dialog.languageComboBox.GetValue() == "text"


def test_dialog_language_values3(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "c"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.languageComboBox.GetItems() == [
        "C++",
        "Haskell",
        "Python",
        "Other...",
    ]

    assert dialog.languageComboBox.GetSelection() == 0
    assert dialog.languageComboBox.GetValue() == "C++"


def test_dialog_language_values4(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "   haskell   "

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.languageComboBox.GetItems() == [
        "C++",
        "Haskell",
        "Python",
        "Other...",
    ]

    assert dialog.languageComboBox.GetSelection() == 1
    assert dialog.languageComboBox.GetValue() == "Haskell"

    assert dialog.tabWidthSpin.GetValue() == 0


def test_dialog_style_values1(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "default"

    result = controller.getCommandStrings()

    assert result == ('(:source lang="python":)\n', "\n(:sourceend:)")


def test_dialog_style_values2(config, dialog, controller):
    config.defaultStyle.value = "blablabla"
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "default"


def test_dialog_style_values3(config, dialog, controller):
    config.defaultStyle.value = ""
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "default"


def test_dialog_style_values4(config, dialog, controller):
    config.defaultStyle.value = "vim"
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "vim"


def test_dialog_style_values5(config, dialog, controller):
    config.defaultStyle.value = "emacs"
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "emacs"


def test_dialog_style1(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"
    config.defaultStyle.value = "vim"
    config.style.value = "vim"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "vim"

    result = controller.getCommandStrings()

    assert result == ('(:source lang="python":)\n', "\n(:sourceend:)")


def test_dialog_style2(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"
    config.defaultStyle.value = "vim"
    config.style.value = "default"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.styleComboBox.GetCount() == STYLES_COUNT
    assert dialog.styleComboBox.GetValue() == "default"

    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="python" style="default":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_style_text(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.styleComboBox.SetSelection(0)

    assert dialog.styleComboBox.GetValue() == "abap"
    assert dialog.style == "abap"

    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="python" style="abap":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_style_file(
    config, dialog, controller, wikipage, samplefiles_path: Path
):
    sources_path = samplefiles_path / "sources"
    Attachment(wikipage).attach([sources_path / "source_utf8.py"])
    Attachment(wikipage).attach([sources_path / "source_cp1251.cs"])

    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.fileCheckBox.SetValue(True)
    dialog.styleComboBox.SetSelection(0)
    dialog.attachmentComboBox.SetValue("source_cp1251.cs")

    assert dialog.styleComboBox.GetValue() == "abap"
    assert dialog.style == "abap"

    result = controller.getCommandStrings()

    assert result == (
        '(:source file="Attach:source_cp1251.cs" lang="python" style="abap":)',
        "(:sourceend:)",
    )


def test_dialog_style_file2(
    config, dialog, controller, wikipage, samplefiles_path: Path
):
    sources_path = samplefiles_path / "sources"
    Attachment(wikipage).attach([sources_path / "source_utf8.py"])
    Attachment(wikipage).attach([sources_path / "source_cp1251.cs"])

    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    dialog.fileCheckBox.SetValue(True)
    dialog.styleComboBox.SetSelection(0)
    dialog.attachmentComboBox.SetValue("source_cp1251.cs")
    dialog.languageComboBox.SetSelection(0)

    assert dialog.styleComboBox.GetValue() == "abap"
    assert dialog.style == "abap"

    result = controller.getCommandStrings()

    assert result == (
        '(:source file="Attach:source_cp1251.cs" style="abap":)',
        "(:sourceend:)",
    )


def test_dialog_style_text2(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.styleComboBox.SetSelection(0)
    dialog.tabWidthSpin.SetValue(5)

    assert dialog.styleComboBox.GetValue() == "abap"
    assert dialog.style == "abap"

    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="python" tabwidth="5" style="abap":)\n',
        "\n(:sourceend:)",
    )


def test_style_config1(config, dialog, controller):
    config.style.value = "default"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.style == "default"


def test_style_config2(config, dialog, controller):
    config.style.value = "vim"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.style == "vim"


def test_style_config3(config, dialog, controller):
    config.style.value = "  vim   "

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.style == "vim"


def test_style_config4(config, dialog, controller):
    config.style.value = "invalid_style"

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.style == "default"


def test_style_config5(config, dialog, controller):
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.style == "default"


def test_parent_bg_config1(config, dialog, controller):
    config.parentbg.value = "  False  "
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.parentbg


def test_parent_bg_config2(config, dialog, controller):
    config.parentbg.value = "  True  "
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.parentbg


def test_parent_bg_config3(config, dialog, controller):
    config.parentbg.value = "  блаблабла  "
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.parentbg


def test_parent_bg_config4(config, dialog, controller):
    # If there are no records in the config file at all
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.parentbg


def test_line_num_config1(config, dialog, controller):
    # If there are no records in the config file at all
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.lineNum


def test_line_num_config2(config, dialog, controller):
    config.lineNum.value = "  False  "
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.lineNum


def test_line_num_config3(config, dialog, controller):
    config.lineNum.value = "  блаблабла  "
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert not dialog.lineNum


def test_line_num_config4(config, dialog, controller):
    config.lineNum.value = "True"
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert dialog.lineNum


def test_dialog_parent_bg(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.parentBgCheckBox.SetValue(True)

    result = controller.getCommandStrings()

    assert result == ('(:source lang="python" parentbg:)\n', "\n(:sourceend:)")


def test_dialog_line_num(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.lineNumCheckBox.SetValue(True)

    result = controller.getCommandStrings()

    assert result == ('(:source lang="python" linenum:)\n', "\n(:sourceend:)")


def test_dialog_parent_bg_line_num(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.parentBgCheckBox.SetValue(True)
    dialog.lineNumCheckBox.SetValue(True)

    result = controller.getCommandStrings()

    assert result == ('(:source lang="python" parentbg linenum:)\n', "\n(:sourceend:)")


def test_dialog_tab_width(config, dialog, controller):
    config.languageList.value = ["python", "cpp", "haskell"]
    config.defaultLanguage.value = "python"

    Tester.dialogTester.appendOk()
    controller.showDialog()
    dialog.tabWidthSpin.SetValue(10)

    result = controller.getCommandStrings()

    assert result == (
        '(:source lang="python" tabwidth="10":)\n',
        "\n(:sourceend:)",
    )


def test_dialog_attach_list_empty(dialog, controller):
    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert len(dialog.attachmentComboBox.GetItems()) == 0


def test_dialog_attach_list_single(
    dialog, controller, wikipage, samplefiles_path: Path
):
    attach = Attachment(wikipage)
    attach.attach([samplefiles_path / "sources" / "source_utf8.py"])

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert len(dialog.attachmentComboBox.GetItems()) == 1


def test_dialog_attach_list_single_subdir(
    dialog, controller, wikipage, samplefiles_path: Path
):
    subdir = "subdir"
    attach = Attachment(wikipage)
    attach.createSubdir(subdir)
    attach.attach([samplefiles_path / "sources" / "source_utf8.py"], subdir)

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert len(dialog.attachmentComboBox.GetItems()) == 2


def test_dialog_attach_list_single_hidden_subdir(
    dialog, controller, wikipage, samplefiles_path: Path
):
    subdir = "subdir"
    attach = Attachment(wikipage)
    attach.createSubdir(subdir)
    attach.createSubdir("__thumb")
    attach.attach([samplefiles_path / "sources" / "source_utf8.py"], subdir)

    Tester.dialogTester.appendOk()
    controller.showDialog()

    assert len(dialog.attachmentComboBox.GetItems()) == 2
