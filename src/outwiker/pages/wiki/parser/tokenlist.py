# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Regex, OneOrMore
from outwiker.pages.wiki.parser.utils import noConvert
import re


class ListFactory (object):
    @staticmethod
    def make (parser):
        return ListToken (parser).getToken()


class ListParams (object):
    """
    Параметры списков в парсере
    """
    def __init__ (self, symbol, startTag, endTag):
        self.symbol = symbol
        self.startTag = startTag
        self.endTag = endTag


class ListToken (object):
    """
    Класс для разбора списков
    """
    unorderList = "*"
    orderList = "#"

    def __init__ (self, parser):
        self.allListsParams = [ListParams (ListToken.unorderList, u"<ul>", u"</ul>"),
                               ListParams (ListToken.orderList, u"<ol>", u"</ol>")]
        self.parser = parser


    def __addDeeperLevel (self, depth, item, currItem):
        """
        Создать список более глубокого уровня
        depth - разница между новым уровнем и текущим
        item - разобранный элемент строки
        currItem - список вложенных списков (их первых символов для определения типа)
        """
        result = u""
        for _ in range (depth):
            result += self.__getStartListTag(item[0], self.allListsParams)
            currItem.append (item[0])

        return result


    def __closeLists (self, depth, currItem):
        """
        Закрыть один или несколько уровней списков (перейти выше)
        depth - разность между текущим уровнем и новым урвонем
        """
        result = u""
        for _ in range (depth):
            result += self.__getEndListTag(currItem[-1], self.allListsParams)
            del currItem[-1]

        return result


    def __closeListStartList (self, level, item, currItem):
        result = u""

        result += self.__closeLists (1, currItem)
        result += self.__getStartListTag(item[0], self.allListsParams)
        currItem.append (item[0])

        result += self.__getListItemTag (item, level)

        return result


    def __generateListForItems (self, items):
        currLevel = 0
        currItem = []

        result = u""

        for item in items:
            if len (item.strip()) == 0:
                continue

            level = self.__getListLevel (item, self.allListsParams)

            if level == currLevel and len (currItem) > 0 and item[0] == currItem[-1]:
                # Новый элемент в текущем списке
                result += self.__getListItemTag (item, level)

            elif level > currLevel:
                # Более глубокий уровень
                result += self.__addDeeperLevel (level - currLevel, item, currItem)
                result += self.__getListItemTag (item, level)

            elif level < currLevel:
                # Более высокий уровень, но тот же тип списка
                result += self.__closeLists (currLevel - level, currItem)

                if item[0] == currItem[-1]:
                    result += self.__getListItemTag (item, level)
                else:
                    result += self.__closeListStartList (level, item, currItem)

            elif level == currLevel and len (currItem) > 0 and item[0] != currItem[-1]:
                # Тот же уровень, но другой список
                result += self.__closeListStartList (level, item, currItem)

            else:
                assert False

            currLevel = level

        result += self.__closeLists (currLevel, currItem)

        return result


    def getToken (self):
        regex = "^(?P<level>["

        for param in self.allListsParams:
            regex += param.symbol

        regex += r"]+) *(?P<item>(?:\\\n|.)*?)$\n{0,2}"

        item = Regex (regex, re.MULTILINE).setParseAction (noConvert).leaveWhitespace()

        fullList = OneOrMore (item).setParseAction (self.__convertList)("list")

        return fullList


    def __convertList (self, s, loc, tokens):
        """
        Преобразовать список элементов списка в HTML-список (возможно, вложенный)
        """
        return self.__generateListForItems (tokens)


    def __getListLevel (self, item, params):
        """
        Получить уровень списка по его элементу (количество символов # и * в начале строки)
        """
        found = False
        for param in params:
            if item[0] == param.symbol:
                found = True
                break

        if not found:
            return 0

        level = 1
        while level < len (item) and item[level] == item[0]:
            level += 1

        return level


    def __getListItemTag (self, item, level):
        text = (item[level:]).strip()
        itemText = self.parser.parseListItemMarkup (text)

        return u"<li>%s</li>" % (itemText)


    def __getStartListTag (self, symbol, params):
        """
        Получить открывающийся тег для элемента
        """
        for listparam in params:
            if listparam.symbol == symbol:
                return listparam.startTag


    def __getEndListTag (self, symbol, params):
        """
        Получить закрывающийся тег для элемента
        """
        for listparam in params:
            if listparam.symbol == symbol:
                return listparam.endTag
