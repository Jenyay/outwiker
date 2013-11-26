#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from command import Command


class SimpleView (object):
    """
    Класс для простого представления списка дочерних страниц - каждая страница на отдельной строке
    """
    @staticmethod
    def make (children, parser, params):
        """
        children - список упорядоченных дочерних страниц
        """
        template = u'<a href="{link}">{title}</a>\n'
        result = u"".join ([template.format (link=page.title, title=page.title) for page in children ] )

        # Выкинем последний перевод строки
        return result[: -1]


class ChildListCommand (Command):
    """
    Команда для вставки списка дочерних команд. 
    Синтсаксис: (:childlist [params...]:)
    Параметры:
        sort=name - сортировка по имени
        sort=descendname - сортировка по имени в обратном направлении
        sort=descendorder - сортировка по положению страницы в обратном порядке
    """
    def __init__ (self, parser):
        Command.__init__ (self, parser)

    @property
    def name (self):
        return u"childlist"


    def execute (self, params, content):
        params_dict = Command.parseParams (params)

        children = self.parser.page.children
        self._sortChildren (children, params_dict)

        return SimpleView.make (children, self.parser, params)


    @staticmethod
    def _sortByName (page1, page2):
        if page1.title.lower() > page2.title.lower():
            return 1
        elif page1.title.lower() < page2.title.lower():
            return -1
        return 0


    def _sortChildren (self, children, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        if "sort" not in params_dict:
            return

        sort = params_dict["sort"].lower()

        if sort == "name":
            children.sort (ChildListCommand._sortByName)
        if sort == "descendname":
            children.sort (ChildListCommand._sortByName, reverse=True)
        if sort == "descendorder":
            children.reverse()
