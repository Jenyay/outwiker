import wx

from typing import Dict, Optional, Tuple
from outwiker.core.event import Event


class Theme:
    # Sections
    SECTION_GENERAL = "General"
    SECTION_TREE = "Tree"
    SECTION_RENDER = "Render"
    SECTION_EDITOR = "Editor"
    SECTION_HTML_EDITOR = "HtmlEditor"
    SECTION_WIKI_EDITOR = "WikiEditor"

    # General section
    GENERAL_BACKGROUND_COLOR = "MainBackgroundColor"
    GENERAL_FONT_COLOR = "MainFontColor"
    GENERAL_HYPERLINK_COLOR = "HyperlinkColor"

    # Tree section
    TREE_SELECTION_COLOR = "SelectionColor"
    TREE_SELECTION_FONT_COLOR = "SelectionFontColor"
    TREE_HIGHLIGHTING_COLOR = "HighlightingColor"
    TREE_HIGHLIGHTING_FONT_COLOR = "HighlightingFontColor"

    # Render
    RENDER_STYLES = "Styles"

    # Editor
    EDITOR_BACKGROUND_COLOR = "BackgroundColor"
    EDITOR_FONT_COLOR = "FontColor"
    EDITOR_SELECTION_COLOR = "SelectionColor"
    EDITOR_FIELD_COLOR = "FieldColor"

    def __init__(self):
        self._data: Dict[str, Tuple[Optional[str], str]] = {}
        self._initDefaults()

        # Event occurs after theme changing
        # Parameters:
        #    params - instance of the onThemeChangedParams class
        self.onThemeChanged = Event()

    def _initDefaults(self):
        self.addParam(self.SECTION_GENERAL, self.GENERAL_BACKGROUND_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_GENERAL, self.GENERAL_FONT_COLOR, "#000000")
        self.addParam(self.SECTION_GENERAL, self.GENERAL_HYPERLINK_COLOR, "#0000FF")

        self.addParam(self.SECTION_TREE, self.TREE_SELECTION_COLOR, "#0000FF")
        self.addParam(self.SECTION_TREE, self.TREE_SELECTION_FONT_COLOR, "#FFFFFF")
        self.addParam(self.SECTION_TREE, self.TREE_HIGHLIGHTING_COLOR, "#E1EFFA")
        self.addParam(self.SECTION_TREE, self.TREE_HIGHLIGHTING_FONT_COLOR, "#000000")

    def addParam(self, section: str, param: str, defaultValue: str):
        fullName = self._getFullName(section, param)
        self._data[fullName] = (defaultValue, defaultValue)

    def _getFullName(self, section: str, param: str) -> str:
        return f"{section}/{param}"

    def get(self, section: str, param: str) -> str:
        fullName = self._getFullName(section, param)
        data = self._data[fullName]
        val = data[0]
        default_value = data[1]
        return self._selectVal(val, default_value)

    def _selectVal(self, value, defaultValue):
        return (
            defaultValue if value is None or value == "" or value == "None" else value
        )

    def set(self, section: str, param: str, val: str):
        fullName = self._getFullName(section, param)
        default_value = self._data[fullName][1]
        self._data[fullName] = (val, default_value)

    def clear(self):
        self.onThemeChanged.clear()

    def loadSystemParams(self):
        self.addParam(
            self.SECTION_TREE,
            self.TREE_SELECTION_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )
        self.addParam(
            self.SECTION_TREE,
            self.TREE_SELECTION_FONT_COLOR,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT).GetAsString(
                wx.C2S_HTML_SYNTAX
            ),
        )

    def loadFromConfig(self, config):
        pass

    def sendEvent(self):
        self.onThemeChanged(self)


class onThemeChangedParams:
    """
    Parameters for onThemeChanged event
    """

    def __init__(self, theme: Theme) -> None:
        self.theme = theme
