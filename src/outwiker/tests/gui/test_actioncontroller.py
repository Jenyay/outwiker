# -*- coding: utf-8 -*-

from collections.abc import Iterator

import pytest
import wx

from outwiker.app.gui.mainwindow import MainWindow
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core.application import Application
from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.defines import MENU_FILE, TOOLBAR_PLUGINS
from outwiker.gui.hotkey import HotKey
from outwiker.gui.hotkeyoption import HotKeyOption
from outwiker.gui.hotkeyparser import HotKeyParser
from outwiker.gui.theme import Theme

TOOLBAR_IMAGE = "testdata/images/save.png"


class ExampleAction(BaseAction):
    stringId = "test_action"

    def __init__(self):
        self.runCount = 0

    @property
    def title(self):
        return "Тестовый Action"

    @property
    def description(self):
        return "Тестовый Action"

    def run(self, params):
        self.runCount += 1


class ExampleCheckAction(BaseAction):
    stringId = "test_check_action"

    def __init__(self):
        self.runCount = 0

    @property
    def title(self):
        return "Тестовый CheckAction"

    @property
    def description(self):
        return "Тестовый CheckAction"

    def run(self, params):
        if params:
            self.runCount += 1
        else:
            self.runCount -= 1


@pytest.fixture
def action_controller(
    ow_application: OutWikerApplication, main_window: MainWindow
) -> Iterator[ActionController]:
    """
    Action controller with an empty hotkeys config section.

    The main window is shared between the tests of the module, so the actions
    left registered by a test are removed from the GUI on teardown.
    """
    application = ow_application.application
    assert application is not None
    controller = ActionController(main_window, application.config, Theme())
    application.config.remove_section(controller.configSection)

    yield controller

    for strid in controller.getActionsStrId():
        controller.removeGui(strid)

    application.config.remove_section(controller.configSection)


@pytest.fixture
def file_menu(main_window: MainWindow) -> wx.Menu:
    return main_window.menuController[MENU_FILE]


def _assert_menu_item_exists(menu: wx.Menu, title: str, hotkey=None) -> None:
    """Check that the menu contains an item with the title (and the hotkey)."""
    menu_item_id = menu.FindItem(title)
    assert menu_item_id != wx.NOT_FOUND

    menu_item = menu.FindItemById(menu_item_id)

    if hotkey is not None:
        assert menu_item.GetItemLabel() == title + "\t" + HotKeyParser.toString(hotkey)
    else:
        assert menu_item.GetItemLabel() == title


def _emulate_menu_click(main_window: MainWindow, menu_item_id: int) -> None:
    """Emulate selecting a menu item."""
    event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, menu_item_id)
    main_window.ProcessEvent(event)


def _emulate_button_click(main_window: MainWindow, tool_item_id: int) -> None:
    """Emulate clicking a toolbar button."""
    event = wx.CommandEvent(wx.wxEVT_COMMAND_TOOL_CLICKED, tool_item_id)
    main_window.ProcessEvent(event)


def _emulate_check_button_click(
    main_window: MainWindow, toolbar, tool_item_id: int
) -> None:
    """Emulate clicking a check toolbar button."""
    tool_item = toolbar.FindById(tool_item_id)
    new_state = not tool_item.IsToggled()
    toolbar.ToggleTool(tool_item_id, new_state)

    event = wx.CommandEvent(wx.wxEVT_COMMAND_TOOL_CLICKED, tool_item_id)
    event.SetInt(new_state)
    main_window.ProcessEvent(event)


def _get_menu_item_id(action_controller: ActionController, strid: str):
    result = None

    action_info = action_controller.getActionInfo(strid)
    if action_info is not None:
        result = action_info.menuItem.GetId()

    return result


def _get_menu_item(action_controller: ActionController, strid: str):
    result = None

    action_info = action_controller.getActionInfo(strid)
    if action_info is not None:
        result = action_info.menuItem

    return result


def _get_tool_item_id(action_controller: ActionController, strid: str):
    """Get the identifier of the toolbar button."""
    result = None

    action_info = action_controller.getActionInfo(strid)
    if action_info is not None:
        result = action_info.toolItemId

    return result


def _get_tool_item_label(action_controller: ActionController, toolbar, strid: str):
    result = None

    item = _get_tool_item(action_controller, toolbar, strid)

    if item is not None:
        result = item.GetShortHelp()

    return result


def _get_tool_item(action_controller: ActionController, toolbar, strid: str):
    result = None

    item_id = _get_tool_item_id(action_controller, strid)
    if item_id is not None:
        result = toolbar.FindById(item_id)

    return result


def test_register_action(action_controller: ActionController):
    action = ExampleAction()

    assert len(action_controller.getActionsStrId()) == 0

    action_controller.register(action)

    assert len(action_controller.getActionsStrId()) == 1


def test_hot_keys(action_controller: ActionController):
    hotkey1 = HotKey("F1")
    action1 = ExampleAction()

    hotkey2 = HotKey("F2", ctrl=True)
    action2 = ExampleCheckAction()

    action_controller.register(action1, hotkey1)
    action_controller.register(action2, hotkey2)

    assert action_controller.getHotKey(action1.stringId) == hotkey1
    assert action_controller.getHotKey(action2.stringId) == hotkey2


def test_titles(action_controller: ActionController):
    action1 = ExampleAction()
    action2 = ExampleCheckAction()

    action_controller.register(action1)
    action_controller.register(action2)

    assert action_controller.getTitle(action1.stringId) == action1.title
    assert action_controller.getTitle(action2.stringId) == action2.title


def test_append_menu(action_controller: ActionController, file_menu: wx.Menu):
    action = ExampleAction()
    menu = file_menu

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    _assert_menu_item_exists(menu, action.title, None)


def test_append_check_menu(action_controller: ActionController, file_menu: wx.Menu):
    action = ExampleCheckAction()
    menu = file_menu

    action_controller.register(action)
    action_controller.appendMenuCheckItem(action.stringId, menu)
    _assert_menu_item_exists(menu, action.title, None)


def test_remove_action(
    action_controller: ActionController, main_window: MainWindow, file_menu: wx.Menu
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert len(action_controller.getActionsStrId()) == 1
    _assert_menu_item_exists(menu, action.title, None)
    assert toolbar.GetToolsCount() == 1

    action_controller.removeAction(action.stringId)
    toolbar.Realize()

    assert len(action_controller.getActionsStrId()) == 0
    assert menu.FindItem(action.title) == wx.NOT_FOUND
    assert toolbar.GetToolsCount() == 0


def test_remove_action_and_run(
    action_controller: ActionController, main_window: MainWindow, file_menu: wx.Menu
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    menu_item_id = _get_menu_item_id(action_controller, action.stringId)
    tool_item_id = _get_tool_item_id(action_controller, action.stringId)

    _emulate_menu_click(main_window, menu_item_id)
    assert action.runCount == 1

    _emulate_button_click(main_window, tool_item_id)
    assert action.runCount == 2

    action_controller.removeAction(action.stringId)

    _emulate_menu_click(main_window, menu_item_id)
    assert action.runCount == 2

    _emulate_button_click(main_window, tool_item_id)
    assert action.runCount == 2


def test_run_action(
    action_controller: ActionController, main_window: MainWindow, file_menu: wx.Menu
):
    action = ExampleAction()
    menu = file_menu

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)

    menu_item_id = _get_menu_item_id(action_controller, action.stringId)

    _emulate_menu_click(main_window, menu_item_id)

    assert action.runCount == 1

    action_controller.removeAction(action.stringId)

    # The event must not be handled after the menu item is removed
    _emulate_menu_click(main_window, menu_item_id)
    assert action.runCount == 1


def test_append_toolbar_button(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1

    action_controller.removeAction(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 0


def test_append_toolbar_check_button(
    action_controller: ActionController, main_window: MainWindow
):
    action = ExampleCheckAction()
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1

    action_controller.removeAction(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 0


def test_append_toolbar_check_button_and_run(
    action_controller: ActionController, main_window: MainWindow
):
    action = ExampleCheckAction()
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    tool_item_id = _get_tool_item_id(action_controller, action.stringId)

    _emulate_check_button_click(main_window, toolbar, tool_item_id)
    assert action.runCount == 1

    _emulate_check_button_click(main_window, toolbar, tool_item_id)
    assert action.runCount == 0

    _emulate_check_button_click(main_window, toolbar, tool_item_id)
    assert action.runCount == 1

    action_controller.removeAction(action.stringId)


def test_check_button_and_menu_with_events(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleCheckAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    action_controller.appendMenuCheckItem(action.stringId, menu)

    menu_item = _get_menu_item(action_controller, action.stringId)
    tool_item = _get_tool_item(action_controller, toolbar, action.stringId)
    tool_item_id = _get_tool_item_id(action_controller, action.stringId)

    assert not menu_item.IsChecked()
    assert not tool_item.IsToggled()

    _emulate_check_button_click(main_window, toolbar, tool_item_id)

    assert menu_item.IsChecked()
    assert tool_item.IsToggled()

    _emulate_check_button_click(main_window, toolbar, tool_item_id)

    assert not menu_item.IsChecked()
    assert not tool_item.IsToggled()


def test_check_button_and_menu(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleCheckAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    action_controller.appendMenuCheckItem(action.stringId, menu)

    menu_item = _get_menu_item(action_controller, action.stringId)
    tool_item = _get_tool_item(action_controller, toolbar, action.stringId)

    assert not menu_item.IsChecked()
    assert not tool_item.IsToggled()
    assert action.runCount == 0

    action_controller.check(action.stringId, True)

    assert menu_item.IsChecked()
    assert tool_item.IsToggled()
    assert action.runCount == 1

    action_controller.check(action.stringId, True)

    assert menu_item.IsChecked()
    assert tool_item.IsToggled()
    assert action.runCount == 2

    action_controller.check(action.stringId, False)

    assert not menu_item.IsChecked()
    assert not tool_item.IsToggled()
    assert action.runCount == 1

    action_controller.check(action.stringId, False)

    assert not menu_item.IsChecked()
    assert not tool_item.IsToggled()
    assert action.runCount == 0


def test_remove_check_menu(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleCheckAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    action_controller.appendMenuCheckItem(action.stringId, menu)
    action_controller.removeMenuItem(action.stringId)

    tool_item = _get_tool_item(action_controller, toolbar, action.stringId)
    tool_item_id = _get_tool_item_id(action_controller, action.stringId)

    assert not tool_item.IsToggled()

    _emulate_check_button_click(main_window, toolbar, tool_item_id)

    assert tool_item.IsToggled()

    _emulate_check_button_click(main_window, toolbar, tool_item_id)

    assert not tool_item.IsToggled()


def test_append_toolbar_button_only(
    action_controller: ActionController, main_window: MainWindow
):
    action = ExampleAction()
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1

    action_controller.removeAction(action.stringId)

    assert toolbar.GetToolsCount() == 0
    toolbar.Realize()


def test_append_toolbar_button_and_run(
    action_controller: ActionController, main_window: MainWindow, file_menu: wx.Menu
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    menu_item_id = _get_menu_item_id(action_controller, action.stringId)

    _emulate_menu_click(main_window, menu_item_id)
    assert action.runCount == 1

    action_controller.removeAction(action.stringId)

    _emulate_menu_click(main_window, menu_item_id)
    assert action.runCount == 1


def test_append_toolbar_button_only_and_run(
    action_controller: ActionController, main_window: MainWindow
):
    action = ExampleAction()
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    tool_item_id = _get_tool_item_id(action_controller, action.stringId)

    _emulate_button_click(main_window, tool_item_id)
    assert action.runCount == 1

    action_controller.removeAction(action.stringId)

    _emulate_button_click(main_window, tool_item_id)
    assert action.runCount == 1


def test_remove_tool_button(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    _assert_menu_item_exists(menu, action.title, None)

    action_controller.removeToolbarButton(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 0
    _assert_menu_item_exists(menu, action.title, None)


def test_remove_tool_button_invalid(
    action_controller: ActionController, main_window: MainWindow, file_menu: wx.Menu
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 0
    _assert_menu_item_exists(menu, action.title, None)

    action_controller.removeToolbarButton(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 0
    _assert_menu_item_exists(menu, action.title, None)


def test_remove_menu_item_invalid(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert menu.FindItem(action.title) == wx.NOT_FOUND

    action_controller.removeMenuItem(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert menu.FindItem(action.title) == wx.NOT_FOUND


def test_remove_menu_item(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleAction()
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action)
    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    _assert_menu_item_exists(menu, action.title, None)

    action_controller.removeMenuItem(action.stringId)
    toolbar.Realize()

    assert toolbar.GetToolsCount() == 1
    assert menu.FindItem(action.title) == wx.NOT_FOUND


def test_hot_keys_default_menu(action_controller: ActionController, file_menu: wx.Menu):
    action = ExampleAction()
    menu = file_menu
    hotkey = HotKey("T", ctrl=True)

    action_controller.register(action, hotkey=hotkey)
    assert action_controller.getHotKey(action.stringId) == hotkey

    action_controller.appendMenuItem(action.stringId, menu)

    _assert_menu_item_exists(menu, action.title, hotkey)


def test_hot_keys_default_toolbar(
    action_controller: ActionController, main_window: MainWindow
):
    action = ExampleAction()
    hotkey = HotKey("T", ctrl=True)
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action, hotkey=hotkey)
    assert action_controller.getHotKey(action.stringId) == hotkey

    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    assert _get_tool_item_label(
        action_controller, toolbar, action.stringId
    ) == "{0} ({1})".format(action.title, HotKeyParser.toString(hotkey))


def test_disable_tools(action_controller: ActionController, main_window: MainWindow):
    action = ExampleAction()
    hotkey = HotKey("T", ctrl=True)
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    action_controller.register(action, hotkey=hotkey)

    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    tool_id = _get_tool_item_id(action_controller, action.stringId)

    action_controller.enableTools(action.stringId, False)
    assert not toolbar.GetToolEnabled(tool_id)

    action_controller.enableTools(action.stringId, True)
    assert toolbar.GetToolEnabled(tool_id)


def test_disable_menu_item(action_controller: ActionController, file_menu: wx.Menu):
    action = ExampleAction()
    hotkey = HotKey("T", ctrl=True)
    menu = file_menu

    action_controller.register(action, hotkey=hotkey)

    action_controller.appendMenuItem(action.stringId, menu)

    menu_item_id = _get_menu_item_id(action_controller, action.stringId)

    action_controller.enableTools(action.stringId, False)
    assert not menu.IsEnabled(menu_item_id)

    action_controller.enableTools(action.stringId, True)
    assert menu.IsEnabled(menu_item_id)


def test_disable_tools_all(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    action = ExampleAction()
    hotkey = HotKey("T", ctrl=True)
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]
    menu = file_menu

    action_controller.register(action, hotkey=hotkey)

    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    menu_item_id = _get_menu_item_id(action_controller, action.stringId)
    tool_id = _get_tool_item_id(action_controller, action.stringId)

    action_controller.enableTools(action.stringId, False)
    assert not toolbar.GetToolEnabled(tool_id)
    assert not menu.IsEnabled(menu_item_id)

    action_controller.enableTools(action.stringId, True)
    assert toolbar.GetToolEnabled(tool_id)
    assert menu.IsEnabled(menu_item_id)


def test_disable_tools_none(action_controller: ActionController):
    action = ExampleAction()
    hotkey = HotKey("T", ctrl=True)

    action_controller.register(action, hotkey=hotkey)
    action_controller.enableTools(action.stringId, False)


def test_get_action_1(action_controller: ActionController):
    action1 = ExampleAction()
    action2 = ExampleCheckAction()

    action_controller.register(action1)
    action_controller.register(action2)

    assert action_controller.getAction(action1.stringId) == action1
    assert action_controller.getAction(action2.stringId) == action2


def test_get_action_2(action_controller: ActionController):
    action1 = ExampleAction()
    action2 = ExampleCheckAction()
    action_controller.register(action1)

    with pytest.raises(KeyError):
        action_controller.getAction(action2.stringId)


def test_hot_key_load_config(
    action_controller: ActionController, application: Application
):
    action = ExampleAction()
    hotkey_from_config = HotKey("F11")
    HotKeyOption(
        application.config,
        action_controller.configSection,
        action.stringId,
        None,
    ).value = hotkey_from_config

    action_controller.register(action, HotKey("F12", ctrl=True))

    assert action_controller.getHotKey(action.stringId).key == "F11"
    assert not action_controller.getHotKey(action.stringId).ctrl
    assert not action_controller.getHotKey(action.stringId).shift
    assert not action_controller.getHotKey(action.stringId).alt


def test_hot_key_save_config_1(
    action_controller: ActionController,
    main_window: MainWindow,
    application: Application,
):
    action = ExampleAction()
    hotkey = HotKey("F11", ctrl=True)

    action_controller.register(action, hotkey)
    action_controller.saveHotKeys()

    other_action_controller = ActionController(main_window, application.config, Theme())
    other_action_controller.register(action)

    assert other_action_controller.getHotKey(action.stringId).key == "F11"
    assert other_action_controller.getHotKey(action.stringId).ctrl
    assert not other_action_controller.getHotKey(action.stringId).shift
    assert not other_action_controller.getHotKey(action.stringId).alt


def test_hot_key_save_config_2(
    action_controller: ActionController,
    main_window: MainWindow,
    application: Application,
):
    action = ExampleAction()
    hotkey = HotKey("F11", ctrl=True)

    action_controller.register(action, hotkey)
    action_controller.saveHotKeys()

    other_action_controller = ActionController(main_window, application.config, Theme())
    other_action_controller.register(action, HotKey("F1", shift=True))

    assert other_action_controller.getHotKey(action.stringId).key == "F11"
    assert other_action_controller.getHotKey(action.stringId).ctrl
    assert not other_action_controller.getHotKey(action.stringId).shift
    assert not other_action_controller.getHotKey(action.stringId).alt


def test_hot_key_save_config_3(
    action_controller: ActionController,
    main_window: MainWindow,
    application: Application,
):
    action = ExampleAction()

    action_controller.register(action)
    action_controller.saveHotKeys()

    other_action_controller = ActionController(main_window, application.config, Theme())
    other_action_controller.register(action)

    assert other_action_controller.getHotKey(action.stringId) is None


def test_set_hot_key(action_controller: ActionController):
    action = ExampleAction()
    action_controller.register(action, None)

    hotkey = HotKey("F11", ctrl=True)
    action_controller.changeHotkeys([(action.stringId, hotkey)])
    assert action_controller.getHotKey(action.stringId) == hotkey


def test_change_hotkey_gui(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    hotkey = HotKey("F11", ctrl=True)

    action = ExampleAction()
    action_controller.register(action, None)

    action_controller.appendMenuItem(action.stringId, menu)
    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    action_controller.changeHotkeys([(action.stringId, hotkey)])

    assert _get_tool_item_label(
        action_controller, toolbar, action.stringId
    ) == "{} ({})".format(action.title, "Ctrl+F11")

    assert _get_menu_item(
        action_controller, action.stringId
    ).GetItemLabel() == "{}\t{}".format(action.title, "Ctrl+F11")


def test_change_hotkey_gui_menu(
    action_controller: ActionController, file_menu: wx.Menu
):
    menu = file_menu

    hotkey = HotKey("F11", ctrl=True)

    action = ExampleAction()
    action_controller.register(action, None)

    action_controller.appendMenuItem(action.stringId, menu)

    action_controller.changeHotkeys([(action.stringId, hotkey)])

    assert _get_menu_item(
        action_controller, action.stringId
    ).GetItemLabel() == "{}\t{}".format(action.title, "Ctrl+F11")


def test_change_hotkey_toolbar(
    action_controller: ActionController, main_window: MainWindow
):
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    hotkey = HotKey("F11", ctrl=True)

    action = ExampleAction()
    action_controller.register(action, None)

    action_controller.appendToolbarButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    action_controller.changeHotkeys([(action.stringId, hotkey)])

    assert _get_tool_item_label(
        action_controller, toolbar, action.stringId
    ) == "{} ({})".format(action.title, "Ctrl+F11")


def test_change_hotkey_gui_checked_1(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    hotkey = HotKey("F11", ctrl=True)

    action = ExampleCheckAction()
    action_controller.register(action, None)

    action_controller.appendMenuCheckItem(action.stringId, menu)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    action_controller.changeHotkeys([(action.stringId, hotkey)])

    assert _get_tool_item_label(
        action_controller, toolbar, action.stringId
    ) == "{} ({})".format(action.title, "Ctrl+F11")

    assert _get_menu_item(
        action_controller, action.stringId
    ).GetItemLabel() == "{}\t{}".format(action.title, "Ctrl+F11")


def test_change_hotkey_gui_checked_2(
    action_controller: ActionController,
    main_window: MainWindow,
    file_menu: wx.Menu,
):
    menu = file_menu
    toolbar = main_window.toolbars[TOOLBAR_PLUGINS]

    hotkey = HotKey("F11", ctrl=True)

    action = ExampleCheckAction()
    action_controller.register(action, None)

    action_controller.appendMenuCheckItem(action.stringId, menu)
    action_controller.appendToolbarCheckButton(action.stringId, toolbar, TOOLBAR_IMAGE)

    menu_item = _get_menu_item(action_controller, action.stringId)
    tool_item = _get_tool_item(action_controller, toolbar, action.stringId)

    action_controller.changeHotkeys([(action.stringId, hotkey)])
    action_controller.check(action.stringId, True)

    assert menu_item.IsChecked()
    assert tool_item.IsToggled()
