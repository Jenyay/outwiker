# -*- coding: utf-8 -*-

import re


class Section (object):
    """
    Класс для хранения информации об одном разделе
    """

    def __init__(self, title, level, anchor):
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

    def __init__(self):
        self.heading = re.compile(
            r'''
            ^(?P<anchor2>\[\[\#.*?\]\])?\s*
            ^(?P<header>!!+)\s+
            (?P<anchor1>\[\[\#.*?\]\])?\s*
            (?P<title>(\\\n|.)*?)\s*
            (?P<anchor3>\[\[\#.*?\]\])?\s*
            $''',
            re.X | re.M)

    def parse(self, text):
        """
        Возвращает список экземпляров класса Section
        """
        matches = self.heading.finditer(text)

        result = [self._makeSection(
            match) for match in matches if not self._inNoFormat(match, text)]

        return result

    def _inNoFormat(self, match, text):
        """
        Возвращает True, если найденный заголовок содержится внутри
            тегов [= ... =]
        """
        tags = [(u"[=", u"=]"),
                (u"[@", u"@]"),
                ]

        for start, end in tags:
            leftStart = text[: match.start()].rfind(start)
            leftEnd = text[: match.start()].rfind(end)

            rightEnd = text[match.end():].find(end)

            if (leftStart != -1 and rightEnd != -1 and
                    (leftEnd == -1 or leftEnd < leftStart)):
                return True

        return False

    def _makeSection(self, match):
        title = match.group("title")
        title = title.replace(u"\\\n", u"")

        level = len(match.group("header")) - 1
        anchor = match.group("anchor1")

        if anchor is None:
            anchor = match.group("anchor2")

        if anchor is None:
            anchor = match.group("anchor3")

        if anchor is None:
            anchor = u""
        else:
            # Вырежем символы, обозначающие якорь - [[# и ]]
            assert len(anchor) >= 5
            anchor = anchor[3: -2].strip()

        return Section(title, level, anchor)
