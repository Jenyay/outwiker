# -*- coding: UTF-8 -*-

import re


class StcStyle (object):
    """
    Набор свойст стиля для класса StyledTextCtrl
    """
    def __init__ (self, fore=u"#000000",
                  back=u"#FFFFFF",
                  bold=False,
                  italic=False,
                  underline=False):
        self.fore = fore
        self.back = back
        self.bold = bold
        self.italic = italic
        self.underline = underline


    def tostr (self):
        """
        Преобразовать набор параметров стиля в строку, как это принято в StyledTextCtrl (параметры разделяются запятыми)
        """
        items = []

        if len (self.fore) != 0:
            items.append (u"fore:{}".format (self.fore))

        if len (self.back) != 0:
            items.append (u"back:{}".format (self.back))

        if self.bold:
            items.append (u"bold")

        if self.italic:
            items.append ("italic")

        if self.underline:
            items.append (u"underline")

        return u",".join (items)


    @staticmethod
    def parse (string):
        """
        Создать класс StcStyle по ее строке представления.
        Возвращает None, если в строке представления есть ошибки
        """
        items = [item.strip() for item in string.split (",") if len (item.strip()) != 0]

        style = StcStyle()
        for item in items:
            if item.lower().startswith (u"fore:"):
                style.fore = item[len (u"fore:"):]
                continue

            if item.lower().startswith (u"back:"):
                style.back = item[len (u"back:"):]
                continue

            if item.lower() == u"bold":
                style.bold = True
                continue

            if item.lower() == u"italic":
                style.italic = True
                continue

            if item.lower() == u"underline":
                style.underline = True
                continue

            return None

        return style


    @staticmethod
    def checkColorString (string):
        """
        Возвращает True, если передаваемая строка имеет формат вида #RRGGBB
        """
        if len (string.strip()) != 7:
            return False

        return re.match (r"#[0-9a-f]{6}", string.strip().lower()) is not None
