# -*- coding: UTF-8 -*-

import re


class Section (object):
    """
    Класс для хранения информации об одном разделе
    """
    def __init__ (self, title, level, anchor):
        """
        title - заголовок раздела
        level - уровень вложенности (начиная с 1)
        anchor - имя якоря в заголовке (или пустая строка, если якоря нет)
        """
        self.title = title
        self.level = level
        self.anchor = anchor


class ContentsParser (object):
    """
    Класс для получения содержания по тексту
    """
    def __init__ (self):
        self.heading = re.compile (r'''(?:^|\n)
                (?P<header>!!+)\s+
                (?P<title>(\\\n|.)*?)\s*
                (?:\n|$)''',
                re.X | re.M)


    def parse (self, text):
        """
        Возвращает список экземпляров класса Section
        """
        text = self._prepareText (text)

        matches = self.heading.finditer (text)

        result = [self._makeSection (match) for match in matches]

        return result


    def _prepareText (self, text):
        """
        Предварительная обработка текста (вырезание участков, которые не должны учитываться при получении оглавления)
        """
        return text


    def _makeSection (self, match):
        title = match.group ("title")
        level = len (match.group ("header")) - 1
        anchor = u""

        return Section (title, level, anchor)
