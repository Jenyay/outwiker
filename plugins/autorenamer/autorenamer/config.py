# -*- coding: utf-8 -*-

from outwiker.api.core.config import BooleanOption


class PluginConfig:
    def __init__(self, config):
        self.__config = config
        self.section = "AutoRenamerPlugin"

        AUTORENAME_ALL_PAGES_OPTION = "AutoRenameAllPages"
        AUTORENAME_ALL_PAGES_DEFAULT = False
        self.__autoRenameAllPages = BooleanOption(
            self.__config,
            self.section,
            AUTORENAME_ALL_PAGES_OPTION,
            AUTORENAME_ALL_PAGES_DEFAULT,
        )

        AUTOSET_FIRST_LINE_OPTION = "AutoSetFirstLine"
        AUTOSET_FIRST_LINE_DEFAULT = False
        self.__autoSetFirstLine = BooleanOption(
            self.__config,
            self.section,
            AUTOSET_FIRST_LINE_OPTION,
            AUTOSET_FIRST_LINE_DEFAULT,
        )

    @property
    def autoRenameAllPages(self):
        return self.__autoRenameAllPages.value

    @autoRenameAllPages.setter
    def autoRenameAllPages(self, value):
        self.__autoRenameAllPages.value = value

    @property
    def autoSetFirstLine(self):
        return self.__autoSetFirstLine.value

    @autoSetFirstLine.setter
    def autoSetFirstLine(self, value):
        self.__autoSetFirstLine.value = value
