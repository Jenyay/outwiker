# -*- coding: utf-8 -*-

from outwiker.api.core.config import IntegerOption


class StatisticsConfig:
    def __init__(self, config):
        self.__config = config

        self.section = "StatisticsPlugin"

        # Размеры диалога статистики дерева
        self.DEFAULT_TREE_DIALOG_WIDTH = 600
        self.DEFAULT_TREE_DIALOG_HEIGHT = 500

        treeDialogWidthOption = "TreeDialogWidth"
        treeDialogHeightOption = "TreeDialogHeight"

        self.__treeDialogWidth = IntegerOption(
            self.__config,
            self.section,
            treeDialogWidthOption,
            self.DEFAULT_TREE_DIALOG_WIDTH,
        )

        self.__treeDialogHeight = IntegerOption(
            self.__config,
            self.section,
            treeDialogHeightOption,
            self.DEFAULT_TREE_DIALOG_HEIGHT,
        )

    @property
    def treeDialogWidth(self):
        return self.__treeDialogWidth

    @property
    def treeDialogHeight(self):
        return self.__treeDialogHeight
