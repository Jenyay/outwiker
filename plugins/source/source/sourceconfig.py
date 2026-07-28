# -*- coding: utf-8 -*-

from outwiker.api.core.config import (
    StringOption,
    IntegerOption,
    ListOption,
    BooleanOption,
)

from .params import (
    LANGUAGE_DEFAULT,
    TAB_WIDTH_DEFAULT,
    STYLE_DEFAULT,
    LANGUAGE_LIST_DEFAULT,
)


class SourceConfig:
    def __init__(self, config):
        self.__config = config

        self.section = "SourcePlugin"

        # Default tab size
        tabWidthOption = "TabWidth"

        self.__tabWidth = IntegerOption(
            self.__config, self.section, tabWidthOption, TAB_WIDTH_DEFAULT
        )

        # Default programming language
        defaultLanguageOption = "DefaultLanguage"

        self.__defaultLanguage = StringOption(
            self.__config, self.section, defaultLanguageOption, LANGUAGE_DEFAULT
        )

        # List of selected programming languages
        languageListOption = "LanguageList"

        self.__languageList = ListOption(
            self.__config, self.section, languageListOption, LANGUAGE_LIST_DEFAULT
        )

        # Default style (used if style is not specified explicitly)
        defaultStyleOption = "DefaultStyle"

        self.__defaultStyle = StringOption(
            self.__config, self.section, defaultStyleOption, STYLE_DEFAULT
        )

        # Размеры диалога для вставки команды (:source:)
        self.DEFAULT_DIALOG_WIDTH = -1
        self.DEFAULT_DIALOG_HEIGHT = -1

        dialogWidthOption = "DialogWidth"
        dialogHeightOption = "DialogHeight"

        self.__dialogWidth = IntegerOption(
            self.__config, self.section, dialogWidthOption, self.DEFAULT_DIALOG_WIDTH
        )

        self.__dialogHeight = IntegerOption(
            self.__config, self.section, dialogHeightOption, self.DEFAULT_DIALOG_HEIGHT
        )

        # "Use page background in code block" setting
        self.DEFAULT_PARENT_BACKGROUND = False
        parentBgOption = "ParentBg"

        self.__parentBg = BooleanOption(
            self.__config, self.section, parentBgOption, self.DEFAULT_PARENT_BACKGROUND
        )

        # Setting for line numbering
        self.DEFAULT_LINE_NUM = False
        lineNumOption = "LineNum"

        self.__lineNum = BooleanOption(
            self.__config, self.section, lineNumOption, self.DEFAULT_LINE_NUM
        )

    @property
    def tabWidth(self):
        return self.__tabWidth

    @property
    def defaultLanguage(self):
        return self.__defaultLanguage

    @property
    def languageList(self):
        return self.__languageList

    @property
    def dialogWidth(self):
        return self.__dialogWidth

    @property
    def dialogHeight(self):
        return self.__dialogHeight

    @property
    def style(self):
        styleOption = "Style"

        # Style selected in dialog by default
        # Variable for parameter is created here to use the default value
        # read from defaultStyle
        style = StringOption(
            self.__config, self.section, styleOption, self.defaultStyle.value
        )

        return style

    @property
    def defaultStyle(self):
        return self.__defaultStyle

    @property
    def parentbg(self):
        return self.__parentBg

    @property
    def lineNum(self):
        return self.__lineNum
