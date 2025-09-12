from typing import Any, Dict, Set, Tuple
import logging

from outwiker.core.event import Event


logger = logging.getLogger("outwiker.gui.theme")


class Theme:
    # Sections
    SECTION_GENERAL = "General"
    SECTION_TREE = "Tree"
    SECTION_RENDER = "Render"
    SECTION_EDITOR = "Editor"
    SECTION_HTML_EDITOR = "HtmlEditor"
    SECTION_WIKI_EDITOR = "WikiEditor"
    SECTION_NOTIFICATION = "Notification"
    SECTION_TABS = "Tabs"

    # General section
    BACKGROUND_COLOR = "BackgroundColor"
    TEXT_COLOR = "FontColor"
    HYPERLINK_COLOR = "HyperlinkColor"
    SELECTION_COLOR = "SelectionColor"
    SELECTION_TEXT_COLOR = "SelectionTextColor"
    SHADOW_COLOR = "ShadowColor"
    CONTROL_BORDER_COLOR = "ControlBorderColor"
    CONTROL_BORDER_SELECTED_COLOR = "ControlBorderSelectedColor"
    STATIC_LINE_COLOR = "StaticLineColor"
    ROUND_RADIUS = "RoundRadius"

    # Tree section
    HIGHLIGHTING_COLOR = "HighlightingColor"
    HIGHLIGHTING_TEXT_COLOR = "HighlightingTextColor"

    # Notification
    NOTIFICATION_BACKGROUND_COLOR = "BackgroundColor"
    NOTIFICATION_TEXT_COLOR = "TextColor"
    NOTIFICATION_ERROR_CAPTION_BACKGROUND_COLOR = "ErrorCaptionBackgroundColor"
    NOTIFICATION_ERROR_CAPTION_TEXT_COLOR = "ErrorCaptionTextColor"
    NOTIFICATION_INFO_CAPTION_BACKGROUND_COLOR = "InfoCaptionBackgroundColor"
    NOTIFICATION_INFO_CAPTION_TEXT_COLOR = "InfoCaptionTextColor"

    # Tabs
    TABS_BACKGROUND_NORMAL_COLOR = "BackgroundNormalColor"
    TABS_BACKGROUND_HOVER_COLOR = "BackgroundHoverColor"
    TABS_BACKGROUND_DOWNED_COLOR = "BackgroundDownedColor"
    TABS_BACKGROUND_DRAGGED_COLOR = "BackgroundDraggedColor"
    TABS_BACKGROUND_SELECTED_COLOR = "BackgroundSelectedColor"
    TABS_BORDER_COLOR = "BorderColor"
    TABS_ICON_SIZE = "IconSize"
    TABS_CLOSE_BUTTON_SIZE = "CloseButtonSize"
    TABS_ADD_BUTTON_SIZE = "AddButtonSize"
    TABS_MIN_WIDTH = "MinWidth"
    TABS_MAX_WIDTH = "MaxWidth"
    TABS_MARGIN_HORIZONTAL = "MarginHorizontal"
    TABS_MARGIN_VERTICAL = "MarginVertical"

    def __init__(self):
        self._data: Dict[str, Tuple[Any, Any]] = {}
        self._initDefaults()
        self._changed_sections: Set[str] = set()

        # Event occurs after theme changing
        # Parameters:
        #    params - instance of the ThemeChangedParams class
        self.onThemeChanged = Event()

    def _initDefaults(self):
        self.addParam(self.SECTION_GENERAL, self.BACKGROUND_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_GENERAL, self.TEXT_COLOR, "#000000")
        self.addParam(self.SECTION_GENERAL, self.HYPERLINK_COLOR, "#0000FF")
        self.addParam(self.SECTION_GENERAL, self.SELECTION_COLOR, "#0000FF")
        self.addParam(self.SECTION_GENERAL, self.SELECTION_TEXT_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_GENERAL, self.SHADOW_COLOR, "#AAAAAA")
        self.addParam(self.SECTION_GENERAL, self.CONTROL_BORDER_COLOR, "#000000")
        self.addParam(
            self.SECTION_GENERAL, self.CONTROL_BORDER_SELECTED_COLOR, "#0000FF"
        )
        self.addParam(self.SECTION_GENERAL, self.STATIC_LINE_COLOR, "#AAAAAA")
        self.addParam(self.SECTION_GENERAL, self.ROUND_RADIUS, 0)

        self.addParam(self.SECTION_TREE, self.SELECTION_COLOR, "#0000FF")
        self.addParam(self.SECTION_TREE, self.SELECTION_TEXT_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_TREE, self.HIGHLIGHTING_COLOR, "#E1EFFA")
        self.addParam(self.SECTION_TREE, self.HIGHLIGHTING_TEXT_COLOR, "#000000")

        self.addParam(
            self.SECTION_NOTIFICATION, self.NOTIFICATION_BACKGROUND_COLOR, "#FFFFFF"
        )
        self.addParam(
            self.SECTION_NOTIFICATION, self.NOTIFICATION_TEXT_COLOR, "#000000"
        )
        self.addParam(
            self.SECTION_NOTIFICATION,
            self.NOTIFICATION_ERROR_CAPTION_BACKGROUND_COLOR,
            "#C80003",
        )
        self.addParam(
            self.SECTION_NOTIFICATION,
            self.NOTIFICATION_ERROR_CAPTION_TEXT_COLOR,
            "#E3E3E3",
        )
        self.addParam(
            self.SECTION_NOTIFICATION,
            self.NOTIFICATION_INFO_CAPTION_BACKGROUND_COLOR,
            "#1989FF",
        )
        self.addParam(
            self.SECTION_NOTIFICATION,
            self.NOTIFICATION_INFO_CAPTION_TEXT_COLOR,
            "#E3E3E3",
        )

        # Tabs
        self.addParam(self.SECTION_TABS, self.TABS_BACKGROUND_NORMAL_COLOR, "#D4D4CE")
        self.addParam(self.SECTION_TABS, self.TABS_BACKGROUND_HOVER_COLOR, "#DDDDDD")
        self.addParam(self.SECTION_TABS, self.TABS_BACKGROUND_DOWNED_COLOR, "#AAAAAA")
        self.addParam(self.SECTION_TABS, self.TABS_BACKGROUND_DRAGGED_COLOR, "#AAAAAA")
        self.addParam(self.SECTION_TABS, self.TABS_BACKGROUND_SELECTED_COLOR, "#F3F3F0")
        self.addParam(self.SECTION_TABS, self.TABS_BORDER_COLOR, "#B3B3B3")
        self.addParam(self.SECTION_TABS, self.TABS_ICON_SIZE, 16)
        self.addParam(self.SECTION_TABS, self.TABS_CLOSE_BUTTON_SIZE, 16)
        self.addParam(self.SECTION_TABS, self.TABS_ADD_BUTTON_SIZE, 20)
        self.addParam(self.SECTION_TABS, self.TABS_MIN_WIDTH, 150)
        self.addParam(self.SECTION_TABS, self.TABS_MAX_WIDTH, 450)
        self.addParam(self.SECTION_TABS, self.TABS_MARGIN_HORIZONTAL, 8)
        self.addParam(self.SECTION_TABS, self.TABS_MARGIN_VERTICAL, 5)

    @property
    def colorBackground(self):
        return self.get(self.SECTION_GENERAL, self.BACKGROUND_COLOR)

    @property
    def colorBackgroundSelected(self):
        return self.get(self.SECTION_GENERAL, self.SELECTION_COLOR)

    @property
    def colorText(self):
        return self.get(self.SECTION_GENERAL, self.TEXT_COLOR)

    @property
    def colorTextSelected(self):
        return self.get(self.SECTION_GENERAL, self.SELECTION_TEXT_COLOR)

    @property
    def changed(self):
        return len(self._changed_sections) != 0

    @property
    def changed_sections(self) -> Set[str]:
        return self._changed_sections

    def addParam(self, section: str, param: str, defaultValue: Any):
        fullName = self._getFullName(section, param)
        self._data[fullName] = (defaultValue, defaultValue)

    def _getFullName(self, section: str, param: str) -> str:
        return f"{section}/{param}"

    def get(self, section: str, param: str) -> Any:
        fullName = self._getFullName(section, param)
        data = self._data[fullName]
        val = data[0]
        default_value = data[1]
        return self._selectVal(val, default_value)

    def _selectVal(self, value, defaultValue):
        return (
            defaultValue if value is None or value == "" or value == "None" else value
        )

    def getDefaults(self, section: str, param: str) -> Any:
        fullName = self._getFullName(section, param)
        return self._data[fullName][1]

    def set(self, section: str, param: str, val: Any):
        fullName = self._getFullName(section, param)
        default_value = self._data[fullName][1]
        old_val = self.get(section, param)
        if old_val != self._selectVal(val, default_value):
            self._data[fullName] = (val, default_value)
            self._changed_sections.add(section)

    def clear(self):
        self._changed_sections.clear()
        self.onThemeChanged.clear()

    def sendEvent(self):
        if self.changed:
            logger.debug("Theme changed")
            self.onThemeChanged(ThemeChangedParams(self, self._changed_sections.copy()))
            self._changed_sections.clear()


class ThemeChangedParams:
    """
    Parameters for onThemeChanged event
    """

    def __init__(self, theme: Theme, changed_sections: Set[str]) -> None:
        self.theme = theme
        self.changed_sections = changed_sections
