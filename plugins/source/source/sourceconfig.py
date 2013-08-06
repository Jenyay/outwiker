#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption, IntegerOption, ListOption, BooleanOption

from .params import LANGUAGE_DEFAULT, TAB_WIDTH_DEFAULT, STYLE_DEFAULT, LANGUAGE_LIST_DEFAULT


class SourceConfig (object):
    def __init__ (self, config):
        self.__config = config

        self.section = u"SourcePlugin"

        # Размер табуляции по умолчанию
        tabWidthOption = u"TabWidth"

        self.__tabWidth = IntegerOption (self.__config, 
                self.section, 
                tabWidthOption, 
                TAB_WIDTH_DEFAULT)


        # Язык программирования по умолчанию
        defaultLanguageOption = u"DefaultLanguage"

        self.__defaultLanguage = StringOption (self.__config, 
                self.section, 
                defaultLanguageOption, 
                LANGUAGE_DEFAULT)


        # Список выбранных языков программирования
        languageListOption = u"LanguageList"

        self.__languageList = ListOption (self.__config, 
                self.section, 
                languageListOption, 
                LANGUAGE_LIST_DEFAULT)


        # Стиль, используемый по умолчанию (если стиль не указан явно)
        defaultStyleOption = u"DefaultStyle"

        self.__defaultStyle = StringOption (self.__config, 
                self.section, 
                defaultStyleOption, 
                STYLE_DEFAULT)

        # Размеры диалога для вставки команды (:source:)
        self.DEFAULT_DIALOG_WIDTH = -1
        self.DEFAULT_DIALOG_HEIGHT = -1

        dialogWidthOption = u"DialogWidth"
        dialogHeightOption = u"DialogHeight"

        self.__dialogWidth = IntegerOption (self.__config, 
                self.section, 
                dialogWidthOption, 
                self.DEFAULT_DIALOG_WIDTH)

        self.__dialogHeight = IntegerOption (self.__config, 
                self.section, 
                dialogHeightOption, 
                self.DEFAULT_DIALOG_HEIGHT)


        # Настройка "Использовать фон страницы в блоке кода"
        self.DEFAULT_PARENT_BACKGROUND = False
        parentBgOption = u"ParentBg"

        self.__parentBg = BooleanOption (self.__config,
                self.section,
                parentBgOption,
                self.DEFAULT_PARENT_BACKGROUND)


        # Настройка для добавления нумерации строк
        self.DEFAULT_LINE_NUM = False
        lineNumOption = u"LineNum"

        self.__lineNum = BooleanOption (self.__config,
                self.section,
                lineNumOption,
                self.DEFAULT_LINE_NUM)



    @property
    def tabWidth (self):
        return self.__tabWidth


    @property
    def defaultLanguage (self):
        return self.__defaultLanguage


    @property
    def languageList (self):
        return self.__languageList


    @property
    def dialogWidth (self):
        return self.__dialogWidth


    @property
    def dialogHeight (self):
        return self.__dialogHeight


    @property
    def style (self):
        styleOption = u"Style"

        # Стиль, выбранный в диалоге по умолчанию
        # Переменная, отвечающая за параметр создается здесь, 
        # чтобы можно было использовать значение по умолчанию, 
        # прочитанное из defaultStyle
        style = StringOption (self.__config, 
                self.section, 
                styleOption, 
                self.defaultStyle.value)

        return style


    @property
    def defaultStyle (self):
        return self.__defaultStyle


    @property
    def parentbg (self):
        return self.__parentBg


    @property
    def lineNum (self):
        return self.__lineNum
