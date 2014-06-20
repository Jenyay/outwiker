# -*- coding: UTF-8 -*-

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


class FactorySelector (object):
    """
    Класс, который выбирает нужную фабрику для каждой страницы
    """
    factories = [WikiPageFactory(),
                 HtmlPageFactory(),
                 TextPageFactory(),
                 SearchPageFactory()]

    defaultFactory = TextPageFactory


    @staticmethod
    def getFactory (pageType):
        """
        Найти фабрику, которая работает с переданным типом страницы (со страницей данного типа).
        Или вернуть фабрику по умолчанию
        """
        selFactory = FactorySelector.defaultFactory

        for factory in FactorySelector.factories:
            if pageType == factory.getTypeString():
                selFactory = factory
                break

        return selFactory
