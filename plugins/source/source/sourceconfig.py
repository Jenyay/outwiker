#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption, IntegerOption


class SourceConfig (object):
    def __init__ (self, config):
        self.__config = config

        section = u"SourcePlugin"

        # Размер табуляции по умолчанию
        self.DEFAULT_TAB_WIDTH = 4
        tabWidthOption = u"TabWidth"
        self.__tabWidth = IntegerOption (self.__config, section, tabWidthOption, self.DEFAULT_TAB_WIDTH)

        # Язык программирования по умолчанию
        self.DEFAULT_LANGUAGE = u"text"
        defaultLanguageOption = u"DefaultLanguage"
        self.__defaultLanguage = StringOption (self.__config, section, defaultLanguageOption, self.DEFAULT_LANGUAGE)


    @property
    def tabWidth (self):
        return self.__tabWidth


    @property
    def defaultLanguage (self):
        return self.__defaultLanguage
