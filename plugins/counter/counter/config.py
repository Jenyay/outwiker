# -*- coding: utf-8 -*-

from outwiker.api.core.config import IntegerOption


class CounterConfig:
    def __init__(self, config):
        self.__config = config

        self.section = "CounterPlugin"

        # Размеры диалога для вставки команды (:counter:)
        self.DEFAULT_DIALOG_WIDTH = -1
        self.DEFAULT_DIALOG_HEIGHT = -1

        dialogWidthOption = "DialogWidth"
        dialogHeightOption = "DialogHeight"

        self.__dialogWidth = IntegerOption(self.__config, 
                self.section, 
                dialogWidthOption, 
                self.DEFAULT_DIALOG_WIDTH)

        self.__dialogHeight = IntegerOption(self.__config, 
                self.section, 
                dialogHeightOption, 
                self.DEFAULT_DIALOG_HEIGHT)
        
    @property
    def dialogWidth(self):
        return self.__dialogWidth

    @property
    def dialogHeight(self):
        return self.__dialogHeight
