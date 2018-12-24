# -*- coding: utf-8 -*-

import os
import os.path

from .style import Style


class StylesList(object):
    """
    Класс для хранения списка существующих стилей страниц
    """
    def __init__(self, dirlist):
        """
        dirlist - список директорий, где ищутся стили
        """
        # Список хранит пути до имеющихся проверенных стилей
        self.__styles = sorted(self.__findStyles(dirlist))

    def __len__(self):
        return len(self.__styles)

    def __getitem__(self, index):
        return self.__styles[index]

    def __findStyles(self, dirlist):
        """
        Поиск стилей в по путям в списке dirlist
        """
        styles = []
        for path in dirlist:
            styles += self.__findStylesInDir(path)

        return styles

    def __findStylesInDir(self, path):
        """
        Возвращает список стилей, найденных в директории path
        """
        if not os.path.exists(path):
            return []

        style = Style()
        return [os.path.join(path, styledir)
                for styledir in os.listdir(path)
                if (not styledir.startswith("__") and
                    style.check(os.path.join(path, styledir)))]
