#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption, IntegerOption, ListOption

from .params import LANGUAGE_DEFAULT, TAB_WIDTH_DEFAULT, STYLE_DEFAULT, LANGUAGE_LIST_DEFAULT


class SourceConfig (object):
    def __init__ (self, config):
        self.__config = config

        section = u"SourcePlugin"

        # Размер табуляции по умолчанию
        tabWidthOption = u"TabWidth"

        self.__tabWidth = IntegerOption (self.__config, 
                section, 
                tabWidthOption, 
                TAB_WIDTH_DEFAULT)


        # Язык программирования по умолчанию
        defaultLanguageOption = u"DefaultLanguage"

        self.__defaultLanguage = StringOption (self.__config, 
                section, 
                defaultLanguageOption, 
                LANGUAGE_DEFAULT)


        # Список выбранных языков программирования
        languageListOption = u"LanguageList"

        self.__languageList = ListOption (self.__config, 
                section, 
                languageListOption, 
                LANGUAGE_LIST_DEFAULT)


        # Стиль по умолчанию
        styleOption = u"Style"

        self.__style = StringOption (self.__config, 
                section, 
                styleOption, 
                STYLE_DEFAULT)


        # Размеры диалога для вставки команды (:source:)
        self.DEFAULT_DIALOG_WIDTH = -1
        self.DEFAULT_DIALOG_HEIGHT = -1

        dialogWidthOption = u"DialogWidth"
        dialogHeightOption = u"DialogHeight"

        self.__dialogWidth = IntegerOption (self.__config, 
                section, 
                dialogWidthOption, 
                self.DEFAULT_DIALOG_WIDTH)

        self.__dialogHeight = IntegerOption (self.__config, 
                section, 
                dialogHeightOption, 
                self.DEFAULT_DIALOG_HEIGHT)



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
        return self.__style
