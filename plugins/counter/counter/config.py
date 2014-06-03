# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption


class CounterConfig (object):
    def __init__ (self, config):
        self.__config = config

        self.section = u"CounterPlugin"

        # Размеры диалога для вставки команды (:counter:)
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
    
        
    @property
    def dialogWidth (self):
        return self.__dialogWidth


    @property
    def dialogHeight (self):
        return self.__dialogHeight
