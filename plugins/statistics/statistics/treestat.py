#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.tree import WikiDocument
from outwiker.core.tagslist import TagsList

from .pagestat import PageStat

class TreeStat (object):
    """
    Класс для сбора статистики по дереву
    """
    def __init__ (self, root):
        """
        root - страница, которая считается корневой
        """
        self._root = root

        # Список всех страниц. Испозуется для кеширования, чтобы каждый раз не формировать
        self._pageList = None


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


    @property
    def tagsCount (self):
        """
        Возвращает количество используемых тегов в дереве
        """
        tags = TagsList (self._root)
        return len (tags)


    @property
    def frequentTags (self):
        """
        Возвращает упорядоченный по количеству использований список кортежей вида: (имя тега, количество использований)
        """
        tags = TagsList (self._root)

        tagslist = [(tagName, len (tags[tagName])) for tagName in tags]
        tagslist.sort (key=lambda item: item[1], reverse=True)

        return tagslist


    @property
    def pageDate (self):
        """
        Возвращает список всех страниц, упорядоченный по дате изменения (новые страницы сверху)
        """
        pageList = self._getPageList (self._root)

        pageList.sort (key=lambda page: page.datetime, reverse=True)
        return pageList


    @property
    def pageContentLength (self):
        """
        Возвращает список всех страниц, упорядоченный по размеру содержимого (самые длинные заметки сверху).
        Возвращает список кортежей вида (страница, количество символов без пробела)
        """
        pageList = self._getPageList (self._root)

        def getLength (page):
            try:
                result = PageStat (page).symbolsNotWhiteSpaces
            except TypeError:
                result = 0

            return result

        pageList.sort (key=getLength, reverse=True)

        result = [(page, getLength (page)) for page in pageList]
        return result


    def _getPageList (self, root):
        """
        Получить список всех страниц, в том числе и вложенных
        """
        if not self._pageList:
            pageList = []
            self._getPageListIterate (self._root, pageList)
            self._pageList = pageList

        return self._pageList[:]


    def _getPageListIterate (self, root, pageList):
        pageList += root.children

        for child in root.children:
            self._getPageListIterate (child, pageList)


    def _getMaxDepth (self, depthList):
        """
        Возвращает список из страниц с наибольшим уровнем вложенности
        """
        if len (depthList) == 0:
            return []

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
