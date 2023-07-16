# -*- coding: utf-8 -*-

import codecs


class TextEditorHelper:
    def calcByteLen(self, text: str) -> int:
        """Посчитать длину строки в байтах, а не в символах"""
        result = len(codecs.encode(text, errors="replace"))
        return result

    def calcBytePos(self, text: str, pos: int) -> int:
        """Преобразовать позицию в символах в позицию в байтах"""
        return self.calcByteLen(text[:pos])

    @staticmethod
    def addStyle(stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет (с помощью операции побитового ИЛИ) стиль с идентификатором
        styleid к массиву байт stylelist
        """
        style_src = stylelist[bytepos_start:bytepos_end]
        style_new = [style | styleid for style in style_src]

        stylelist[bytepos_start:bytepos_end] = style_new

    @staticmethod
    def setStyle(stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву байт stylelist
        """
        stylelist[bytepos_start:bytepos_end] = [styleid] * (bytepos_end - bytepos_start)
