# -*- coding: utf-8 -*-

import wx

from outwiker.core.config import (StringOption, BooleanOption, IntegerOption,
                                  ListOption, StcStyleOption)
from outwiker.gui.stcstyle import StcStyle


class GeneralGuiConfig(object):
    '''
    Класс для хранения основных настроек
    '''
    GENERAL_SECTION = u'General'
    RECENT_SECTION = u'RecentWiki'

    ASK_BEFORE_EXIT_PARAM = u'AskBeforeExit'
    ASK_BEFORE_EXIT_DEFAULT = False

    AUTOSAVE_INTERVAL_PARAM = u'AutosaveInterval'
    AUTOSAVE_INTERVAL_DEFAULT = 3

    RECENT_WIKI_COUNT_PARAM = u'maxcount'
    RECENT_WIKI_COUNT_DEFAULT = 5

    RECENT_ICONS_COUNT_PARAM = u'recenticonscount'
    RECENT_ICONS_COUNT_DEFAULT = 30

    RECENT_AUTOOPEN_PARAM = u'AutoOpen'
    RECENT_AUTOOPEN_DEFAULT = True

    DATETIME_FORMAT_PARAM = u'DateTimeFormat'
    DATETIME_FORMAT_DEFAULT = u'%c'

    # Последний используемый формат представления даты
    RECENT_DATETIME_FORMAT_PARAM = u'RecentDateTimeFormat'

    # Default tab for page(editor / preview / recent used)
    PAGE_TAB_RECENT = 0
    PAGE_TAB_CODE = 1
    PAGE_TAB_RESULT = 2

    PAGE_TAB_PARAM = u'PageTab'

    TABLE_COLS_COUNT = u'TableColsCount'
    TABLE_COLS_COUNT_DEFAULT = 1

    DEBUG_PARAM = u'debug'
    DEBUG_DEFAULT = False

    RECENT_TEXT_COLORS_PARAM = 'RecentTextColors'
    RECENT_TEXT_COLORS_DEFAULT = '#000000;#FFFFFF;#ff0000;#00ff00;#0000ff;#8a2be2;#7fff00;#d2691e;#6495ed;#dc143c;#00ffff;#a9a9a9;#ff8c00;#ff1493;#ffd700;#adff2f;#ffff00'.split(';')

    RECENT_BACKGROUND_COLORS_PARAM = 'RecentBackgroundColors'
    RECENT_BACKGROUND_COLORS_DEFAULT = '#000000;#FFFFFF;#ff0000;#00ff00;#0000ff;#8a2be2;#7fff00;#d2691e;#6495ed;#dc143c;#00ffff;#a9a9a9;#ff8c00;#ff1493;#ffd700;#adff2f;#ffff00'.split(';')

    def __init__(self, config):
        self.config = config

        # Спрашивать подтверждение выхода?
        self.askBeforeExit = BooleanOption(self.config,
                                           self.GENERAL_SECTION,
                                           self.ASK_BEFORE_EXIT_PARAM,
                                           self.ASK_BEFORE_EXIT_DEFAULT)

        # Интервал, через которое происходит автосохранение страницы.
        # Если значение <= 0, значит автосохранение отключено
        self.autosaveInterval = IntegerOption(self.config,
                                              self.GENERAL_SECTION,
                                              self.AUTOSAVE_INTERVAL_PARAM,
                                              self.AUTOSAVE_INTERVAL_DEFAULT)

        # Количество последних открытых вики
        self.historyLength = IntegerOption(self.config,
                                           self.RECENT_SECTION,
                                           self.RECENT_WIKI_COUNT_PARAM,
                                           self.RECENT_WIKI_COUNT_DEFAULT)

        # Recently icons history length
        self.iconsHistoryLength = IntegerOption(
            self.config,
            self.RECENT_SECTION,
            self.RECENT_ICONS_COUNT_PARAM,
            self.RECENT_ICONS_COUNT_DEFAULT)

        # Открывать последнуюю открытую вики при старте?
        self.autoopen = BooleanOption(self.config,
                                      self.RECENT_SECTION,
                                      self.RECENT_AUTOOPEN_PARAM,
                                      self.RECENT_AUTOOPEN_DEFAULT)

        # Формат для представления даты и времени модификиции страниц
        self.dateTimeFormat = StringOption(self.config,
                                           self.GENERAL_SECTION,
                                           self.DATETIME_FORMAT_PARAM,
                                           self.DATETIME_FORMAT_DEFAULT)

        # Последний используемый формат для представления даты и времени
        # модификиции страниц
        self.recentDateTimeFormat = StringOption(
            self.config,
            self.GENERAL_SECTION,
            self.RECENT_DATETIME_FORMAT_PARAM,
            self.dateTimeFormat.value
        )

        # Default tab for page(editor / preview / recent used)
        self.pageTab = IntegerOption(self.config,
                                     self.GENERAL_SECTION,
                                     self.PAGE_TAB_PARAM,
                                     self.PAGE_TAB_RECENT)

        # Default columns count in table dialog
        self.tableColsCount = IntegerOption(self.config,
                                            self.GENERAL_SECTION,
                                            self.TABLE_COLS_COUNT,
                                            self.TABLE_COLS_COUNT_DEFAULT)

        self.recentTextColors = ListOption(self.config,
                                           self.GENERAL_SECTION,
                                           self.RECENT_TEXT_COLORS_PARAM,
                                           self.RECENT_TEXT_COLORS_DEFAULT,
                                           separator=u';')

        self.recentBackgroundColors = ListOption(
            self.config,
            self.GENERAL_SECTION,
            self.RECENT_BACKGROUND_COLORS_PARAM,
            self.RECENT_BACKGROUND_COLORS_DEFAULT,
            separator=u';')

        self.debug = BooleanOption(self.config,
                                   self.GENERAL_SECTION,
                                   self.DEBUG_PARAM,
                                   self.DEBUG_DEFAULT)


class PluginsConfig(object):
    '''
    Класс для хранения настроек, связанных с плагинами
    '''
    PLUGINS_SECTION = u'Plugins'
    DISABLED_PARAM = u'Disabled'

    def __init__(self, config):
        self.config = config

        self.disabledPlugins = ListOption(self.config,
                                          PluginsConfig.PLUGINS_SECTION,
                                          PluginsConfig.DISABLED_PARAM,
                                          [],
                                          separator=u';')


class TrayConfig(object):
    '''
    Класс для хранения настроек, связанных с иконками в трее
    '''
    MINIMIZE_TO_TRAY_PARAM = u'MinimizeToTray'
    MINIMIZE_TO_TRAY_DEFAULT = True

    START_ICONIZED_PARAM = u'StartIconized'
    START_ICONIZED_DEFAULT = False

    ALWAYS_SHOW_TRAY_ICON_PARAM = u'AlwaysShowTrayIcon'
    ALWAYS_SHOW_TRAY_ICON_DEFAULT = False

    MINIMIZE_ON_CLOSE_PARAM = u'MinimizeOnClose'
    MINIMIZE_ON_CLOSE_DEFAULT = False

    def __init__(self, config):
        self.config = config

        # Сворачивать в трей?
        self.minimizeToTray = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.MINIMIZE_TO_TRAY_PARAM,
            TrayConfig.MINIMIZE_TO_TRAY_DEFAULT
        )

        # Запускаться свернутым?
        self.startIconized = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.START_ICONIZED_PARAM,
            TrayConfig.START_ICONIZED_DEFAULT
        )

        # Всегда показывать иконку в трее?
        self.alwaysShowTrayIcon = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.ALWAYS_SHOW_TRAY_ICON_PARAM,
            TrayConfig.ALWAYS_SHOW_TRAY_ICON_DEFAULT
        )

        # Сворачивать окно программы при закрытии главного окна
        self.minimizeOnClose = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            TrayConfig.MINIMIZE_ON_CLOSE_PARAM,
            TrayConfig.MINIMIZE_ON_CLOSE_DEFAULT
        )


class EditorConfig(object):
    '''
    Класс для хранения настроек редактора
    '''
    FONT_SECTION = u'Font'

    SHOW_LINE_NUMBERS_SECTION = u'ShowLineNumbers'
    SHOW_LINE_NUMBERS_DEFAULT = False

    TAB_WIDTH_SECTION = u'TabWidth'
    TAB_WIDTH_DEFAULT = 4

    FONT_SIZE_SECTION = u'size'
    FONT_SIZE_DEFAULT = 10

    FONT_NAME_SECTION = u'FaceName'
    FONT_NAME_DEFAULT = u''

    FONT_BOLD_SECTION = u'bold'
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = u'italic'
    FONT_ITALIC_DEFAULT = False

    # Поведение клавиш Home / End.
    HOME_END_OF_LINE = 0
    HOME_END_OF_PARAGRAPH = 1

    HOME_END_KEYS_SECTION = u'HomeEndKeys'
    HOME_END_KEYS_DEFAULT = HOME_END_OF_LINE

    # Цвет шрифта
    FONT_COLOR_SECTION = u'FontColor'
    FONT_COLOR_DEFAULT = u'#000000'

    # Цвет фона
    BACK_COLOR_SECTION = u'BackColor'
    BACK_COLOR_DEFAULT = u'#FFFFFF'

    # Selected text background color
    SEL_BACK_COLOR_SECTION = u'SelBackColor'
    SEL_BACK_COLOR_DEFAULT = u'#C0C0C0'

    # Margin background color
    MARGIN_BACK_COLOR_SECTION = u'MarginBackColor'
    MARGIN_BACK_COLOR_DEFAULT = u'#C4C4C4'

    # Spell checker
    SPELL_DICTS_SECTION = u'dictionaries'
    SPELL_DICT_DEFAULT = u'en_US, ru_RU, ru_RU_yo, uk_UA'

    SPELL_ENABLE_SECTION = u'SpellChecking'
    SPELL_ENABLE_DEFAULT = True

    SPELL_SKIP_DIGITS_SECTION = u'SpellSkipDigits'
    SPELL_SKIP_DIGITS_DEFAULT = True

    def __init__(self, config):
        self.config = config

        # Показывать номера строк в редакторе?
        self.lineNumbers = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SHOW_LINE_NUMBERS_SECTION,
            EditorConfig.SHOW_LINE_NUMBERS_DEFAULT
        )

        # Размер табуляции
        self.tabWidth = IntegerOption(self.config,
                                      GeneralGuiConfig.GENERAL_SECTION,
                                      EditorConfig.TAB_WIDTH_SECTION,
                                      EditorConfig.TAB_WIDTH_DEFAULT)

        # Размер шрифта
        self.fontSize = IntegerOption(self.config,
                                      EditorConfig.FONT_SECTION,
                                      EditorConfig.FONT_SIZE_SECTION,
                                      EditorConfig.FONT_SIZE_DEFAULT)

        # Начертание шрифта
        self.fontName = StringOption(self.config,
                                     EditorConfig.FONT_SECTION,
                                     EditorConfig.FONT_NAME_SECTION,
                                     EditorConfig.FONT_NAME_DEFAULT)

        self.fontIsBold = BooleanOption(self.config,
                                        EditorConfig.FONT_SECTION,
                                        EditorConfig.FONT_BOLD_SECTION,
                                        EditorConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption(self.config,
                                          EditorConfig.FONT_SECTION,
                                          EditorConfig.FONT_ITALIC_SECTION,
                                          EditorConfig.FONT_ITALIC_DEFAULT)

        # Поведение клавиш Home / End
        self.homeEndKeys = IntegerOption(self.config,
                                         GeneralGuiConfig.GENERAL_SECTION,
                                         EditorConfig.HOME_END_KEYS_SECTION,
                                         EditorConfig.HOME_END_KEYS_DEFAULT)

        self.fontColor = StringOption(self.config,
                                      GeneralGuiConfig.GENERAL_SECTION,
                                      EditorConfig.FONT_COLOR_SECTION,
                                      EditorConfig.FONT_COLOR_DEFAULT)

        self.backColor = StringOption(self.config,
                                      GeneralGuiConfig.GENERAL_SECTION,
                                      EditorConfig.BACK_COLOR_SECTION,
                                      EditorConfig.BACK_COLOR_DEFAULT)

        self.selBackColor = StringOption(self.config,
                                         GeneralGuiConfig.GENERAL_SECTION,
                                         EditorConfig.SEL_BACK_COLOR_SECTION,
                                         EditorConfig.SEL_BACK_COLOR_DEFAULT)

        self.marginBackColor = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.MARGIN_BACK_COLOR_SECTION,
            EditorConfig.MARGIN_BACK_COLOR_DEFAULT)

        self.spellCheckerDicts = StringOption(self.config,
                                              GeneralGuiConfig.GENERAL_SECTION,
                                              EditorConfig.SPELL_DICTS_SECTION,
                                              EditorConfig.SPELL_DICT_DEFAULT)

        self.spellEnabled = BooleanOption(self.config,
                                          GeneralGuiConfig.GENERAL_SECTION,
                                          EditorConfig.SPELL_ENABLE_SECTION,
                                          EditorConfig.SPELL_ENABLE_DEFAULT)

        self.spellSkipDigits = BooleanOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            EditorConfig.SPELL_SKIP_DIGITS_SECTION,
            EditorConfig.SPELL_SKIP_DIGITS_DEFAULT)


class HtmlEditorStylesConfig(object):
    '''
    Класс для хранения настроек стилей редактора HTML
    '''
    HTML_STYLES_SECTION = u'EditorStyles'

    STYLE_TAG_SECTION = u'tag'
    STYLE_TAG_DEFAULT = StcStyle.parse(u'fore:#000080,bold')

    STYLE_TAG_UNKNOWN_SECTION = u'tag_unknown'
    STYLE_TAG_UNKNOWN_DEFAULT = StcStyle.parse(u'fore:#FF0000')

    STYLE_ATTRIBUTE_SECTION = u'attribute'
    STYLE_ATTRIBUTE_DEFAULT = StcStyle.parse(u'fore:#008080')

    STYLE_ATTRIBUTE_UNKNOWN_SECTION = u'attribute_unknown'
    STYLE_ATTRIBUTE_UNKNOWN_DEFAULT = StcStyle.parse(u'fore:#FF0000')

    STYLE_NUMBER_SECTION = u'number'
    STYLE_NUMBER_DEFAULT = StcStyle.parse(u'fore:#000000')

    STYLE_STRING_SECTION = u'string'
    STYLE_STRING_DEFAULT = StcStyle.parse(u'fore:#0000FF')

    STYLE_COMMENT_SECTION = u'comment'
    STYLE_COMMENT_DEFAULT = StcStyle.parse(u'fore:#12B535')

    def __init__(self, config):
        self.config = config

        self.tag = StcStyleOption(self.config,
                                  HtmlEditorStylesConfig.HTML_STYLES_SECTION,
                                  HtmlEditorStylesConfig.STYLE_TAG_SECTION,
                                  HtmlEditorStylesConfig.STYLE_TAG_DEFAULT)

        self.tagUnknown = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_UNKNOWN_SECTION,
            HtmlEditorStylesConfig.STYLE_TAG_UNKNOWN_DEFAULT
        )

        self.attribute = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_DEFAULT
        )

        self.attributeUnknown = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_UNKNOWN_SECTION,
            HtmlEditorStylesConfig.STYLE_ATTRIBUTE_UNKNOWN_DEFAULT
        )

        self.number = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_NUMBER_SECTION,
            HtmlEditorStylesConfig.STYLE_NUMBER_DEFAULT
        )

        self.string = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_STRING_SECTION,
            HtmlEditorStylesConfig.STYLE_STRING_DEFAULT
        )

        self.comment = StcStyleOption(
            self.config,
            HtmlEditorStylesConfig.HTML_STYLES_SECTION,
            HtmlEditorStylesConfig.STYLE_COMMENT_SECTION,
            HtmlEditorStylesConfig.STYLE_COMMENT_DEFAULT
        )


class HtmlRenderConfig(object):
    '''
    Класс для хранения настроек HTML-рендера
    '''
    # Название секции в конфиге для настроек HTML
    HTML_SECTION = u'HTML'

    FONT_FACE_NAME_PARAM = u'FontFaceName'
    FONT_NAME_DEFAULT = u'Verdana'

    FONT_SIZE_PARAM = u'FontSize'
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_PARAM = u'FontBold'
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_PARAM = u'FontItalic'
    FONT_ITALIC_DEFAULT = False

    USER_STYLE_PARAM = u'UserStyle'
    USER_STYLE_DEFAULT = u''

    HTML_IMPROVER_PARAM = u'HtmlImprover'
    HTML_IMPROVER_DEFAULT = u'brimprover'

    def __init__(self, config):
        self.config = config

        self.fontSize = IntegerOption(self.config,
                                      HtmlRenderConfig.HTML_SECTION,
                                      HtmlRenderConfig.FONT_SIZE_PARAM,
                                      HtmlRenderConfig.FONT_SIZE_DEFAULT)

        self.fontName = StringOption(self.config,
                                     HtmlRenderConfig.HTML_SECTION,
                                     HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                     HtmlRenderConfig.FONT_NAME_DEFAULT)

        self.fontIsBold = BooleanOption(self.config,
                                        HtmlRenderConfig.HTML_SECTION,
                                        HtmlRenderConfig.FONT_BOLD_PARAM,
                                        HtmlRenderConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption(self.config,
                                          HtmlRenderConfig.HTML_SECTION,
                                          HtmlRenderConfig.FONT_ITALIC_PARAM,
                                          HtmlRenderConfig.FONT_ITALIC_DEFAULT)

        self.userStyle = StringOption(self.config,
                                      HtmlRenderConfig.HTML_SECTION,
                                      HtmlRenderConfig.USER_STYLE_PARAM,
                                      HtmlRenderConfig.USER_STYLE_DEFAULT)

        self.HTMLImprover = StringOption(
            self.config,
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.HTML_IMPROVER_PARAM,
            HtmlRenderConfig.HTML_IMPROVER_DEFAULT
        )


class TextPrintConfig(object):
    '''
    Класс для хранения настроек печати текста
    '''
    PRINT_SECTION = u'Print'

    FONT_NAME_SECTION = u'FontFaceName'
    FONT_NAME_DEFAULT = u'Arial'

    FONT_SIZE_SECTION = u'FontSize'
    FONT_SIZE_DEFAULT = 10

    FONT_BOLD_SECTION = u'FontBold'
    FONT_BOLD_DEFAULT = False

    FONT_ITALIC_SECTION = u'FontItalic'
    FONT_ITALIC_DEFAULT = False

    PAPPER_SIZE_SECTION = u'PaperId'
    PAPPER_SIZE_DEFAULT = wx.PAPER_A4

    MARGIN_TOP_SECTION = u'MarginTop'
    MARGIN_TOP_DEFAULT = 20

    MARGIN_BOTTOM_SECTION = u'MarginBottom'
    MARGIN_BOTTOM_DEFAULT = 20

    MARGIN_LEFT_SECTION = u'MarginLeft'
    MARGIN_LEFT_DEFAULT = 20

    MARGIN_RIGHT_SECTION = u'MarginRight'
    MARGIN_RIGHT_DEFAULT = 20

    def __init__(self, config):
        self.config = config

        # Настройки шрифта
        self.fontName = StringOption(self.config,
                                     TextPrintConfig.PRINT_SECTION,
                                     TextPrintConfig.FONT_NAME_SECTION,
                                     TextPrintConfig.FONT_NAME_DEFAULT)

        self.fontSize = IntegerOption(self.config,
                                      TextPrintConfig.PRINT_SECTION,
                                      TextPrintConfig.FONT_SIZE_SECTION,
                                      TextPrintConfig.FONT_SIZE_DEFAULT)

        self.fontIsBold = BooleanOption(self.config,
                                        TextPrintConfig.PRINT_SECTION,
                                        TextPrintConfig.FONT_BOLD_SECTION,
                                        TextPrintConfig.FONT_BOLD_DEFAULT)

        self.fontIsItalic = BooleanOption(self.config,
                                          TextPrintConfig.PRINT_SECTION,
                                          TextPrintConfig.FONT_ITALIC_SECTION,
                                          TextPrintConfig.FONT_ITALIC_DEFAULT)

        self.paperId = IntegerOption(self.config,
                                     TextPrintConfig.PRINT_SECTION,
                                     TextPrintConfig.PAPPER_SIZE_SECTION,
                                     TextPrintConfig.PAPPER_SIZE_DEFAULT)

        self.marginTop = IntegerOption(self.config,
                                       TextPrintConfig.PRINT_SECTION,
                                       TextPrintConfig.MARGIN_TOP_SECTION,
                                       TextPrintConfig.MARGIN_TOP_DEFAULT)

        self.marginBottom = IntegerOption(
            self.config,
            TextPrintConfig.PRINT_SECTION,
            TextPrintConfig.MARGIN_BOTTOM_SECTION,
            TextPrintConfig.MARGIN_BOTTOM_DEFAULT
        )

        self.marginLeft = IntegerOption(self.config,
                                        TextPrintConfig.PRINT_SECTION,
                                        TextPrintConfig.MARGIN_LEFT_SECTION,
                                        TextPrintConfig.MARGIN_LEFT_DEFAULT)

        self.marginRight = IntegerOption(self.config,
                                         TextPrintConfig.PRINT_SECTION,
                                         TextPrintConfig.MARGIN_RIGHT_SECTION,
                                         TextPrintConfig.MARGIN_RIGHT_DEFAULT)


class MainWindowConfig(object):
    '''
    Класс для хранения настроек главного окна
    '''
    MAIN_WINDOW_SECTION = u'MainWindow'

    TITLE_FORMAT_SECTION = u'Title'
    TITLE_FORMAT_DEFAULT = u'{page} - {file} - OutWiker'

    WIDTH_SECTION = u'width'
    WIDTH_DEFAULT = 800

    HEIGHT_SECTION = u'height'
    HEIGHT_DEFAULT = 680

    XPOS_SECTION = u'xpos'
    XPOS_DEFAULT = 0

    YPOS_SECTION = u'ypos'
    YPOS_DEFAULT = 0

    FULLSCREEN_SECTION = u'fullscreen'
    FULLSCREEN_DEFAULT = False

    MAXIMIZED_SECTION = u'maximized'
    MAXIMIZED_DEFAULT = False

    # Размер области в статусной панели для показа даты изменения текущей
    # страницы
    DATETIME_STATUS_WIDTH_SECTION = u'datetime_status_width'
    DATETIME_STATUS_WIDTH_DEFAULT = 250

    STATUSBAR_VISIBLE_SECTION = 'statusbar_visible'
    STATUSBAR_VISIBLE_DEFAULT = True

    MAIN_PANES_BACKGROUND_COLOR_SECTION = 'main_panes_background_color'
    MAIN_PANES_BACKGROUND_COLOR_DEFAULT = '#ffffff'

    MAIN_PANES_TEXT_COLOR_SECTION = 'main_panes_text_color'
    MAIN_PANES_TEXT_COLOR_DEFAULT = '#000000'

    def __init__(self, config):
        self.config = config

        self.titleFormat = StringOption(self.config,
                                        MainWindowConfig.MAIN_WINDOW_SECTION,
                                        self.TITLE_FORMAT_SECTION,
                                        self.TITLE_FORMAT_DEFAULT)

        self.width = IntegerOption(self.config,
                                   MainWindowConfig.MAIN_WINDOW_SECTION,
                                   self.WIDTH_SECTION,
                                   self.WIDTH_DEFAULT)

        self.height = IntegerOption(self.config,
                                    MainWindowConfig.MAIN_WINDOW_SECTION,
                                    self.HEIGHT_SECTION,
                                    self.HEIGHT_DEFAULT)

        self.xPos = IntegerOption(self.config,
                                  MainWindowConfig.MAIN_WINDOW_SECTION,
                                  self.XPOS_SECTION,
                                  self.XPOS_DEFAULT)

        self.yPos = IntegerOption(self.config,
                                  MainWindowConfig.MAIN_WINDOW_SECTION,
                                  self.YPOS_SECTION,
                                  self.YPOS_DEFAULT)

        self.fullscreen = BooleanOption(self.config,
                                        MainWindowConfig.MAIN_WINDOW_SECTION,
                                        self.FULLSCREEN_SECTION,
                                        self.FULLSCREEN_DEFAULT)

        self.maximized = BooleanOption(self.config,
                                       MainWindowConfig.MAIN_WINDOW_SECTION,
                                       self.MAXIMIZED_SECTION,
                                       self.MAXIMIZED_DEFAULT)

        self.datetimeStatusWidth = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.DATETIME_STATUS_WIDTH_SECTION,
            self.DATETIME_STATUS_WIDTH_DEFAULT)

        self.statusbar_visible = BooleanOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.STATUSBAR_VISIBLE_SECTION,
            self.STATUSBAR_VISIBLE_DEFAULT)

        self.mainPanesBackgroundColor = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.MAIN_PANES_BACKGROUND_COLOR_SECTION,
            self.MAIN_PANES_BACKGROUND_COLOR_DEFAULT)

        self.mainPanesTextColor = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.MAIN_PANES_TEXT_COLOR_SECTION,
            self.MAIN_PANES_TEXT_COLOR_DEFAULT)


class TreeConfig(object):
    '''
    Класс для хранения настроек панели с деревом
    '''
    WIDTH_SECTION = u'TreeWidth'
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u'TreeHeight'
    HEIGHT_DEFAULT = 250

    PANE_OPTIONS_SECTION = u'TreePane'
    PANE_OPTIONS_DEFAULT = u''

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(self.config,
                                   MainWindowConfig.MAIN_WINDOW_SECTION,
                                   TreeConfig.WIDTH_SECTION,
                                   TreeConfig.WIDTH_DEFAULT)

        self.height = IntegerOption(self.config,
                                    MainWindowConfig.MAIN_WINDOW_SECTION,
                                    TreeConfig.HEIGHT_SECTION,
                                    TreeConfig.HEIGHT_DEFAULT)

        # Параметры панели с деревом
        self.pane = StringOption(self.config,
                                 MainWindowConfig.MAIN_WINDOW_SECTION,
                                 TreeConfig.PANE_OPTIONS_SECTION,
                                 TreeConfig.PANE_OPTIONS_DEFAULT)


class AttachConfig(object):
    '''
    Класс для хранения настроек панели с вложенными файлами
    '''
    WIDTH_SECTION = u'AttachesWidth'
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u'AttachesHeight'
    HEIGHT_DEFAULT = 150

    PANE_OPTIONS_SECTION = u'AttachesPane'
    PANE_OPTIONS_DEFAULT = u''

    ACTION_INSERT_LINK = 0
    ACTION_OPEN = 1

    DOUBLE_CLICK_ACTION_PARAM = u'AttachDoubleClickAction'
    DOUBLE_CLICK_ACTION_DEFAULT = ACTION_OPEN

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.WIDTH_SECTION,
            self.WIDTH_DEFAULT)

        self.height = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.HEIGHT_SECTION,
            self.HEIGHT_DEFAULT)

        self.pane = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.PANE_OPTIONS_SECTION,
            self.PANE_OPTIONS_DEFAULT)

        self.doubleClickAction = IntegerOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.DOUBLE_CLICK_ACTION_PARAM,
            self.DOUBLE_CLICK_ACTION_DEFAULT
        )


class TagsCloudConfig(object):
    '''
    Класс для хранения настроек панели с облагом тегов
    '''
    WIDTH_SECTION = u'TagsCloudWidth'
    WIDTH_DEFAULT = 250

    HEIGHT_SECTION = u'TagsCloudHeight'
    HEIGHT_DEFAULT = 170

    PANE_OPTIONS_SECTION = u'TagsCloudPane'
    PANE_OPTIONS_DEFAULT = u''

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(self.config,
                                   MainWindowConfig.MAIN_WINDOW_SECTION,
                                   self.WIDTH_SECTION,
                                   self.WIDTH_DEFAULT)

        self.height = IntegerOption(self.config,
                                    MainWindowConfig.MAIN_WINDOW_SECTION,
                                    self.HEIGHT_SECTION,
                                    self.HEIGHT_DEFAULT)

        # Параметры панели с деревом
        self.pane = StringOption(self.config,
                                 MainWindowConfig.MAIN_WINDOW_SECTION,
                                 self.PANE_OPTIONS_SECTION,
                                 self.PANE_OPTIONS_DEFAULT)


class PageDialogConfig(object):
    WIDTH_SECTION = u'PageDialogWidth'
    WIDTH_DEFAULT = 500

    HEIGHT_SECTION = u'PageDialogHeight'
    HEIGHT_DEFAULT = 350

    # Последний используемый стиль
    RECENT_STYLE_SECTION = u'RecentStyle'
    RECENT_STYLE_DEFAULT = u''

    RECENT_CREATED_PAGE_TYPE_PARAM = u'RecentCreatedPageType'
    RECENT_CREATED_PAGE_TYPE_DEFAULT = u'wiki'

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(self.config,
                                   MainWindowConfig.MAIN_WINDOW_SECTION,
                                   self.WIDTH_SECTION,
                                   self.WIDTH_DEFAULT)

        self.height = IntegerOption(self.config,
                                    MainWindowConfig.MAIN_WINDOW_SECTION,
                                    self.HEIGHT_SECTION,
                                    self.HEIGHT_DEFAULT)

        self.recentStyle = StringOption(self.config,
                                        GeneralGuiConfig.GENERAL_SECTION,
                                        self.RECENT_STYLE_SECTION,
                                        self.RECENT_STYLE_DEFAULT)

        self.recentCreatedPageType = StringOption(
            self.config,
            GeneralGuiConfig.GENERAL_SECTION,
            self.RECENT_CREATED_PAGE_TYPE_PARAM,
            self.RECENT_CREATED_PAGE_TYPE_DEFAULT
        )


class PrefDialogConfig(object):
    WIDTH_SECTION = u'PrefDialogWidth'
    WIDTH_DEFAULT = 800

    HEIGHT_SECTION = u'PrefDialogHeight'
    HEIGHT_DEFAULT = 500

    def __init__(self, config):
        self.config = config

        self.width = IntegerOption(self.config,
                                   MainWindowConfig.MAIN_WINDOW_SECTION,
                                   self.WIDTH_SECTION,
                                   self.WIDTH_DEFAULT)

        self.height = IntegerOption(self.config,
                                    MainWindowConfig.MAIN_WINDOW_SECTION,
                                    self.HEIGHT_SECTION,
                                    self.HEIGHT_DEFAULT)


class TagsConfig(object):
    """
    Options for tags and tags cloud
    """
    SECTION = u'Tags'

    TAG_COLOR_FONT_NORMAL_PARAM = u'TagFontNormalColor'
    TAG_COLOR_FONT_NORMAL_DEFAULT = u'#0000FF'

    TAG_COLOR_FONT_SELECTED_PARAM = u'TagFontSelectedColor'
    TAG_COLOR_FONT_SELECTED_DEFAULT = u'#0000FF'

    TAG_COLOR_FONT_NORMAL_HOVER_PARAM = u'TagFontNormalHoverColor'
    TAG_COLOR_FONT_NORMAL_HOVER_DEFAULT = u'#FF0000'

    TAG_COLOR_FONT_SELECTED_HOVER_PARAM = u'TagFontSelectedHoverColor'
    TAG_COLOR_FONT_SELECTED_HOVER_DEFAULT = u'#FF0000'

    TAG_COLOR_BACK_SELECTED_PARAM = u'TagBackSelectedColor'
    TAG_COLOR_BACK_SELECTED_DEFAULT = u'#FAFF24'

    ACTION_SHOW_LIST = 0
    ACTION_MARK_TOGGLE = 1

    LEFT_CLICK_ACTION_PARAM = u'LeftClickAction'
    LEFT_CLICK_ACTION_DEFAULT = ACTION_SHOW_LIST

    MIDDLE_CLICK_ACTION_PARAM = u'MiddleClickAction'
    MIDDLE_CLICK_ACTION_DEFAULT = ACTION_MARK_TOGGLE

    POPUP_HEADERS_SECTION = 'PopupHeaders'
    POPUP_HEADERS_DEFAULT = ''

    def __init__(self, config):
        self.config = config

        self.colorFontNormal = StringOption(
            self.config,
            self.SECTION,
            self.TAG_COLOR_FONT_NORMAL_PARAM,
            self.TAG_COLOR_FONT_NORMAL_DEFAULT
        )

        self.colorFontSelected = StringOption(
            self.config,
            self.SECTION,
            self.TAG_COLOR_FONT_SELECTED_PARAM,
            self.TAG_COLOR_FONT_SELECTED_DEFAULT
        )

        self.colorFontNormalHover = StringOption(
            self.config,
            self.SECTION,
            self.TAG_COLOR_FONT_NORMAL_HOVER_PARAM,
            self.TAG_COLOR_FONT_NORMAL_HOVER_DEFAULT
        )

        self.colorFontSelectedHover = StringOption(
            self.config,
            self.SECTION,
            self.TAG_COLOR_FONT_SELECTED_HOVER_PARAM,
            self.TAG_COLOR_FONT_SELECTED_HOVER_DEFAULT
        )

        self.colorBackSelected = StringOption(
            self.config,
            self.SECTION,
            self.TAG_COLOR_BACK_SELECTED_PARAM,
            self.TAG_COLOR_BACK_SELECTED_DEFAULT
        )

        self.leftClickAction = IntegerOption(
            self.config,
            self.SECTION,
            self.LEFT_CLICK_ACTION_PARAM,
            self.LEFT_CLICK_ACTION_DEFAULT
        )

        self.middleClickAction = IntegerOption(
            self.config,
            self.SECTION,
            self.MIDDLE_CLICK_ACTION_PARAM,
            self.MIDDLE_CLICK_ACTION_DEFAULT
        )

        self.popupHeaders = StringOption(
            self.config,
            MainWindowConfig.MAIN_WINDOW_SECTION,
            self.POPUP_HEADERS_SECTION,
            self.POPUP_HEADERS_DEFAULT
        )
