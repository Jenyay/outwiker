# -*- coding: UTF-8 -*-

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.application import Application


class FactorySelector (object):
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
    def getFactories ():
        return FactorySelector._factories.values()


    @staticmethod
    def getFactory (pageType):
        """
        Найти фабрику, которая работает с переданным типом страницы (со страницей данного типа).
        Или вернуть фабрику по умолчанию
        """
        return FactorySelector._factories.get (pageType, FactorySelector._defaultFactory)


    @staticmethod
    def reset ():
        """
        Установить словарь фабрик в первоначальное состояние. Используется для тестирования.
        Это не конструктор. В случае изменения списка фабрик, установленных по умолчанию, нужно изменять этот метод.
        """
        FactorySelector._factories = {factory.getTypeString(): factory
                                      for factory
                                      in [WikiPageFactory(),
                                          HtmlPageFactory(),
                                          TextPageFactory(),
                                          SearchPageFactory()]}

        Application.onPageFactoryListChange (newfactory = None)


    @staticmethod
    def addFactory (newFactory):
        """
        Добавить новую фабрику. При этом у фабрики может быть новый создаваемый тип страниц, в то же время фабрика может заменить существующую фабрику.
        """
        FactorySelector._factories[newFactory.getTypeString()] = newFactory
        Application.onPageFactoryListChange (newfactory = newFactory)


    @staticmethod
    def removeFactory (typeString):
        """
        Удаляет фабрику из словаря
        """
        FactorySelector._factories.pop (typeString, None)
        Application.onPageFactoryListChange (newfactory = None)
