#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx.stc

from outwiker.gui.texteditor import TextEditor
from parser.tokenfonts import FontsFactory
from parser.tokenheading import HeadingFactory
from parser.tokencommand import CommandFactory
from parser.tokenlink import LinkFactory


class WikiEditor (TextEditor):
    def __init__ (self, parent):
        self.STYLE_BOLD_ID = 1
        self.style_bold = "bold"

        self.STYLE_ITALIC_ID = 2
        self.style_italic = "italic"

        self.STYLE_LINK_ID = 4
        self.style_link = "fore:#0000FF,underline"

        self.STYLE_HEADING_ID = 126
        self.style_heading = "bold"

        self.STYLE_COMMAND_ID = 125
        self.style_command = "fore:#6A686B"

        self.STYLE_BOLD_ITALIC_ID = self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID
        self.style_bold_italic = "bold,italic"

        super (WikiEditor, self).__init__ (parent)

        self.bolded = FontsFactory.makeBold (None).setParseAction(lambda s, l, t: None).setResultsName ("bold")
        self.italic = FontsFactory.makeItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("italic")
        self.bold_italic = FontsFactory.makeBoldItalic (None).setParseAction(lambda s, l, t: None).setResultsName ("bold_italic")
        self.heading = HeadingFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("heading")
        self.command = CommandFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("command")
        self.link = LinkFactory.make (None).setParseAction(lambda s, l, t: None).setResultsName ("link")

        self.colorParser = self.command | self.bold_italic | self.bolded | self.italic | self.heading | self.link
        self.insideBlockParser = self.bold_italic | self.bolded | self.italic | self.link

        self.textCtrl.Bind (wx.EVT_IDLE, self.onStyleNeeded)
        # self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.onChange)

        self.__styleSet = False


    def setDefaultSettings (self):
        super (WikiEditor, self).setDefaultSettings()

        self.textCtrl.SetLexer (wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)
        self.textCtrl.SetStyleBits (7)

        self._setStyleDefault (self.STYLE_BOLD_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ID, self.style_bold)

        self._setStyleDefault (self.STYLE_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_ID, self.style_italic)

        self._setStyleDefault (self.STYLE_COMMAND_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_COMMAND_ID, self.style_command)

        self._setStyleDefault (self.STYLE_BOLD_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_ID, self.style_bold_italic)

        self._setStyleDefault (self.STYLE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_LINK_ID, self.style_link)

        self.textCtrl.StyleSetSize (self.STYLE_HEADING_ID, self.config.fontSize.value + 2)
        self.textCtrl.StyleSetFaceName (self.STYLE_HEADING_ID, self.config.fontName.value)
        self.textCtrl.StyleSetSpec (self.STYLE_HEADING_ID, self.style_heading)


    def _setStyleDefault (self, styleId):
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
        stylelist = [0] * textlength

        self._colorizeText (text, 0, textlength, self.colorParser, stylelist)

        stylebytes = "".join ([chr(byte) for byte in stylelist])

        self.textCtrl.StartStyling (0, 0xff)
        self.textCtrl.SetStyleBytes (textlength, stylebytes)

        self.__styleSet = True


    def _colorizeText (self, text, start, end, parser, stylelist):
        tokens = parser.scanString (text[start: end])

        for token in tokens:
            pos_start = token[1] + start
            pos_end = token[2] + start

            # Нас интересует позиция в байтах, а не в символах
            bytepos_start = self.calcBytePos (text, pos_start)
            bytepos_end = self.calcBytePos (text, pos_end)

            # Применим стиль
            if token[0].getName() == "bold":
                self._addStyle (stylelist, self.STYLE_BOLD_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, self.insideBlockParser, stylelist)
            elif token[0].getName() == "italic":
                self._addStyle (stylelist, self.STYLE_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 3, pos_end - 3, self.insideBlockParser, stylelist)
            elif token[0].getName() == "bold_italic":
                self._addStyle (stylelist, self.STYLE_BOLD_ITALIC_ID, bytepos_start, bytepos_end)
                self._colorizeText (text, pos_start + 4, pos_end - 4, self.insideBlockParser, stylelist)
            elif token[0].getName() == "heading":
                self._setStyle (stylelist, self.STYLE_HEADING_ID, bytepos_start, bytepos_end)
            elif token[0].getName() == "command":
                self._setStyle (stylelist, self.STYLE_COMMAND_ID, bytepos_start, bytepos_end)
            elif token[0].getName() == "link":
                self._setStyle (stylelist, self.STYLE_LINK_ID, bytepos_start, bytepos_end)


    def _addStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [style | styleid for style in style_src]
        
        stylelist[bytepos_start: bytepos_end] = style_new


    def _setStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву stylelist
        """
        stylelist[bytepos_start: bytepos_end] = [styleid] * (bytepos_end - bytepos_start)
