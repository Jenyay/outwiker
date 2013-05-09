#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption


class StatisticsConfig (object):
    def __init__ (self, config):
        self.__config = config

        self.section = u"StatisticsPlugin"

        # Размеры диалога статистики дерева
        self.DEFAULT_TREE_DIALOG_WIDTH = 600
        self.DEFAULT_TREE_DIALOG_HEIGHT = 500

        treeDialogWidthOption = u"TreeDialogWidth"
        treeDialogHeightOption = u"TreeDialogHeight"

        self.__treeDialogWidth = IntegerOption (self.__config, 
                self.section, 
                treeDialogWidthOption, 
                self.DEFAULT_TREE_DIALOG_WIDTH)

        self.__treeDialogHeight = IntegerOption (self.__config, 
                self.section, 
                treeDialogHeightOption, 
                self.DEFAULT_TREE_DIALOG_HEIGHT)


    @property
    def treeDialogWidth (self):
        return self.__treeDialogWidth


    @property
    def treeDialogHeight (self):
        return self.__treeDialogHeight
