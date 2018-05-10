# -*- coding: utf-8 -*-

import datetime

from outwiker.core.config import IntegerOption, DateTimeOption, BooleanOption


class UpdatesConfig (object):
    def __init__(self, config):
        self.__config = config

        self.section = u"UpdateNotifierPlugin"

        # Интервал обновлений (в днях)
        UPDATE_INTERVAL_OPTION = u"UpdateInterval"

        # Интервал проверки обновлений по умолчанию
        UPDATE_INTERVAL_DEFAULT = 7

        self.__updateInterval = IntegerOption(self.__config,
                                              self.section,
                                              UPDATE_INTERVAL_OPTION,
                                              UPDATE_INTERVAL_DEFAULT)

        # Дата последней проверки обновлений
        LAST_UPDATE_OPTION = u"LastUpdate"

        # Дата последнего обновления по умолчанию (если еще не было обновлений)
        LAST_UPDATE_DEFAULT = datetime.datetime(1961, 4, 12)

        self.__lastUpdate = DateTimeOption(self.__config,
                                           self.section,
                                           LAST_UPDATE_OPTION,
                                           LAST_UPDATE_DEFAULT)

        # Игнорировать обновления нестабильной версии OutWiker?
        IGNORE_UNSTABLE_OPTION = u"IgnoreUnstable"

        IGNORE_UNSTABLE_DEFAULT = False

        self.__ignoreUnstable = BooleanOption(self.__config,
                                              self.section,
                                              IGNORE_UNSTABLE_OPTION,
                                              IGNORE_UNSTABLE_DEFAULT)

    @property
    def updateInterval(self):
        """
        Интервал для автоматических обновлений
        """
        return self.__updateInterval.value

    @updateInterval.setter
    def updateInterval(self, value):
        """
        Интервал для автоматических обновлений
        """
        self.__updateInterval.value = value

    @property
    def lastUpdate(self):
        """
        Дата последнего обновления
        """
        return self.__lastUpdate.value

    @lastUpdate.setter
    def lastUpdate(self, value):
        """
        Дата последнего обновления
        """
        self.__lastUpdate.value = value

    @property
    def ignoreUnstable(self):
        return self.__ignoreUnstable.value

    @ignoreUnstable.setter
    def ignoreUnstable(self, value):
        self.__ignoreUnstable.value = value
