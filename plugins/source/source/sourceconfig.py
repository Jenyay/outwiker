#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption, IntegerOption, ListOption


class SourceConfig (object):
    def __init__ (self, config):
        self.__config = config

        section = u"SourcePlugin"

        # Размер табуляции по умолчанию
        self.DEFAULT_TAB_WIDTH = 4
        tabWidthOption = u"TabWidth"

        self.__tabWidth = IntegerOption (self.__config, 
                section, 
                tabWidthOption, 
                self.DEFAULT_TAB_WIDTH)

        # Язык программирования по умолчанию
        self.DEFAULT_LANGUAGE = u"text"
        defaultLanguageOption = u"DefaultLanguage"

        self.__defaultLanguage = StringOption (self.__config, 
                section, 
                defaultLanguageOption, 
                self.DEFAULT_LANGUAGE)

        # Список выбранных языков программирования
        self.DEFAULT_LANGUAGE_LIST = [
            u"text",
            u"c",
            u"cpp",
            u"csharp",
            u"php",
            u"python",
            u"html",
            u"css",
            u"ruby",
            u"java",
            u"javascript",
            u"objective-c",
            u"perl",
            u"vb.net"]

        languageListOption = u"LanguageList"

        self.__languageList = ListOption (self.__config, 
                section, 
                languageListOption, 
                self.DEFAULT_LANGUAGE_LIST)


    @property
    def tabWidth (self):
        return self.__tabWidth


    @property
    def defaultLanguage (self):
        return self.__defaultLanguage


    @property
    def languageList (self):
        return self.__languageList
