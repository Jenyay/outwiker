# -*- coding: utf-8 -*-

import re


class StcStyle(object):
    """
    Набор свойств стиля для класса StyledTextCtrl
    """

    def __init__(
        self, fore="#000000", back="#FFFFFF", bold=False, italic=False, underline=False
    ):
        self.fore = fore
        self.back = back
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def tostr(self):
        """
        Преобразовать набор параметров стиля в строку, как это принято в
            StyledTextCtrl (параметры разделяются запятыми)
        """
        items = []

        if len(self.fore) != 0:
            items.append("fore:{}".format(self.fore))

        if len(self.back) != 0:
            items.append("back:{}".format(self.back))

        if self.bold:
            items.append("bold")

        if self.italic:
            items.append("italic")

        if self.underline:
            items.append("underline")

        return ",".join(items)

    @staticmethod
    def parse(string):
        """
        Создать класс StcStyle по ее строке представления.
        Возвращает None, если в строке представления есть ошибки
        """
        items = [item.strip() for item in string.split(",") if len(item.strip()) != 0]

        style = StcStyle()
        for item in items:
            if item.lower().startswith("fore:"):
                style.fore = item[len("fore:") :]
                continue

            if item.lower().startswith("back:"):
                style.back = item[len("back:") :]
                continue

            if item.lower() == "bold":
                style.bold = True
                continue

            if item.lower() == "italic":
                style.italic = True
                continue

            if item.lower() == "underline":
                style.underline = True
                continue

            return None

        return style

    @staticmethod
    def checkColorString(string):
        """
        Возвращает True, если передаваемая строка имеет формат вида #RRGGBB
        """
        if len(string.strip()) != 7:
            return False

        return re.match(r"#[0-9a-f]{6}", string.strip().lower()) is not None
