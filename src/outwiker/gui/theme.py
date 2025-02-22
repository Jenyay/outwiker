from typing import Any, Dict, Tuple
import logging

import wx

from outwiker.core.event import Event
from outwiker.gui.guiconfig import MainWindowConfig


logger = logging.getLogger("outwiker.gui.theme")


class Theme:
    # Sections
    SECTION_GENERAL = "General"
    SECTION_TREE = "Tree"
    SECTION_RENDER = "Render"
    SECTION_EDITOR = "Editor"
    SECTION_HTML_EDITOR = "HtmlEditor"
    SECTION_WIKI_EDITOR = "WikiEditor"

    # General section
    BACKGROUND_COLOR = "BackgroundColor"
    TEXT_COLOR = "FontColor"
    HYPERLINK_COLOR = "HyperlinkColor"
    SELECTION_COLOR = "SelectionColor"
    SELECTION_FONT_COLOR = "SelectionFontColor"

    # Tree section
    HIGHLIGHTING_COLOR = "HighlightingColor"
    HIGHLIGHTING_FONT_COLOR = "HighlightingFontColor"

    # Render
    # RENDER_STYLES = "Styles"

    # Editor
    # FIELD_COLOR = "FieldColor"

    def __init__(self):
        self._data: Dict[str, Tuple[Any, Any]] = {}
        self._initDefaults()
        self._changed = False

        # Event occurs after theme changing
        # Parameters:
        #    params - instance of the onThemeChangedParams class
        self.onThemeChanged = Event()

    def _initDefaults(self):
        self.addParam(self.SECTION_GENERAL, self.BACKGROUND_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_GENERAL, self.TEXT_COLOR, "#000000")
        self.addParam(self.SECTION_GENERAL, self.HYPERLINK_COLOR, "#0000FF")
        self.addParam(self.SECTION_GENERAL, self.SELECTION_COLOR, "#0000FF")
        self.addParam(self.SECTION_GENERAL, self.SELECTION_FONT_COLOR, "#FFFFFF")

        self.addParam(self.SECTION_TREE, self.SELECTION_COLOR, "#0000FF")
        self.addParam(self.SECTION_TREE, self.SELECTION_FONT_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_TREE, self.HIGHLIGHTING_COLOR, "#E1EFFA")
        self.addParam(self.SECTION_TREE, self.HIGHLIGHTING_FONT_COLOR, "#000000")

    @property
    def changed(self):
        return self._changed

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
            self._changed = True

    def clear(self):
        self._changed = False
        self.onThemeChanged.clear()

    def loadSystemParams(self):
        self.addParam(
            self.SECTION_GENERAL,
            self.SELECTION_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self.addParam(
            self.SECTION_TREE,
            self.SELECTION_COLOR,
            self.getDefaults(self.SECTION_GENERAL, self.SELECTION_COLOR),
        )

        self.addParam(
            self.SECTION_GENERAL,
            self.SELECTION_FONT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

        self.addParam(
            self.SECTION_TREE,
            self.SELECTION_FONT_COLOR,
            self.getDefaults(self.SECTION_GENERAL, self.SELECTION_FONT_COLOR),
        )

    def loadFromConfig(self, config):
        mainWindowConfig = MainWindowConfig(config)
        self.set(self.SECTION_GENERAL, self.BACKGROUND_COLOR, mainWindowConfig.mainPanesBackgroundColor.value)
        self.set(self.SECTION_GENERAL, self.TEXT_COLOR, mainWindowConfig.mainPanesTextColor.value)

    def sendEvent(self):
        if self._changed:
            logger.debug("Theme changed")
            self.onThemeChanged(self)
            self._changed = False


class onThemeChangedParams:
    """
    Parameters for onThemeChanged event
    """

    def __init__(self, theme: Theme) -> None:
        self.theme = theme
