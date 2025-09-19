from typing import Optional

import wx

from outwiker.core.application import Application
from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.gui.colors import sanitize_color
from outwiker.gui.guiconfig import MainWindowConfig, TabsConfig
from outwiker.gui.theme import Theme


class ThemeController:
    def __init__(self, application: Application) -> None:
        self._application = application
        self._theme: Optional[Theme] = None
        self._application.onPreferencesDialogClose.bind(
            self._onPreferences, EVENT_PRIORITY_MAX_CORE
        )

    def setTheme(self, theme: Theme):
        self.clear()
        self._theme = theme

    def loadFromConfig(self):
        if self._theme is None:
            return

        mainWindowConfig = MainWindowConfig(self._application.config)

        # General
        self._theme.set(
            self._theme.SECTION_GENERAL,
            self._theme.BACKGROUND_COLOR,
            sanitize_color(mainWindowConfig.mainPanesBackgroundColor),
        )

        self._theme.set(
            self._theme.SECTION_GENERAL,
            self._theme.TEXT_COLOR,
            sanitize_color(mainWindowConfig.mainPanesTextColor),
        )

        # Notification
        self._theme.set(
            self._theme.SECTION_NOTIFICATION,
            self._theme.NOTIFICATION_BACKGROUND_COLOR,
            sanitize_color(mainWindowConfig.mainPanesBackgroundColor),
        )

        self._theme.set(
            self._theme.SECTION_NOTIFICATION,
            self._theme.NOTIFICATION_TEXT_COLOR,
            sanitize_color(mainWindowConfig.mainPanesTextColor),
        )

        self._loadTabsConfig()

    def _loadTabsConfig(self):
        assert self._theme is not None

        tabsConfig = TabsConfig(self._application.config)

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BACKGROUND_NORMAL_COLOR,
            sanitize_color(tabsConfig.backColorNormal),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BACKGROUND_HOVER_COLOR,
            sanitize_color(tabsConfig.backColorHover),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BACKGROUND_DOWNED_COLOR,
            sanitize_color(tabsConfig.backColorDowned),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BACKGROUND_DRAGGED_COLOR,
            sanitize_color(tabsConfig.backColorDragged),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BACKGROUND_SELECTED_COLOR,
            sanitize_color(tabsConfig.backColorSelected),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_NORMAL_COLOR,
            sanitize_color(tabsConfig.fontColorNormal),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_HOVER_COLOR,
            sanitize_color(tabsConfig.fontColorHover),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_DOWNED_COLOR,
            sanitize_color(tabsConfig.fontColorDowned),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_DRAGGED_COLOR,
            sanitize_color(tabsConfig.fontColorDragged),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_SELECTED_COLOR,
            sanitize_color(tabsConfig.fontColorSelected),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_FONT_SIZE,
            tabsConfig.fontSize.value,
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_BORDER_COLOR,
            sanitize_color(tabsConfig.borderColor),
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_ICON_SIZE,
            tabsConfig.iconSize.value,
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_MIN_WIDTH,
            tabsConfig.minTabWidth.value,
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_MAX_WIDTH,
            tabsConfig.maxTabWidth.value,
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_MARGIN_HORIZONTAL,
            tabsConfig.marginHorizontal.value,
        )

        self._theme.set(
            self._theme.SECTION_TABS,
            self._theme.TABS_MARGIN_VERTICAL,
            tabsConfig.marginVertical.value,
        )

    def loadSystemParams(self):
        if self._theme is None:
            return

        # General
        self._theme.addParam(
            self._theme.SECTION_GENERAL,
            self._theme.BACKGROUND_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            self._theme.SECTION_GENERAL,
            self._theme.TEXT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            self._theme.SECTION_GENERAL,
            self._theme.SELECTION_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            self._theme.SECTION_GENERAL,
            self._theme.SELECTION_TEXT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        # Tree
        self._theme.addParam(
            self._theme.SECTION_TREE,
            self._theme.SELECTION_TEXT_COLOR,
            self._theme.getDefaults(
                self._theme.SECTION_GENERAL, self._theme.SELECTION_TEXT_COLOR
            ),
        )

        self._theme.addParam(
            self._theme.SECTION_TREE,
            self._theme.SELECTION_COLOR,
            self._theme.getDefaults(
                self._theme.SECTION_GENERAL, self._theme.SELECTION_COLOR
            ),
        )

    def loadParams(self):
        if self._theme is not None:
            self.loadSystemParams()
            self.loadFromConfig()
            self._theme.sendEvent()

    def clear(self):
        if self._theme is not None:
            self._theme.clear()
            self._theme = None

    def _onPreferences(self, dialog):
        if self._theme is not None:
            self.loadFromConfig()
            self._theme.sendEvent()
