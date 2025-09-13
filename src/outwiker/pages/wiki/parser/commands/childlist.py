# -*- coding: utf-8 -*-

from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parser.htmlelements import create_link_to_page
import outwiker.core.cssclasses as css
from outwiker.pages.wiki.parser.wikiparser import Parser


CSS_ID_STYLES = css.CSS_CHILD_LIST
CSS_STYLES = """ul.ow-child-list {
		  padding-left: 1rem;
          list-style-type: none;
		}

		ul.ow-child-list ul {
		  margin-left: 15px;
		  padding-left: 10px;
		  border-left: 1px dashed #ddd;
		}

        li.ow-child-list-item:before {
		  content: "";
		  padding-left: 1.5em;
          background-position: 0.0em 0.1em;
          background-size: auto 1.0em;
          background-repeat: no-repeat;
          height: 1.6em;
          background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/PjxzdmcgaWQ9IklDT04iIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDojYjBjYmUwO30uY2xzLTEsLmNscy0ye3N0cm9rZTojNjY2NjdlO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2Utd2lkdGg6MTVweDt9LmNscy0ye2ZpbGw6IzVmOWNjYjt9PC9zdHlsZT48L2RlZnM+PHRpdGxlLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0zOTEsMTU4LjV2MjY1YTI1LDI1LDAsMCwxLTI1LDI1SDE0NmEyNSwyNSwwLDAsMS0yNS0yNVY4OC41YTI1LDI1LDAsMCwxLDI1LTI1SDI5NloiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0zOTEsMTU4LjVIMzIxYTI1LDI1LDAsMCwxLTI1LTI1di03MFoiLz48L3N2Zz4=");
		}

        span.ow-child-list-title {
		  font-weight: bold;
        }

        span.ow-child-list-title:before {
		  margin-right: 0px;
		  content: "";
		  height: 1.8em;
		  vertical-align: middle;
		  width: 1.5em;
		  background-repeat: no-repeat;
		  display: inline-block;
		  background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/PjxzdmcgaWQ9IklDT04iIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDojYjBjYmUwO30uY2xzLTEsLmNscy0ye3N0cm9rZTojNjY2NjdlO3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtzdHJva2Utd2lkdGg6MTVweDt9LmNscy0ye2ZpbGw6IzVmOWNjYjt9PC9zdHlsZT48L2RlZnM+PHRpdGxlLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0zOTEsMTU4LjV2MjY1YTI1LDI1LDAsMCwxLTI1LDI1SDE0NmEyNSwyNSwwLDAsMS0yNS0yNVY4OC41YTI1LDI1LDAsMCwxLDI1LTI1SDI5NloiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0zOTEsMTU4LjVIMzIxYTI1LDI1LDAsMCwxLTI1LTI1di03MFoiLz48L3N2Zz4=");
		  background-position: center center;
		  background-size: 75% auto;
		}"""


class SimpleView:
    """
    Класс для простого представления списка дочерних страниц - каждая страница
    на отдельной строке
    """
    @staticmethod
    def make(title: str, children, parser: Parser, params) -> str:
        """
        children - список упорядоченных дочерних страниц
        """
        if not children:
            return ''

        links = [create_link_to_page('page://{}'.format(page.title),
                                     page.display_title)
                for page in children]
        items = [f'<li class="{css.CSS_CHILD_LIST_ITEM}">{link}</li>'
                 for link in links]
        all_items_str = ''.join(items)
        result = f'<ul class="{css.CSS_CHILD_LIST}"><span class="{css.CSS_CHILD_LIST_TITLE}">{title}</span><ul class="{css.CSS_CHILD_LIST}">{all_items_str}</ul></ul>'

        parser.addStyle(CSS_ID_STYLES, CSS_STYLES)
        return result


class ChildListCommand(Command):
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
        return "childlist"

    def execute(self, params, content):
        params_dict = Command.parseParams(params)

        children = self.parser.page.children
        title = self.parser.page.display_title
        self._sortChildren(children, params_dict)

        return SimpleView.make(title, children, self.parser, params)

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
