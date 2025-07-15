# -*- coding: utf-8 -*-

import re
from typing import List, Tuple

from pyparsing import Regex, OneOrMore, Combine

from outwiker.pages.wiki.parser.utils import noConvert
from outwiker.pages.wiki.parser.tokenmultilineblock import MultilineBlockFactory
import outwiker.core.cssclasses as css


CSS_ID_STYLE_UNORDER_LIST = "ul.ow-wiki"
CSS_STYLE_UNORDER_LIST = """ul.ow-wiki {
            padding-left: 1rem;
            list-style-type: none;
        }

        ul.ow-wiki > li.ow-wiki:before {
          background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguMjQ4MjIgMCAwIC4yNDgwOCAtMi4zNzEzIC0yLjU0NzYpIj4KPGNpcmNsZSBjeD0iMTMuNTgxIiBjeT0iMTQuMjk5IiByPSIxIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iLjgxOSIvPgo8L2c+Cjwvc3ZnPgoK");
          background-position: 0.0 0.0em;
          background-size: 1.2em 1.2em;
          background-repeat: no-repeat;

          margin-right: 0px;
          content: "";
          height: 1.4em;
          width: 1.5em;
          vertical-align: middle;
          display: inline-block;
        }"""

CSS_STYLE_EMPTY = """ul.ow-wiki li.ow-li-empty:before { background-image: none; }"""
CSS_STYLE_TODO = """ul.ow-wiki li.ow-li-todo:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMS45ODU3bW0iIGhlaWdodD0iMS45ODU3bW0iIHZlcnNpb249IjEuMSIgdmlld0JveD0iMCAwIDEuOTg1NyAxLjk4NTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMi4xMDMgLTEyLjgzNykiPgo8cmVjdCB4PSIxMi4zNDUiIHk9IjEzLjA3OSIgd2lkdGg9IjEuNTE2NCIgaGVpZ2h0PSIxLjUxNjQiIGZpbGw9Im5vbmUiIGltYWdlLXJlbmRlcmluZz0iYXV0byIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9Ii4xODM2MiIvPgo8L2c+Cjwvc3ZnPgoK"); }"""
CSS_STYLE_INCOMPLETE = """ul.ow-wiki li.ow-li-incomplete:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMS45ODU3bW0iIGhlaWdodD0iMS45ODU3bW0iIHZlcnNpb249IjEuMSIgdmlld0JveD0iMCAwIDEuOTg1NyAxLjk4NTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMi4xMDMgLTEyLjgzNykiPgo8cmVjdCB4PSIxMi4zNDUiIHk9IjEzLjA3OSIgd2lkdGg9IjEuNTE2NCIgaGVpZ2h0PSIxLjUxNjQiIGZpbGw9Im5vbmUiIGltYWdlLXJlbmRlcmluZz0iYXV0byIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9Ii4xODM2MiIvPgo8L2c+CjxwYXRoIGQ9Im0xLjc1ODUgMC4yNDQwMS0xLjQ4MDkgMS40ODkzIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iLjE4Ii8+Cjwvc3ZnPgo="); }"""
CSS_STYLE_COMPLETE = """ul.ow-wiki li.ow-li-complete:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMS45ODU3bW0iIGhlaWdodD0iMS45ODU3bW0iIHZlcnNpb249IjEuMSIgdmlld0JveD0iMCAwIDEuOTg1NyAxLjk4NTciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMi4xMDMgLTEyLjgzNykiPgo8cmVjdCB4PSIxMi4zNDUiIHk9IjEzLjA3OSIgd2lkdGg9IjEuNTE2NCIgaGVpZ2h0PSIxLjUxNjQiIGZpbGw9Im5vbmUiIGltYWdlLXJlbmRlcmluZz0iYXV0byIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9Ii4xODM2MiIvPgo8L2c+CjxwYXRoIGQ9Im0wLjI2OTI1IDAuMjY5MjUgMS40NzI0IDEuNDcyNCIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9Ii4xOCIvPgo8cGF0aCBkPSJtMS43NTg1IDAuMjQ0MDEtMS40ODA5IDEuNDg5MyIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9Ii4xOCIvPgo8L3N2Zz4K"); }"""
CSS_STYLE_STAR = """ul.ow-wiki li.ow-li-star:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjAwNTMgMCAwIC45NDEwMSAtMTIuMTg5IC0xMi4wMzcpIiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iLjIiPgo8cGF0aCBkPSJtMTMuMTIxIDEzLjE2NHYxLjM4MTUiLz4KPHBhdGggZD0ibTEzLjcxOSAxMy41MDktMS4xOTY0IDAuNjkwNzYiLz4KPHBhdGggZD0ibTEzLjcxOSAxNC4yLTEuMTk2NC0wLjY5MDc2Ii8+CjwvZz4KPC9zdmc+Cgo="); }"""
CSS_STYLE_PLUS = """ul.ow-wiki li.ow-li-plus:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguNiAwIDAgMSAtNy4wNTMyIC0xMi42NjMpIiBzdHJva2Utd2lkdGg9Ii4xOTM2NSI+CjxwYXRoIGQ9Im0xMi40MjIgMTMuNjYzaDIiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMTkzNjUiLz4KPC9nPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCgwIC42IC0xIDAgMTQuNjYzIC03LjA1MzIpIiBzdHJva2Utd2lkdGg9Ii4xOTM2NSI+CjxwYXRoIGQ9Im0xMi40MjIgMTMuNjYzaDIiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMTkzNjUiLz4KPC9nPgo8L3N2Zz4K"); }"""
CSS_STYLE_MINUS = """ul.ow-wiki li.ow-li-minus:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguNiAwIDAgMSAtNy4wNTMyIC0xMi42NjMpIiBzdHJva2Utd2lkdGg9Ii4xOTM2NSI+CjxwYXRoIGQ9Im0xMi40MjIgMTMuNjYzaDIiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMTkzNjUiLz4KPC9nPgo8L3N2Zz4K"); }"""
CSS_STYLE_CIRCLE = """ul.ow-wiki li.ow-li-circle:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguMzMzNDUgMCAwIC4zMjQ0OSAtMy41Mjg1IC0zLjY1MDUpIiBmaWxsPSJub25lIj4KPGNpcmNsZSBjeD0iMTMuNTgxIiBjeT0iMTQuMjk5IiByPSIxIiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iLjQiLz4KPC9nPgo8L3N2Zz4K"); }"""
CSS_STYLE_CHECK = """ul.ow-wiki li.ow-li-check:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguNzUwMSAwIDAgLjc5ODkgLTkuMTA2NSAtOS45MTc4KSI+CjxwYXRoIGQ9Im0xMi42MTcgMTMuNDA1IDAuNTk4NzcgMS4wMjM0IDEuMTIyNi0xLjY5MzIiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMjU1cHgiLz4KPC9nPgo8L3N2Zz4K"); }"""
CSS_STYLE_LT = """ul.ow-wiki li.ow-li-lt:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCguNzMyMTcgMCAwIC42NTA2MyAtOC41ODM5IC04LjAzODkpIj4KPHBhdGggZD0ibTEzLjg2OSAxMy4yODQtMS4zNzU0IDAuNTU2NzIgMS4zNzY5IDAuNjUxMjkiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMTc5NDdweCIvPgo8L2c+Cjwvc3ZnPgo="); }"""
CSS_STYLE_GT = """ul.ow-wiki li.ow-li-gt:before { background-image: url("data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMm1tIiBoZWlnaHQ9IjJtbSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMiAyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyB0cmFuc2Zvcm09Im1hdHJpeCgtLjczMjE3IDAgMCAtLjY1MDYzIDEwLjU4NCAxMC4wMzIpIj4KPHBhdGggZD0ibTEzLjg2OSAxMy4yODQtMS4zNzU0IDAuNTU2NzIgMS4zNzY5IDAuNjUxMjkiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSIuMTc5NDdweCIvPgo8L2c+Cjwvc3ZnPgo="); }"""


class ListFactory:
    @staticmethod
    def make(parser):
        return ListToken(parser).getToken()


class ListParams:
    """
    Параметры списков в парсере
    """

    def __init__(self, symbol, startTag, endTag):
        self.symbol = symbol
        self.startTag = startTag
        self.endTag = endTag


class ListToken:
    """
    Класс для разбора списков
    """
    unorderList = "*"
    orderList = "#"

    unorderListCSS = [
            ('[]', css.CSS_LIST_ITEM_EMPTY, CSS_STYLE_EMPTY),
            ('[ ]', css.CSS_LIST_ITEM_TODO, CSS_STYLE_TODO),
            ('[/]', css.CSS_LIST_ITEM_INCOMPLETE, CSS_STYLE_INCOMPLETE),
            ('[\\]', css.CSS_LIST_ITEM_INCOMPLETE, CSS_STYLE_INCOMPLETE),
            ('[x]', css.CSS_LIST_ITEM_COMPLETE, CSS_STYLE_COMPLETE),
            ('[X]', css.CSS_LIST_ITEM_COMPLETE, CSS_STYLE_COMPLETE),
            ('[*]', css.CSS_LIST_ITEM_STAR, CSS_STYLE_STAR),
            ('[+]', css.CSS_LIST_ITEM_PLUS, CSS_STYLE_PLUS),
            ('[-]', css.CSS_LIST_ITEM_MINUS, CSS_STYLE_MINUS),
            ('[o]', css.CSS_LIST_ITEM_CIRCLE, CSS_STYLE_CIRCLE),
            ('[O]', css.CSS_LIST_ITEM_CIRCLE, CSS_STYLE_CIRCLE),
            ('[v]', css.CSS_LIST_ITEM_CHECK, CSS_STYLE_CHECK),
            ('[V]', css.CSS_LIST_ITEM_CHECK, CSS_STYLE_CHECK),
            ('[<]', css.CSS_LIST_ITEM_LT, CSS_STYLE_LT),
            ('[>]', css.CSS_LIST_ITEM_GT, CSS_STYLE_GT),
            ]

    def __init__(self, parser):
        self.allListsParams = [
            ListParams(ListToken.unorderList, f'<ul class="{css.CSS_WIKI}">', '</ul>'),
            ListParams(ListToken.orderList, f'<ol class="{css.CSS_WIKI}">', '</ol>'),
        ]

        self.parser = parser
        self._maxDepthLevel = 500
        self._blockToken = MultilineBlockFactory.make(
            self.parser).setParseAction(noConvert)

    def _addDeeperLevel(self, depth, item, currItem):
        """
        Создать список более глубокого уровня
        depth - разница между новым уровнем и текущим
        item - разобранный элемент строки
        currItem - список вложенных списков
            (их первых символов для определения типа)
        """
        result = self._getStartListTag(item[0], self.allListsParams) * depth
        for _ in range(depth):
            currItem.append(item[0])

        return result

    def _closeLists(self, depth, currItem):
        """
        Закрыть один или несколько уровней списков (перейти выше)
        depth - разность между текущим уровнем и новым урвонем
        """
        result = self._getEndListTag(currItem[-1], self.allListsParams) * depth
        for _ in range(depth):
            del currItem[-1]

        return result

    def _closeListStartList(self, level, item, currItem):
        result = ''

        result += self._closeLists(1, currItem)
        result += self._getStartListTag(item[0], self.allListsParams)
        currItem.append(item[0])

        result += self._getListItemTag(item, level)

        return result

    def _generateListForItems(self, items):
        currLevel = 0
        currItem = []

        result = ''

        for item in items:
            if len(item.strip()) == 0:
                continue

            level = self._getListLevel(item, self.allListsParams)
            if level > self._maxDepthLevel:
                level = self._maxDepthLevel

            if (level == currLevel and
                    len(currItem) > 0 and
                    item[0] == currItem[-1]):
                # Новый элемент в текущем списке
                result += self._getListItemTag(item, level)

            elif level > currLevel:
                # Более глубокий уровень
                result += self._addDeeperLevel(level -
                                                currLevel, item, currItem)
                result += self._getListItemTag(item, level)

            elif level < currLevel:
                # Более высокий уровень, но тот же тип списка
                result += self._closeLists(currLevel - level, currItem)

                if item[0] == currItem[-1]:
                    result += self._getListItemTag(item, level)
                else:
                    result += self._closeListStartList(level, item, currItem)

            elif level == currLevel and len(currItem) > 0 and item[0] != currItem[-1]:
                # Тот же уровень, но другой список
                result += self._closeListStartList(level, item, currItem)

            else:
                assert False

            currLevel = level

        result += self._closeLists(currLevel, currItem)

        return result

    def getToken(self):
        text = Regex(r"(?:\\\n|.)*?$", re.MULTILINE)
        line_break = Regex(r'\n{0,2}', re.MULTILINE)

        item = Combine(Regex(r'^(?:(?:\*+)|(?:#+))\s*', re.MULTILINE) +
                       (self._blockToken | text) +
                       line_break).leaveWhitespace()
        fullList = OneOrMore(item).setParseAction(self._convertList).ignoreWhitespace(False)("list")

        return fullList

    def _convertList(self, s, loc, tokens):
        """
        Преобразовать список элементов списка в HTML-список
        (возможно, вложенный)
        """
        return self._generateListForItems(tokens)

    def _getListLevel(self, item, params):
        """
        Получить уровень списка по его элементу
        (количество символов # и * в начале строки)
        """
        found = False
        for param in params:
            if item[0] == param.symbol:
                found = True
                break

        if not found:
            return 0

        level = 1
        while level < len(item) and item[level] == item[0]:
            level += 1

        return level

    def _getListItemTag(self, item: str, level: int) -> str:
        text = (item[level:]).strip()
        css_classes = [css.CSS_WIKI]

        if item[level - 1] == self.unorderList:
            # Find classes for unorder lists
            text, other_css = self._processUnorderClasses(text)
            css_classes += other_css
            self.parser.addStyle(CSS_ID_STYLE_UNORDER_LIST, CSS_STYLE_UNORDER_LIST)

        itemText = self.parser.parseListItemMarkup(text)
        return '<li class="{css_class}">{text}</li>'.format(text=itemText, css_class=' '.join(css_classes))

    def _processUnorderClasses(self, text) -> Tuple[str, List[str]]:
        result_text = text
        classes: List[str] = []

        for prefix, css_class, css_style in self.unorderListCSS:
            if text.startswith(prefix):
                result_text = text[len(prefix):].strip()
                classes.append(css_class)
                self.parser.addStyle(css_class, css_style)
                break

        return (result_text, classes)

    def _getStartListTag(self, symbol, params):
        """
        Получить открывающийся тег для элемента
        """
        for listparam in params:
            if listparam.symbol == symbol:
                return listparam.startTag

    def _getEndListTag(self, symbol, params):
        """
        Получить закрывающийся тег для элемента
        """
        for listparam in params:
            if listparam.symbol == symbol:
                return listparam.endTag
