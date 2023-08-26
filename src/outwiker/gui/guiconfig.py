# -*- coding: utf-8 -*-

from typing import Tuple

import wx

from outwiker.core.config import (
    StringOption,
    BooleanOption,
    IntegerOption,
    ListOption,
    StcStyleOption,
)
from outwiker.gui.defines import TAGS_CLOUD_MODE_CONTINUOUS
from outwiker.gui.stcstyle import StcStyle


class GuiConfig:
    SECTION = "GUI"

    def __init__(self, config):
        self.config = config
        self._wnd_width_suffix = "width"
        self._wnd_height_suffix = "height"

    def saveWindowSize(self, prefix: str, width: int, height: int):
        width_option, height_option = self._get_options(prefix, 0, 0)
        if width > 0:
            width_option.value = width

        if height > 0:
            height_option.value = height

    def loadWindowSize(
        self, prefix: str, width_default: int, height_default: int
    ) -> Tuple[int, int]:
        width_option, height_option = self._get_options(
            prefix, width_default, height_default
        )
        return (width_option.value, height_option.value)

    def _get_options(
        self, prefix: str, width_default: int, height_default: int
    ) -> Tuple[IntegerOption, IntegerOption]:
        width_param_name = "{}_{}".format(prefix, self._wnd_width_suffix)
        height_param_name = "{}_{}".format(prefix, self._wnd_height_suffix)

        width_option = IntegerOption(
            self.config, self.SECTION, width_param_name, width_default
        )

        height_option = IntegerOption(
            self.config, self.SECTION, height_param_name, height_default
        )

        return (width_option, height_option)


class GeneralGuiConfig:
    """
    Класс для хранения основных настроек
    """

    GENERAL_SECTION = "General"
    RECENT_SECTION = "RecentWiki"

    ASK_BEFORE_EXIT_PARAM = "AskBeforeExit"
    ASK_BEFORE_EXIT_DEFAULT = False

    AUTOSAVE_INTERVAL_PARAM = "AutosaveInterval"
    AUTOSAVE_INTERVAL_DEFAULT = 3

    RECENT_WIKI_COUNT_PARAM = "maxcount"
    RECENT_WIKI_COUNT_DEFAULT = 5

    RECENT_ICONS_COUNT_PARAM = "recenticonscount"
    RECENT_ICONS_COUNT_DEFAULT = 30

    RECENT_AUTOOPEN_PARAM = "AutoOpen"
    RECENT_AUTOOPEN_DEFAULT = True

    DATETIME_FORMAT_PARAM = "DateTimeFormat"
    DATETIME_FORMAT_DEFAULT = "%c"

    PAGE_TITLE_TEMPLATE_PARAM = "PageTitleTemplate"
    PAGE_TITLE_TEMPLATE_DEFAULT = ""

    # Последний используемый формат представления даты
    RECENT_DATETIME_FORMAT_PARAM = "RecentDateTimeFormat"

    # Default tab for page(editor / preview / recent used)
    PAGE_TAB_RECENT = 0
    PAGE_TAB_CODE = 1
    PAGE_TAB_RESULT = 2

    PAGE_TAB_PARAM = "PageTab"

    TABLE_COLS_COUNT = "TableColsCount"
    TABLE_COLS_COUNT_DEFAULT = 1

    DEBUG_PARAM = "debug"
    DEBUG_DEFAULT = False

    RECENT_TEXT_COLORS_PARAM = "RecentTextColors"
    RECENT_TEXT_COLORS_DEFAULT = "#000000;#FFFFFF;#ff0000;#00ff00;#0000ff;#8a2be2;#7fff00;#d2691e;#6495ed;#dc143c;#00ffff;#a9a9a9;#ff8c00;#ff1493;#ffd700;#adff2f;#ffff00".split(
        ";"
    )

    RECENT_BACKGROUND_COLORS_PARAM = "RecentBackgroundColors"
    RECENT_BACKGROUND_COLORS_DEFAULT = "#000000;#FFFFFF;#ff0000;#00ff00;#0000ff;#8a2be2;#7fff00;#d2691e;#6495ed;#dc143c;#00ffff;#a9a9a9;#ff8c00;#ff1493;#ffd700;#adff2f;#ffff00".split(
        ";"
    )

    # Toaster delay in milliseconds
    TOASTER_DELAY_PARAM = "ToasterDelay"
    TOASTER_DELAY_DEFAULT = 7000

    # Headers for bookmarks page list in RootPagePanel
    BOOKMARKS_HEADERS_PARAM = "BookmarksHeaders"
    BOOKMARKS_HEADERS_DEFAULT = ""

    def __init__(self, config):
        self.config = config

        # Спрашивать подтверждение выхода?
        self.askBeforeExit = BooleanOption(
            self.config,
            self.GENERAL_SECTION,
            self.ASK_BEFORE_EXIT_PARAM,
            self.ASK_BEFORE_EXIT_DEFAULT,
        )

        # Интервал, через которое происходит автосохранение страницы.
        # Если значение <= 0, значит автосохранение отключено
        self.autosaveInterval = IntegerOption(
            self.config,
            self.GENERAL_SECTION,
            self.AUTOSAVE_INTERVAL_PARAM,
            self.AUTOSAVE_INTERVAL_DEFAULT,
        )

        # Количество последних открытых вики
        self.historyLength = IntegerOption(
            self.config,
            self.RECENT_SECTION,
            self.RECENT_WIKI_COUNT_PARAM,
            self.RECENT_WIKI_COUNT_DEFAULT,
        )

        # Recently icons history length
        self.iconsHistoryLength = IntegerOption(
            self.config,
            self.RECENT_SECTION,
            self.RECENT_ICONS_COUNT_PARAM,
            self.RECENT_ICONS_COUNT_DEFAULT,
        )

        # Открывать последнуюю открытую вики при старте?
        self.autoopen = BooleanOption(
            self.config,
            self.RECENT_SECTION,
            self.RECENT_AUTOOPEN_PARAM,
            self.RECENT_AUTOOPEN_DEFAULT,
        )

        # Формат для представления даты и времени модификиции страниц
        self.dateTimeFormat = StringOption(
            self.config,
            self.GENERAL_SECTION,
            self.DATETIME_FORMAT_PARAM,
            self.DATETIME_FORMAT_DEFAULT,
        )

        self.pageTitleTemplate = StringOption(
            self.config,
            self.GENERAL_SECTION,
            self.PAGE_TITLE_TEMPLATE_PARAM,
            self.PAGE_TITLE_TEMPLATE_DEFAULT,
        )

        # Последний используемый формат для представления даты и времени
        # модификиции страниц
        self.recentDateTimeFormat = StringOption(
            self.config,
            self.GENERAL_SECTION,
            self.RECENT_DATETIME_FORMAT_PARAM,
            self.dateTimeFormat.value,
        )

        # Default tab for page(editor / preview / recent used)
        self.pageTab = IntegerOption(
            self.config, self.GENERAL_SECTION, self.PAGE_TAB_PARAM, self.PAGE_TAB_RECENT
        )

        # Default columns count in table dialog
        self.tableColsCount = IntegerOption(
            self.config,
            self.GENERAL_SECTION,
            self.TABLE_COLS_COUNT,
            self.TABLE_COLS_COUNT_DEFAULT,
        )

        self.recentTextColors = ListOption(
            self.config,
            self.GENERAL_SECTION,
            self.RECENT_TEXT_COLORS_PARAM,
            self.RECENT_TEXT_COLORS_DEFAULT,
            separator=";",
        )

        self.recentBackgroundColors = ListOption(
            self.config,
            self.GENERAL_SECTION,
            self.RECENT_BACKGROUND_COLORS_PARAM,
            self.RECENT_BACKGROUND_COLORS_DEFAULT,
            separator=";",
        )

        self.debug = BooleanOption(
            self.config, self.GENERAL_SECTION, self.DEBUG_PARAM, self.DEBUG_DEFAULT
        )

        self.toasterDelay = IntegerOption(
            self.config,
            self.GENERAL_SECTION,
            self.TOASTER_DELAY_PARAM,
            self.TOASTER_DELAY_DEFAULT,
        )

        self.bookmarksHeaders = StringOption(
            self.config,
            self.GENERAL_SECTION,
            self.BOOKMARKS_HEADERS_PARAM,
            self.BOOKMARKS_HEADERS_DEFAULT,
        )


class PluginsConfig:
    """
    Класс для хранения настроек, связанных с плагинами
    """

    PLUGINS_SECTION = "Plugins"
    DISABLED_PARAM = "Disabled"

    def __init__(self, config):
        self.config = config

        self.disabledPlugins = ListOption(
            self.config,
            PluginsConfig.PLUGINS_SECTION,
            PluginsConfig.DISABLED_PARAM,
            [],
            separator=";",
        )


class TrayConfig:
    """
    Класс для хранения настроек, связанных с иконками в трее
    """

    MINIMIZE_TO_TRAY_PARAM = "MinimizeToTray"
    MINIMIZE_TO_TRAY_DEFAULT = 0

    CLOSE_BUTTON_ACTION_PARAM = "CloseButtonAction"
    CLOSE_BUTTON_ACTION_DEFAULT = 0

    START_ICONIZED_PARAM = "StartIconized"
    START_ICONIZED_DEFAULT = False

    ALWAYS_SHOW_TRAY_ICON_PARAM = "AlwaysShowTrayIcon"
    ALWAYS_SHOW_TRAY_ICON_DEFAULT = False

    MINIMIZE_ON_CLOSE_PARAM = "MinimizeOnClose"
    MINIMIZE_ON_CLOSE_DEFAULT = False

    def __init__(self, config):
        self.config = config

        # Minimize button action
        self.minimizeToTray = IntegerOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.MINIMIZE_TO_TRAY_PARAM,
            TrayConfig.MINIMIZE_TO_TRAY_DEFAULT,
        )

        # Close button action
        self.closeButtonAction = IntegerOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.CLOSE_BUTTON_ACTION_PARAM,
            TrayConfig.CLOSE_BUTTON_ACTION_DEFAULT,
        )

        # Execute minimized?
        self.startIconized = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.START_ICONIZED_PARAM,
            TrayConfig.START_ICONIZED_DEFAULT,
        )

        # Всегда показывать иконку в трее?
        self.alwaysShowTrayIcon = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.ALWAYS_SHOW_TRAY_ICON_PARAM,
            TrayConfig.ALWAYS_SHOW_TRAY_ICON_DEFAULT,
        )

        # Сворачивать окно программы при закрытии главного окна
        self.minimizeOnClose = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.MINIMIZE_ON_CLOSE_PARAM,
            TrayConfig.MINIMIZE_ON_CLOSE_DEFAULT,
        )


class EditorConfig:
    """
    Класс для хранения настроек редактора
    """

    FONT_SECTION = "Font"

    SHOW_LINE_NUMBERS_SECTION = "ShowLineNumbers"
    SHOW_LINE_NUMBERS_DEFAULT = False

    TAB_WIDTH_SECTION = "TabWidth"
    TAB_WIDTH_DEFAULT = 4

    FONT_SIZE_SECTION = "size"
    FONT_SIZE_DEFAULT = 10

    FONT_NAME_SECTION = "FaceName"
    FONT_NAME_DEFAULT = ""

    FONT_BOLD_SECTION = "bold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = "italic"
    FONT_ITALIC_DEFAULT = False

    # Поведение клавиш Home / End.
    HOME_END_OF_LINE = 0
    HOME_END_OF_PARAGRAPH = 1

    HOME_END_KEYS_SECTION = "HomeEndKeys"
    HOME_END_KEYS_DEFAULT = HOME_END_OF_LINE

    # Цвет шрифта
    FONT_COLOR_SECTION = "FontColor"
    FONT_COLOR_DEFAULT = "#000000"

    # Цвет фона
    BACK_COLOR_SECTION = "BackColor"
    BACK_COLOR_DEFAULT = "#FFFFFF"

    # Selected text background color
    SEL_BACK_COLOR_SECTION = "SelBackColor"
    SEL_BACK_COLOR_DEFAULT = "#C0C0C0"

    # Margin background color
    MARGIN_BACK_COLOR_SECTION = "MarginBackColor"
    MARGIN_BACK_COLOR_DEFAULT = "#C4C4C4"

    # Spell checker
    SPELL_DICTS_SECTION = "dictionaries"
    SPELL_DICT_DEFAULT = "en_US, ru_RU, ru_RU_yo, uk_UA"

    SPELL_ENABLE_SECTION = "SpellChecking"
    SPELL_ENABLE_DEFAULT = True

    SPELL_SKIP_DIGITS_SECTION = "SpellSkipDigits"
    SPELL_SKIP_DIGITS_DEFAULT = True

    def __init__(self, config):
        self.config = config

        # Показывать номера строк в редакторе?
        self.lineNumbers = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SHOW_LINE_NUMBERS_SECTION,
            EditorConfig.SHOW_LINE_NUMBERS_DEFAULT,
        )

        # Размер табуляции
        self.tabWidth = IntegerOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.TAB_WIDTH_SECTION,
            EditorConfig.TAB_WIDTH_DEFAULT,
        )

        # Размер шрифта
        self.fontSize = IntegerOption(
            self.config,
            EditorConfig.FONT_SECTION,
            EditorConfig.FONT_SIZE_SECTION,
            EditorConfig.FONT_SIZE_DEFAULT,
        )

        # Начертание шрифта
        self.fontName = StringOption(
            self.config,
            EditorConfig.FONT_SECTION,
            EditorConfig.FONT_NAME_SECTION,
            EditorConfig.FONT_NAME_DEFAULT,
        )

        self.fontIsBold = BooleanOption(
            self.config,
            EditorConfig.FONT_SECTION,
            EditorConfig.FONT_BOLD_SECTION,
            EditorConfig.FONT_BOLD_DEFAULT,
        )

        self.fontIsItalic = BooleanOption(
            self.config,
            EditorConfig.FONT_SECTION,
            EditorConfig.FONT_ITALIC_SECTION,
            EditorConfig.FONT_ITALIC_DEFAULT,
        )

        # Поведение клавиш Home / End
        self.homeEndKeys = IntegerOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.HOME_END_KEYS_SECTION,
            EditorConfig.HOME_END_KEYS_DEFAULT,
        )

        self.fontColor = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.FONT_COLOR_SECTION,
            EditorConfig.FONT_COLOR_DEFAULT,
        )

        self.backColor = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.BACK_COLOR_SECTION,
            EditorConfig.BACK_COLOR_DEFAULT,
        )

        self.selBackColor = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SEL_BACK_COLOR_SECTION,
            EditorConfig.SEL_BACK_COLOR_DEFAULT,
        )

        self.marginBackColor = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.MARGIN_BACK_COLOR_SECTION,
            EditorConfig.MARGIN_BACK_COLOR_DEFAULT,
        )

        self.spellCheckerDicts = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SPELL_DICTS_SECTION,
            EditorConfig.SPELL_DICT_DEFAULT,
        )

        self.spellEnabled = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SPELL_ENABLE_SECTION,
            EditorConfig.SPELL_ENABLE_DEFAULT,
        )

        self.spellSkipDigits = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SPELL_SKIP_DIGITS_SECTION,
            EditorConfig.SPELL_SKIP_DIGITS_DEFAULT,
        )


class HtmlEditorStylesConfig:
    """
    Класс для хранения настроек стилей редактора HTML
    """

    HTML_STYLES_SECTION = "EditorStyles"

    STYLE_TAG_SECTION = "tag"
    STYLE_TAG_DEFAULT = StcStyle.parse("fore:#000080,bold")

    STYLE_TAG_UNKNOWN_SECTION = "tag_unknown"
    STYLE_TAG_UNKNOWN_DEFAULT = StcStyle.parse("fore:#FF0000")

    STYLE_ATTRIBUTE_SECTION = "attribute"
    STYLE_ATTRIBUTE_DEFAULT = StcStyle.parse("fore:#008080")

    STYLE_ATTRIBUTE_UNKNOWN_SECTION = "attribute_unknown"
    STYLE_ATTRIBUTE_UNKNOWN_DEFAULT = StcStyle.parse("fore:#FF0000")

    STYLE_NUMBER_SECTION = "number"
    STYLE_NUMBER_DEFAULT = StcStyle.parse("fore:#000000")

    STYLE_STRING_SECTION = "string"
    STYLE_STRING_DEFAULT = StcStyle.parse("fore:#0000FF")

    STYLE_COMMENT_SECTION = "comment"
    STYLE_COMMENT_DEFAULT = StcStyle.parse("fore:#12B535")

    def __init__(self, config):
        self.config = config

        self.tag = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_DEFAULT,
        )

        self.tagUnknown = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_UNKNOWN_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_UNKNOWN_DEFAULT,
        )

        self.attribute = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_DEFAULT,
        )

        self.attributeUnknown = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_UNKNOWN_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_UNKNOWN_DEFAULT,
        )

        self.number = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_NUMBER_SECTION,
            HtmlEditorStylesConfig.STYLE_NUMBER_DEFAULT,
        )

        self.string = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_STRING_SECTION,
            HtmlEditorStylesConfig.STYLE_STRING_DEFAULT,
        )

        self.comment = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_COMMENT_SECTION,
            HtmlEditorStylesConfig.STYLE_COMMENT_DEFAULT,
        )


class HtmlRenderConfig:
    """
    Класс для хранения настроек HTML-рендера
    """

    # Название секции в конфиге для настроек HTML
    HTML_SECTION = "HTML"

    FONT_FACE_NAME_PARAM = "FontFaceName"
    FONT_NAME_DEFAULT = "Verdana"

    FONT_SIZE_PARAM = "FontSize"
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_PARAM = "FontBold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_PARAM = "FontItalic"
    FONT_ITALIC_DEFAULT = False

    USER_STYLE_PARAM = "UserStyle"
    USER_STYLE_DEFAULT = ""

    HTML_IMPROVER_PARAM = "HtmlImprover"
    HTML_IMPROVER_DEFAULT = "brimprover"

    def __init__(self, config):
        self.config = config

        self.fontSize = IntegerOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_SIZE_PARAM,
            HtmlRenderConfig.FONT_SIZE_DEFAULT,
        )

        self.fontName = StringOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_FACE_NAME_PARAM,
            HtmlRenderConfig.FONT_NAME_DEFAULT,
        )

        self.fontIsBold = BooleanOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_BOLD_PARAM,
            HtmlRenderConfig.FONT_BOLD_DEFAULT,
        )

        self.fontIsItalic = BooleanOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_ITALIC_PARAM,
            HtmlRenderConfig.FONT_ITALIC_DEFAULT,
        )

        self.userStyle = StringOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.USER_STYLE_PARAM,
            HtmlRenderConfig.USER_STYLE_DEFAULT,
        )

        self.HTMLImprover = StringOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.HTML_IMPROVER_PARAM,
            HtmlRenderConfig.HTML_IMPROVER_DEFAULT,
        )


class TextPrintConfig:
    """
    Класс для хранения настроек печати текста
    """

    PRINT_SECTION = "Print"

    FONT_NAME_SECTION = "FontFaceName"
    FONT_NAME_DEFAULT = "Arial"

    FONT_SIZE_SECTION = "FontSize"
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_SECTION = "FontBold"
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = "FontItalic"
    FONT_ITALIC_DEFAULT = False

    PAPPER_SIZE_SECTION = "PaperId"
    PAPPER_SIZE_DEFAULT = wx.PAPER_A4

    MARGIN_TOP_SECTION = "MarginTop"
    MARGIN_TOP_DEFAULT = 20

    MARGIN_BOTTOM_SECTION = "MarginBottom"
    MARGIN_BOTTOM_DEFAULT = 20

    MARGIN_LEFT_SECTION = "MarginLeft"
    MARGIN_LEFT_DEFAULT = 20

    MARGIN_RIGHT_SECTION = "MarginRight"
    MARGIN_RIGHT_DEFAULT = 20

    def __init__(self, config):
        self.config = config

        # Настройки шрифта
        self.fontName = StringOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.FONT_NAME_SECTION,
            TextPrintConfig.FONT_NAME_DEFAULT,
        )

        self.fontSize = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.FONT_SIZE_SECTION,
            TextPrintConfig.FONT_SIZE_DEFAULT,
        )

        self.fontIsBold = BooleanOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.FONT_BOLD_SECTION,
            TextPrintConfig.FONT_BOLD_DEFAULT,
        )

        self.fontIsItalic = BooleanOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.FONT_ITALIC_SECTION,
            TextPrintConfig.FONT_ITALIC_DEFAULT,
        )

        self.paperId = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.PAPPER_SIZE_SECTION,
            TextPrintConfig.PAPPER_SIZE_DEFAULT,
        )

        self.marginTop = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.MARGIN_TOP_SECTION,
            TextPrintConfig.MARGIN_TOP_DEFAULT,
        )

        self.marginBottom = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.MARGIN_BOTTOM_SECTION,
            TextPrintConfig.MARGIN_BOTTOM_DEFAULT,
        )

        self.marginLeft = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.MARGIN_LEFT_SECTION,
            TextPrintConfig.MARGIN_LEFT_DEFAULT,
        )

        self.marginRight = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.MARGIN_RIGHT_SECTION,
            TextPrintConfig.MARGIN_RIGHT_DEFAULT,
        )


class MainWindowConfig:
    """
    Класс для хранения настроек главного окна
    """

    MAIN_WINDOW_SECTION = "MainWindow"

    TITLE_FORMAT_SECTION = "Title"
    TITLE_FORMAT_DEFAULT = "{page} - {file} - OutWiker"

    WIDTH_SECTION = "width"
    WIDTH_DEFAULT = 800

    HEIGHT_SECTION = "height"
    HEIGHT_DEFAULT = 680

    XPOS_SECTION = "xpos"
    XPOS_DEFAULT = 0

    YPOS_SECTION = "ypos"
    YPOS_DEFAULT = 0

    FULLSCREEN_SECTION = "fullscreen"
    FULLSCREEN_DEFAULT = False

    MAXIMIZED_SECTION = "maximized"
    MAXIMIZED_DEFAULT = False

    # Размер области в статусной панели для показа даты изменения текущей
    # страницы
    DATETIME_STATUS_WIDTH_SECTION = "datetime_status_width"
    DATETIME_STATUS_WIDTH_DEFAULT = 250

    STATUSBAR_VISIBLE_SECTION = "statusbar_visible"
    STATUSBAR_VISIBLE_DEFAULT = True

    MAIN_PANES_BACKGROUND_COLOR_SECTION = "main_panes_background_color"
    MAIN_PANES_BACKGROUND_COLOR_DEFAULT = "#ffffff"

    MAIN_PANES_TEXT_COLOR_SECTION = "main_panes_text_color"
    MAIN_PANES_TEXT_COLOR_DEFAULT = "#000000"

    def __init__(self, config):
        self.config = config

        self.titleFormat = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.TITLE_FORMAT_SECTION,
            self.TITLE_FORMAT_DEFAULT,
        )

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT,
        )

        self.xPos = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.XPOS_SECTION,
            self.XPOS_DEFAULT,
        )

        self.yPos = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.YPOS_SECTION,
            self.YPOS_DEFAULT,
        )

        self.fullscreen = BooleanOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.FULLSCREEN_SECTION,
            self.FULLSCREEN_DEFAULT,
        )

        self.maximized = BooleanOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.MAXIMIZED_SECTION,
            self.MAXIMIZED_DEFAULT,
        )

        self.datetimeStatusWidth = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.DATETIME_STATUS_WIDTH_SECTION,
            self.DATETIME_STATUS_WIDTH_DEFAULT,
        )

        self.statusbar_visible = BooleanOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.STATUSBAR_VISIBLE_SECTION,
            self.STATUSBAR_VISIBLE_DEFAULT,
        )

        self.mainPanesBackgroundColor = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.MAIN_PANES_BACKGROUND_COLOR_SECTION,
            self.MAIN_PANES_BACKGROUND_COLOR_DEFAULT,
        )

        self.mainPanesTextColor = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.MAIN_PANES_TEXT_COLOR_SECTION,
            self.MAIN_PANES_TEXT_COLOR_DEFAULT,
        )


class TreeConfig:
    """
    Класс для хранения настроек панели с деревом
    """

    WIDTH_SECTION = "TreeWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = "TreeHeight"
    HEIGHT_DEFAULT = 250

    PANE_OPTIONS_SECTION = "TreePane"
    PANE_OPTIONS_DEFAULT = ""

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            TreeConfig.WIDTH_SECTION,
            TreeConfig.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            TreeConfig.HEIGHT_SECTION,
            TreeConfig.HEIGHT_DEFAULT,
        )

        # Параметры панели с деревом
        self.pane = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            TreeConfig.PANE_OPTIONS_SECTION,
            TreeConfig.PANE_OPTIONS_DEFAULT,
        )


class AttachConfig:
    """
    Класс для хранения настроек панели с вложенными файлами
    """

    WIDTH_SECTION = "AttachesWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = "AttachesHeight"
    HEIGHT_DEFAULT = 150

    PANE_OPTIONS_SECTION = "AttachesPane"
    PANE_OPTIONS_DEFAULT = ""

    ACTION_INSERT_LINK = 0
    ACTION_OPEN = 1

    DOUBLE_CLICK_ACTION_PARAM = "AttachDoubleClickAction"
    DOUBLE_CLICK_ACTION_DEFAULT = ACTION_OPEN

    SHOW_HIDDEN_DIRS_PARAM = "ShowHiddenDirs"
    SHOW_HIDDEN_DIRS_DEFAULT = False

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT,
        )

        self.pane = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.PANE_OPTIONS_SECTION,
            self.PANE_OPTIONS_DEFAULT,
        )

        self.doubleClickAction = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.DOUBLE_CLICK_ACTION_PARAM,
            self.DOUBLE_CLICK_ACTION_DEFAULT,
        )

        self.showHiddenDirs = BooleanOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.SHOW_HIDDEN_DIRS_PARAM,
            self.SHOW_HIDDEN_DIRS_DEFAULT,
        )


class TagsCloudConfig:
    """
    Класс для хранения настроек панели с облагом тегов
    """

    WIDTH_SECTION = "TagsCloudWidth"
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = "TagsCloudHeight"
    HEIGHT_DEFAULT = 170

    PANE_OPTIONS_SECTION = "TagsCloudPane"
    PANE_OPTIONS_DEFAULT = ""

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT,
        )

        # Параметры панели с деревом
        self.pane = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.PANE_OPTIONS_SECTION,
            self.PANE_OPTIONS_DEFAULT,
        )


class PageDialogConfig:
    WIDTH_SECTION = "PageDialogWidth"
    WIDTH_DEFAULT = 500

    HEIGHT_SECTION = "PageDialogHeight"
    HEIGHT_DEFAULT = 350

    # Последний используемый стиль
    RECENT_STYLE_SECTION = "RecentStyle"
    RECENT_STYLE_DEFAULT = ""

    RECENT_CREATED_PAGE_TYPE_PARAM = "RecentCreatedPageType"
    RECENT_CREATED_PAGE_TYPE_DEFAULT = "wiki"

    RECENT_NEW_PAGE_ORDER_CALCULATOR_PARAM = "PageOrderCalculator"
    RECENT_NEW_PAGE_ORDER_CALCULATOR_DEFAULT = 1

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT,
        )

        self.recentStyle = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            self.RECENT_STYLE_SECTION,
            self.RECENT_STYLE_DEFAULT,
        )

        self.recentCreatedPageType = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            self.RECENT_CREATED_PAGE_TYPE_PARAM,
            self.RECENT_CREATED_PAGE_TYPE_DEFAULT,
        )

        self.newPageOrderCalculator = IntegerOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            self.RECENT_NEW_PAGE_ORDER_CALCULATOR_PARAM,
            self.RECENT_NEW_PAGE_ORDER_CALCULATOR_DEFAULT,
        )


class PrefDialogConfig:
    WIDTH_SECTION = "PrefDialogWidth"
    WIDTH_DEFAULT = 800

    HEIGHT_SECTION = "PrefDialogHeight"
    HEIGHT_DEFAULT = 500

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT,
        )

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT,
        )


class TagsConfig:
    """
    Options for tags and tags cloud
    """

    SECTION = "Tags"

    POPUP_HEADERS_SECTION = "PopupHeaders"
    POPUP_HEADERS_DEFAULT = ""

    POPUP_WIDTH_SECTION = "TagsPopupWidth"
    POPUP_WIDTH_DEFAULT = 825

    POPUP_HEIGHT_SECTION = "TagsPopupHeight"
    POPUP_HEIGHT_DEFAULT = 200

    MIN_FONT_SIZE_SECTION = "MinFontSize"
    MIN_FONT_SIZE_DEFAULT = 8

    MAX_FONT_SIZE_SECTION = "MaxFontSize"
    MAX_FONT_SIZE_DEFAULT = 16

    TAGS_CLOUD_MODE_SECTION = "tagsCloudMode"
    TAGS_CLOUD_MODE_DEFAULT = TAGS_CLOUD_MODE_CONTINUOUS

    def __init__(self, config):
        self.config = config

        self.popupHeaders = StringOption(
            self.config,
            self.SECTION,
            self.POPUP_HEADERS_SECTION,
            self.POPUP_HEADERS_DEFAULT,
        )

        self.popupWidth = IntegerOption(
            self.config,
            self.SECTION,
            self.POPUP_WIDTH_SECTION,
            self.POPUP_WIDTH_DEFAULT,
        )

        self.popupHeight = IntegerOption(
            self.config,
            self.SECTION,
            self.POPUP_HEIGHT_SECTION,
            self.POPUP_HEIGHT_DEFAULT,
        )

        self.minFontSize = IntegerOption(
            self.config,
            self.SECTION,
            self.MIN_FONT_SIZE_SECTION,
            self.MIN_FONT_SIZE_DEFAULT,
        )

        self.maxFontSize = IntegerOption(
            self.config,
            self.SECTION,
            self.MAX_FONT_SIZE_SECTION,
            self.MAX_FONT_SIZE_DEFAULT,
        )

        self.tagsCloudMode = StringOption(
            self.config,
            self.SECTION,
            self.TAGS_CLOUD_MODE_SECTION,
            self.TAGS_CLOUD_MODE_DEFAULT,
        )
