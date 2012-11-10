#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Стратегии для сортировки результатов поиска
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from outwiker.core.sortfunctions import sortAlphabeticalFunction, sortDateFunction


def getSortStrategies ():
    """
    Возвращает список существующих стратегий сортировок
    """
    return [TitleAlphabeticalSort(),
            TitleAlphabeticalInverseSort(),
            DateDescendingSort(),
            DateAscendingSort()]


class BaseSortStrategy (object):
    """
    Базовый абстрактрый класс для стратегий сортировки
    """
    __metaclass__ = ABCMeta
    

    @abstractmethod
    def sort (self, page1, page2):
        """
        Функция для сортировки
        """
        pass


    @abstractproperty
    def title (self):
        """
        Название стратегии в списке сортировок
        """
        pass


class TitleAlphabeticalSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по заголовку по алфавиту
    """
    def sort (self, page1, page2):
        return sortAlphabeticalFunction (page1, page2)


    @property
    def title (self):
        return _(u"Title")


class TitleAlphabeticalInverseSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по заголовку по алфавиту наоборот
    """
    def sort (self, page1, page2):
        return sortAlphabeticalFunction (page2, page1)


    @property
    def title (self):
        return _(u"Title (inverse)")


class DateDescendingSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по дате (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortDateFunction (page2, page1)


    @property
    def title (self):
        return _(u"Date (newest first)")


class DateAscendingSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по дате (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortDateFunction (page1, page2)


    @property
    def title (self):
        return _(u"Date (oldest first)")
