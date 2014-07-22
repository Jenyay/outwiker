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
        result = u"".join ([template.format (link=page.title, title=page.title) for page in children])

        # Выкинем последний перевод строки
        return result[: -1]


class ChildListCommand (Command):
    """
    Команда для вставки списка дочерних команд.
    Синтсаксис: (:childlist [params...]:)
    Параметры:
        sort=name - сортировка по имени
        sort=descendname - сортировка по имени в обратном порядке
        sort=descendorder - сортировка по положению страницы в обратном порядке
        sort=edit - сортировка по дате редактирования
        sort=descendedit - сортировка по дате редактирования в обратном порядке
        sort=creation - сортировка по дате создания
        sort=descendcreation - сортировка по дате создания в обратном порядке
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


    def _sortByNameKey (self, page):
        return page.title.lower()


    def _sortByEditDate (self, page):
        return page.datetime


    def _sortByCreationDate (self, page):
        return page.creationdatetime


    def _sortByOrder (self, page):
        return page.order


    def _sortChildren (self, children, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        if "sort" not in params_dict:
            return

        sort = params_dict["sort"].lower()

        # Ключ - название сортировки,
        # значение - кортеж из (функция ключа сортировки, reverse)
        sortdict = {
            u"name":             (self._sortByNameKey, False),
            u"descendname":      (self._sortByNameKey, True),
            u"order":            (self._sortByOrder, False),
            u"descendorder":     (self._sortByOrder, True),
            u"edit":             (self._sortByEditDate, False),
            u"descendedit":      (self._sortByEditDate, True),
            u"creation":         (self._sortByCreationDate, False),
            u"descendcreation":  (self._sortByCreationDate, True),
        }

        if sort in sortdict:
            func, reverse = sortdict[sort]
            children.sort (key = func, reverse = reverse)
