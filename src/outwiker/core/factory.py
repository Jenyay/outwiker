# -*- coding: utf-8 -*-

import os.path
from abc import ABCMeta, abstractmethod
from typing import Callable, List

from .exceptions import ReadonlyException
from .tree import BasePage, WikiPage
from .treetools import getAlternativeTitle

# Functions to calculate new page order


def orderCalculatorTop(_parent: BasePage, _alias: str, _tags: List[str]) -> int:
    """Add a page to top of the siblings"""
    return 0


def orderCalculatorBottom(parent: BasePage, _alias: str, _tags: List[str]) -> int:
    """Add a page to bottom of the siblings"""
    return len(parent.children)


def orderCalculatorAlphabetically(
    parent: BasePage, alias: str, _tags: List[str]
) -> int:
    """Sort a page alias alphabetically"""
    order = len(parent.children)
    alias_lower = alias.lower()
    for n, page in enumerate(parent.children):
        if alias_lower < page.display_title.lower():
            order = n
            break

    return order


class PageFactory(metaclass=ABCMeta):
    """
    Класс для создания страниц
    """

    def create(
        self,
        parent: BasePage,
        alias: str,
        tags: List[str],
        order_calculator: Callable[
            [BasePage, str, List[str]], int
        ] = orderCalculatorBottom
    ) -> WikiPage:
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        if parent.readonly:
            raise ReadonlyException

        siblings = [child_page.title for child_page in parent.children]
        title = getAlternativeTitle(alias, siblings)
        path = os.path.join(parent.path, title)

        # page = self.createPage(parent, title, path)
        page = WikiPage(path, title, parent)
        order = order_calculator(parent, alias, tags)
        parent.addToChildren(page, order)

        try:
            page.initAfterCreating(tags)
        except Exception:
            parent.removeFromChildren(page)
            raise

        if title != alias:
            page.alias = alias

        page.setTypeString(self.getPageTypeString())
        return page

    @property
    @abstractmethod
    def title(self) -> str:
        """
        Название страницы, показываемое пользователю
        """
        raise NotImplementedError

    @abstractmethod
    def getPageView(self, parent, application):
        """Метод возвращает контрол,
        который будет отображать и редактировать страницу
        """
        raise NotImplementedError

    @abstractmethod
    def getPageTypeString(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def createPageAdapter(self, page):
        raise NotImplementedError
