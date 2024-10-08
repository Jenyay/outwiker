# -*- coding: utf-8 -*-

from outwiker.gui.unknownpagetype import UnknownPageTypeFactory


def addPageFactory(new_factory) -> None:
    FactorySelector.addFactory(new_factory)


def removePageFactory(pageTypeString: str) -> None:
    FactorySelector.removeFactory(pageTypeString)


class FactorySelector:
    """
    Класс, который выбирает нужную фабрику для каждой страницы
    """

    _factories = {}

    @staticmethod
    def getFactories():
        return sorted(FactorySelector._factories.values(), key=lambda x: x.title)

    @staticmethod
    def getFactory(page_type):
        """
        Найти фабрику, которая работает с переданным типом страницы
        (со страницей данного типа). Или вернуть фабрику по умолчанию
        """
        if page_type in FactorySelector._factories:
            return FactorySelector._factories[page_type]
        else:
            return UnknownPageTypeFactory(page_type)

    @staticmethod
    def reset():
        """
        Установить словарь фабрик в первоначальное состояние.
        Используется для тестирования.
        Это не конструктор. В случае изменения списка фабрик,
        установленных по умолчанию, нужно изменять этот метод.
        """
        FactorySelector._factories = {}

    @staticmethod
    def addFactory(new_factory):
        """
        Добавить новую фабрику. При этом у фабрики может быть новый
        создаваемый тип страниц, в то же время фабрика может заменить
        существующую фабрику.
        """
        FactorySelector._factories[new_factory.getPageTypeString()] = new_factory

    @staticmethod
    def removeFactory(typeString):
        """
        Удаляет фабрику из словаря
        """
        FactorySelector._factories.pop(typeString, None)
