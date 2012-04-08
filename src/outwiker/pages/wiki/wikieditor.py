#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx.stc

from outwiker.gui.texteditor import TextEditor
from parser.tokenfonts import FontsFactory

class WikiEditor (TextEditor):
    def __init__ (self, parent):
        self.STYLE_BOLD_ID = 1
        self.style_bold = "bold"

        self.STYLE_ITALIC_ID = 2
        self.style_italic = "italic"

        self.STYLE_BOLD_ITALIC_ID = self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID
        self.style_bold_italic = "bold,italic"

        self._stylelist = []

        super (WikiEditor, self).__init__ (parent)

        self.bolded = FontsFactory.makeBold (None).setParseAction(lambda s, l, t: None).setResultsName ("bold")
        self.italic = FontsFactory.makeItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("italic")
        self.bold_italic = FontsFactory.makeBoldItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("bold_italic")

        self.colorParser = self.bold_italic | self.bolded | self.italic 

        self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.onChange)

        self.__styleSet = False


    def setDefaultSettings (self):
        super (WikiEditor, self).setDefaultSettings()

        self.textCtrl.SetLexer (wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)
        self.textCtrl.SetStyleBits (7)

        self._setStyleDafault (self.STYLE_BOLD_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ID, self.style_bold)

        self._setStyleDafault (self.STYLE_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_ID, self.style_italic)

        self._setStyleDafault (self.STYLE_BOLD_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_ID, self.style_bold_italic)


    def _setStyleDafault (self, styleId):
        self.textCtrl.StyleSetSize (styleId, self.config.fontSize.value)
        self.textCtrl.StyleSetFaceName (styleId, self.config.fontName.value)


    def onChange (self, event):
        self.__styleSet = False


    def onStyleNeeded (self, event):
        if self.__styleSet:
            return

        # Табуляция в редакторе считается за несколько символов
        text = self.textCtrl.GetText().replace ("\t", " ")

        textlength = self.calcByteLen (text)
        self._stylelist = [0] * textlength

        self._colorizeText (text, 0, textlength, self.colorParser, self._stylelist)

        stylebytes = "".join ([chr(byte) for byte in self._stylelist])

        self.textCtrl.StartStyling (0, 0xff)
        self.textCtrl.SetStyleBytes (textlength, stylebytes)

        self.__styleSet = True


    def _colorizeText (self, text, start, end, parser, stylelist):
        tokens = self.colorParser.scanString (text[start: end])
        for token in tokens:
            pos_start = token[1] + start
            pos_end = token[2] + start

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self.calcBytePos (text, pos_start)
            bytepos_end = self.calcBytePos (text, pos_end)

            # Применим стиль
            if token[0].getName() == "bold":
                self._addStyle (stylelist, self.STYLE_BOLD_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, parser, stylelist)
            elif token[0].getName() == "italic":
                self._addStyle (stylelist, self.STYLE_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, parser, stylelist)
            elif token[0].getName() == "bold_italic":
                self._addStyle (stylelist, self.STYLE_BOLD_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 4, pos_end - 4, parser, stylelist)


    def _addStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [style | styleid for style in style_src]
        
        stylelist[bytepos_start: bytepos_end] = style_new
