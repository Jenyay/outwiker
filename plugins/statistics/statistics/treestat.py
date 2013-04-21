#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.tree import WikiDocument


class TreeStat (object):
    """
    Класс для сбора статистики по дереву
    """
    def __init__ (self, root):
        """
        root - страница, которая считается корневой
        """
        self._root = root


    @property
    def pageCount (self):
        """
        Возвращает количество страниц в дереве
        """
        startcount = 0 if self._root.getTypeString() == WikiDocument.getTypeString() else 1
        return self._getChildCount (self._root) + startcount


    @property
    def maxDepth (self):
        """
        Возвращает список кортежей для страниц с максимальным уровнем вложенности. Кортежи состоят из двух элементов: уровень вложенности и ссылка на страницу
        """
        depthList = []
        self._getDepthList(self._root, depthList, 0)

        return self._getMaxDepth (depthList)


    def _getMaxDepth (self, depthList):
        """
        Возвращает список из страниц с наибольшим уровнем вложенности
        """
        maxDepth = max (depthList, key=lambda item: item[0])[0]

        maxDepthList = [item for item in depthList if item[0] == maxDepth]
        return maxDepthList


    def _getDepthList (self, root, depthList, currentDepth):
        """
        Получить список кортежей, состоящих из элементов: уровень вложенности и ссылка на страницу

        root - элемент, начиная с которого отсчитывается вложенность,
        depthList - заполняемый список кортежей
        currentDepth - уровень вложенности для корневого элемента root
        """
        if currentDepth != 0:
            depthList.append ((currentDepth, root))

        for child in root.children:
            self._getDepthList (child, depthList, currentDepth + 1)


    def _getChildCount (self, root):
        count = len (root)

        for child in root.children:
            count += self._getChildCount (child)

        return count
