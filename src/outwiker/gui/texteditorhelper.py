# -*- coding: utf-8 -*-

import codecs

import wx.stc


class TextEditorHelper (object):
    def __init__(self):
        self.SPELL_ERROR_INDICATOR_MASK = wx.stc.STC_INDIC0_MASK

        self._encoder = codecs.getencoder("utf-8")

    def calcByteLen(self, text):
        """Посчитать длину строки в байтах, а не в символах"""
        return len(self._encoder(text)[0])

    def calcBytePos(self, text, pos):
        """Преобразовать позицию в символах в позицию в байтах"""
        return len(self._encoder(text[: pos])[0])

    @staticmethod
    def addStyle(stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет (с помощью операции побитового ИЛИ) стиль с идентификатором
        styleid к массиву байт stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [style | styleid for style in style_src]

        stylelist[bytepos_start: bytepos_end] = style_new

    @staticmethod
    def setStyle(stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву байт stylelist
        """
        stylelist[bytepos_start: bytepos_end] = [styleid] * (bytepos_end - bytepos_start)

    def setSpellError(self, stylelist, fullText, startpos, endpos):
        """
        Mark positions as error
        startpos, endpos - positions in characters
        """
        startbytes = self.calcBytePos(fullText, startpos)
        endbytes = self.calcBytePos(fullText, endpos)

        self.addStyle(stylelist,
                      self.SPELL_ERROR_INDICATOR_MASK,
                      startbytes,
                      endbytes)
