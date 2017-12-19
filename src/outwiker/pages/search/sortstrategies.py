# -*- coding: UTF-8 -*-
"""
Стратегии для сортировки результатов поиска
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from outwiker.core.sortfunctions import sortAlphabeticalFunction, sortDateFunction, sortCreationDateFunction


def getSortStrategies ():
    """
    Возвращает список существующих стратегий сортировок
    """
    return [TitleAlphabeticalSort(),
            TitleAlphabeticalInverseSort(),
            DateDescendingSort(),
            DateAscendingSort(),
            CreationDateDescendingSort(),
            CreationDateAscendingSort()]


class BaseSortStrategy (object, metaclass=ABCMeta):
    """
    Базовый абстрактрый класс для стратегий сортировки
    """

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
    Стратегия для сортировки страниц по дате последней правки (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortDateFunction (page2, page1)


    @property
    def title (self):
        return _(u"Changing date (newest first)")


class DateAscendingSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по дате последней правки (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortDateFunction (page1, page2)


    @property
    def title (self):
        return _(u"Changing date (oldest first)")


class CreationDateDescendingSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по дате создания (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortCreationDateFunction (page2, page1)


    @property
    def title (self):
        return _(u"Creation date (newest first)")


class CreationDateAscendingSort (BaseSortStrategy):
    """
    Стратегия для сортировки страниц по дате создания (сверху - самые новые)
    """
    def sort (self, page1, page2):
        return sortCreationDateFunction (page1, page2)


    @property
    def title (self):
        return _(u"Creation date (oldest first)")
