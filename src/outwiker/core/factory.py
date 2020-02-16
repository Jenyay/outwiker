# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import os.path

from .exceptions import ReadonlyException
from .tree_commands import getAlternativeTitle


class PageFactory(metaclass=ABCMeta):
    """
    Класс для создания страниц
    """

    def create(self, parent, alias, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        if parent.readonly:
            raise ReadonlyException

        siblings = [child_page.title for child_page in parent.children]
        title = getAlternativeTitle(alias, siblings)
        path = os.path.join(parent.path, title)

        pageType = self.getPageType()
        page = pageType(path, title, parent)
        parent.addToChildren(page)

        try:
            page.initAfterCreating(tags)
        except Exception:
            parent.removeFromChildren(page)
            raise

        if title != alias:
            page.alias = alias

        return page

    @abstractmethod
    def getPageType(self):
        """
        Метод возвращает тип создаваемой страницы (не экземпляр страницы)
        """

    @abstractproperty
    def title(self):
        """
        Название страницы, показываемое пользователю
        """

    @abstractmethod
    def getPageView(self, parent, application):
        """
        Метод возвращает контрол,
        который будет отображать и редактировать страницу
        """

    def getTypeString(self):
        return self.getPageType().getTypeString()
