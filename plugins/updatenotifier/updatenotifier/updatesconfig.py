#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption, DateTimeOption

class UpdatesConfig (object):
    def __init__ (self, config):
        self.__config = config

        self.section = u"UpdateNotifierPlugin"

        # Интервал проверки обновлений по умолчанию
        DEFAULT_INTERVAL = 7

        # Интервал обновлений (в днях)
        updateIntervalOption = u"UpdateInterval"

        self.__updateInterval = IntegerOption (self.__config, 
                self.section, 
                updateIntervalOption, 
                DEFAULT_INTERVAL)


    @property
    def updateInterval (self):
        return self.__updateInterval.value


    @updateInterval.setter
    def updateInterval (self, value):
        self.__updateInterval.value = value
