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

        self._stylelist = []

        super (WikiEditor, self).__init__ (parent)

        self.bolded = FontsFactory.makeBold (None).setParseAction(lambda s, l, t: None).setResultsName ("bold")
        self.italic = FontsFactory.makeItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("italic")

        self.colorParser = self.bolded | self.italic

        self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.onChange)

        self.__styleSet = False

    
    # def _applyBoldStyle (self, s, loc, toks):
        # text = self.textCtrl.GetText()

        # bytepos_start = self.calcBytePos (text, loc)
        # byte_len = self.calcByteLen (toks[0])
        # bytepos_end = bytepos_start + byte_len

        # self._stylelist[bytepos_start: bytepos_end] = [self.STYLE_BOLD_ID] * byte_len
        # print "_applyBoldStyle start"
        # print loc
        # print toks
        # print "_applyBoldStyle end"
        # pass



    def setDefaultSettings (self):
        super (WikiEditor, self).setDefaultSettings()

        self.textCtrl.SetLexer (wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)
        self.textCtrl.SetStyleBits (7)

        self._setStyleDafault (self.STYLE_BOLD_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ID, self.style_bold)

        self._setStyleDafault (self.STYLE_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_ID, self.style_italic)


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

        # tmp = self.colorParser.searchString (text)
        tmp = self.colorParser.scanString (text)
        # print tmp
        for item in tmp:
            pos_start = item[1]
            pos_end = item[2]

            # print item[0]

            # print "for start"
            # print item[0].getName()
            # print item[1]
            # print item[2]
            # print "for end"
            # print 

            # # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self.calcBytePos (text, pos_start)
            bytepos_end = self.calcBytePos (text, pos_end)
            text_byte_len = bytepos_end - bytepos_start

            # Применим стиль
            if item[0].getName() == "bold":
                self._stylelist[bytepos_start: bytepos_end] = [self.STYLE_BOLD_ID] * text_byte_len
            elif item[0].getName() == "italic":
                self._stylelist[bytepos_start: bytepos_end] = [self.STYLE_ITALIC_ID] * text_byte_len
            # pass

        stylebytes = "".join ([chr(byte) for byte in self._stylelist])

        self.textCtrl.StartStyling (0, 0xff)
        self.textCtrl.SetStyleBytes (textlength, stylebytes)

        self.__styleSet = True
