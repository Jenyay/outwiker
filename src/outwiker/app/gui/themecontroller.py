from typing import Optional

import wx

from outwiker.core.application import Application
from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.gui.colors import sanitize_color
from outwiker.gui.guiconfig import MainWindowConfig, TabsConfig, TreeConfig, TagsConfig
from outwiker.gui.theme import Theme


class ThemeController:
    def __init__(self, application: Application) -> None:
        self._application = application
        self._theme: Optional[Theme] = None
        self._first_load = True
        self._application.onPreferencesDialogClose.bind(
            self._onPreferences, EVENT_PRIORITY_MAX_CORE
        )

    def setTheme(self, theme: Theme):
        self.clear()
        self._theme = theme

    def loadFromConfig(self):
        if self._theme is None:
            return

        self._loadGeneralConfig()
        self._loadNotificationConfig()
        self._loadTabsConfig()
        self._loadTreeConfig()
        self._loadTagsConfig()

        self._first_load = False

    def _loadNotificationConfig(self):
        assert self._theme is not None

        mainWindowConfig = MainWindowConfig(self._application.config)
        self._theme.set(
            Theme.SECTION_NOTIFICATION,
            Theme.NOTIFICATION_BACKGROUND_COLOR,
            sanitize_color(mainWindowConfig.mainPanesBackgroundColor),
        )

        self._theme.set(
            Theme.SECTION_NOTIFICATION,
            Theme.NOTIFICATION_TEXT_COLOR,
            sanitize_color(mainWindowConfig.mainPanesTextColor),
        )

    def _loadGeneralConfig(self):
        assert self._theme is not None

        mainWindowConfig = MainWindowConfig(self._application.config)

        self._theme.set(
            Theme.SECTION_GENERAL,
            Theme.BACKGROUND_COLOR,
            sanitize_color(mainWindowConfig.mainPanesBackgroundColor),
        )

        self._theme.set(
            Theme.SECTION_GENERAL,
            Theme.TEXT_COLOR,
            sanitize_color(mainWindowConfig.mainPanesTextColor),
        )

        if self._first_load:
            self._theme.set(
                Theme.SECTION_GENERAL,
                Theme.BUTTONS_ICON_SIZE,
                mainWindowConfig.buttonsIconSize.value,
            )

    def _loadTreeConfig(self):
        assert self._theme is not None

        tree_config = TreeConfig(self._application.config)

        self._theme.set(
            Theme.SECTION_TREE, Theme.TREE_FONT_SIZE, tree_config.fontSize.value
        )

        self._theme.set(
            Theme.SECTION_TREE,
            Theme.TREE_SHOW_NOTE_ICONS,
            tree_config.showNoteIcons.value,
        )

        self._theme.set(
            Theme.SECTION_TREE,
            Theme.TREE_EXTRA_ICON_BOOKMARK,
            tree_config.extraIconBookmark.value,
        )

        self._theme.set(
            Theme.SECTION_TREE,
            Theme.TREE_EXTRA_ICON_READ_ONLY,
            tree_config.extraIconReadOnly.value,
        )

        self._theme.set(
            Theme.SECTION_TREE,
            Theme.TREE_ICON_SIZE,
            tree_config.iconSize.value,
        )

    def _loadTabsConfig(self):
        assert self._theme is not None

        tabsConfig = TabsConfig(self._application.config)

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BACKGROUND_NORMAL_COLOR,
            sanitize_color(tabsConfig.backColorNormal),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BACKGROUND_HOVER_COLOR,
            sanitize_color(tabsConfig.backColorHover),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BACKGROUND_DOWNED_COLOR,
            sanitize_color(tabsConfig.backColorDowned),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BACKGROUND_DRAGGED_COLOR,
            sanitize_color(tabsConfig.backColorDragged),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BACKGROUND_SELECTED_COLOR,
            sanitize_color(tabsConfig.backColorSelected),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_NORMAL_COLOR,
            sanitize_color(tabsConfig.fontColorNormal),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_HOVER_COLOR,
            sanitize_color(tabsConfig.fontColorHover),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_DOWNED_COLOR,
            sanitize_color(tabsConfig.fontColorDowned),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_DRAGGED_COLOR,
            sanitize_color(tabsConfig.fontColorDragged),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_SELECTED_COLOR,
            sanitize_color(tabsConfig.fontColorSelected),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_FONT_SIZE,
            tabsConfig.fontSize.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_BORDER_COLOR,
            sanitize_color(tabsConfig.borderColor),
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_ICON_SIZE,
            tabsConfig.iconSize.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_MIN_WIDTH,
            tabsConfig.minTabWidth.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_MAX_WIDTH,
            tabsConfig.maxTabWidth.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_MARGIN_HORIZONTAL,
            tabsConfig.marginHorizontal.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_MARGIN_VERTICAL,
            tabsConfig.marginVertical.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_SHOW_ICONS,
            tabsConfig.showIcon.value,
        )

        self._theme.set(
            Theme.SECTION_TABS,
            Theme.TABS_SHOW_CLOSE_BUTTON,
            tabsConfig.showCloseButton.value,
        )

    def _loadTagsConfig(self):
        assert self._theme is not None

        tagsConfig = TagsConfig(self._application.config)

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_NORMAL_FONT_COLOR,
            sanitize_color(tagsConfig.normalFontColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_NORMAL_HOVER_BACK_COLOR,
            sanitize_color(tagsConfig.normalHoverBackColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_NORMAL_HOVER_BORDER_COLOR,
            sanitize_color(tagsConfig.normalHoverBorderColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_NORMAL_HOVER_FONT_COLOR,
            sanitize_color(tagsConfig.normalHoverFontColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_ADD_BUTTON_COLOR,
            sanitize_color(tagsConfig.addButtonColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_HOVER_ADD_BUTTON_COLOR,
            sanitize_color(tagsConfig.hoverAddButtonColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_BACK_COLOR,
            sanitize_color(tagsConfig.markedBackColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_BORDER_COLOR,
            sanitize_color(tagsConfig.markedBorderColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_FONT_COLOR,
            sanitize_color(tagsConfig.markedFontColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_HOVER_BACK_COLOR,
            sanitize_color(tagsConfig.markedHoverBackColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_HOVER_BORDER_COLOR,
            sanitize_color(tagsConfig.markedHoverBorderColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_MARKED_HOVER_FONT_COLOR,
            sanitize_color(tagsConfig.markedHoverFontColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_REMOVE_BUTTON_COLOR,
            sanitize_color(tagsConfig.removeButtonColor),
        )

        self._theme.set(
            Theme.SECTION_TAGS,
            Theme.TAGS_HOVER_REMOVE_BUTTON_COLOR,
            sanitize_color(tagsConfig.hoverRemoveButtonColor),
        )

    def loadSystemParams(self):
        if self._theme is None:
            return

        # General
        self._theme.addParam(
            Theme.SECTION_GENERAL,
            Theme.BACKGROUND_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            Theme.SECTION_GENERAL,
            Theme.TEXT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            Theme.SECTION_GENERAL,
            Theme.SELECTION_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self._theme.addParam(
            Theme.SECTION_GENERAL,
            Theme.SELECTION_TEXT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        # Tree
        self._theme.addParam(
            Theme.SECTION_TREE,
            Theme.SELECTION_TEXT_COLOR,
            self._theme.getDefaults(Theme.SECTION_GENERAL, Theme.SELECTION_TEXT_COLOR),
        )

        self._theme.addParam(
            Theme.SECTION_TREE,
            Theme.SELECTION_COLOR,
            self._theme.getDefaults(Theme.SECTION_GENERAL, Theme.SELECTION_COLOR),
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
