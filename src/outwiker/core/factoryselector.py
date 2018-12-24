# -*- coding: utf-8 -*-

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


class FactorySelector(object):
    """
    Класс, который выбирает нужную фабрику для каждой страницы
    """
    _defaultFactory = TextPageFactory()

    _factories = {factory.getTypeString(): factory
                  for factory
                  in [WikiPageFactory(),
                      HtmlPageFactory(),
                      TextPageFactory(),
                      SearchPageFactory()]}

    @staticmethod
    def getFactories():
        return sorted(FactorySelector._factories.values(),
                      key=lambda x: x.title)

    @staticmethod
    def getFactory(page_type):
        """
        Найти фабрику, которая работает с переданным типом страницы
        (со страницей данного типа). Или вернуть фабрику по умолчанию
        """
        return FactorySelector._factories.get(page_type,
                                              FactorySelector._defaultFactory)

    @staticmethod
    def reset():
        """
        Установить словарь фабрик в первоначальное состояние.
        Используется для тестирования.
        Это не конструктор. В случае изменения списка фабрик,
        установленных по умолчанию, нужно изменять этот метод.
        """
        FactorySelector._factories = {factory.getTypeString(): factory
                                      for factory
                                      in [WikiPageFactory(),
                                          HtmlPageFactory(),
                                          TextPageFactory(),
                                          SearchPageFactory()]}

    @staticmethod
    def addFactory(new_factory):
        """
        Добавить новую фабрику. При этом у фабрики может быть новый
        создаваемый тип страниц, в то же время фабрика может заменить
        существующую фабрику.
        """
        FactorySelector._factories[new_factory.getTypeString()] = new_factory

    @staticmethod
    def removeFactory(typeString):
        """
        Удаляет фабрику из словаря
        """
        FactorySelector._factories.pop(typeString, None)
