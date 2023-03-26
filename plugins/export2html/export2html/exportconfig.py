# -*- coding: utf-8 -*-

from outwiker.api.core.config import BooleanOption


class ExportConfig:
    def __init__(self, config):
        self.__config = config

        self.section = "Export2Html"

        # Перезаписывать существующие файлы?
        overwriteOption = "Overwrite"

        self.__overwrite = BooleanOption(
            self.__config, self.section, overwriteOption, False
        )

        # Прикрепленные файлы. Сохранять только картинки
        imagesOnlyOption = "ImagesOnly"

        self.__imagesOnly = BooleanOption(
            self.__config, self.section, imagesOnlyOption, False
        )

        # Создавать файлы с длинными именами (включать заголовки родителей)
        longNamesOption = "LongNames"

        self.__longNames = BooleanOption(
            self.__config, self.section, longNamesOption, False
        )

    @property
    def overwrite(self):
        """
        Перезаписывать существующие файлы?
        """
        return self.__overwrite.value

    @overwrite.setter
    def overwrite(self, value):
        self.__overwrite.value = value

    @property
    def imagesOnly(self):
        """
        Прикрепленные файлы. Сохранять только картинки
        """
        return self.__imagesOnly.value

    @imagesOnly.setter
    def imagesOnly(self, value):
        self.__imagesOnly.value = value

    @property
    def longNames(self):
        return self.__longNames.value

    @longNames.setter
    def longNames(self, value):
        self.__longNames.value = value
