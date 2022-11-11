# -*- coding: utf-8 -*-

from outwiker.pages.wiki.parser.command import Command
import outwiker.core.cssclasses as css


class SimpleView:
    """
    Класс для простого представления списка дочерних страниц - каждая страница
    на отдельной строке
    """
    @staticmethod
    def make(children, parser, params):
        """
        children - список упорядоченных дочерних страниц
        """
        css_classes = '{} {}'.format(css.CSS_LINK, css.CSS_LINK_PAGE)
        template = '<a class="{css_classes}" href="page://{link}">{text}</a>\n'
        result = ''.join(
            [template.format(link=page.title, text=page.display_title, css_classes=css_classes)
                for page in children])

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

    def __init__(self, parser):
        Command.__init__(self, parser)

    @property
    def name(self):
        return u"childlist"

    def execute(self, params, content):
        params_dict = Command.parseParams(params)

        children = self.parser.page.children
        self._sortChildren(children, params_dict)

        return SimpleView.make(children, self.parser, params)

    def _sortByNameKey(self, page):
        return page.display_title.lower()

    def _sortByEditDate(self, page):
        return page.datetime

    def _sortByCreationDate(self, page):
        return page.creationdatetime

    def _sortByOrder(self, page):
        return page.order

    def _sortChildren(self, children, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        if "sort" not in params_dict:
            return

        sort = params_dict["sort"].lower()

        # Ключ - название сортировки,
        # значение - кортеж из (функция ключа сортировки, reverse)
        sortdict = {
            "name":             (self._sortByNameKey, False),
            "descendname":      (self._sortByNameKey, True),
            "order":            (self._sortByOrder, False),
            "descendorder":     (self._sortByOrder, True),
            "edit":             (self._sortByEditDate, False),
            "descendedit":      (self._sortByEditDate, True),
            "creation":         (self._sortByCreationDate, False),
            "descendcreation":  (self._sortByCreationDate, True),
        }

        if sort in sortdict:
            func, reverse = sortdict[sort]
            children.sort(key=func, reverse=reverse)
