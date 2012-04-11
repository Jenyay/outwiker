#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx.stc

from outwiker.gui.texteditor import TextEditor
from .wikicolorizer import WikiColorizer, EVT_APPLY_STYLE

# Событие вызывается с помощью PostEvent для потокобезопасного применения стилей к редактору


class WikiEditor (TextEditor):
    def __init__ (self, parent):
        self.STYLE_BOLD_ID = 1
        self.style_bold = "bold"

        self.STYLE_ITALIC_ID = 2
        self.style_italic = "italic"

        self.STYLE_UNDERLINE_ID = 4
        self.style_underline = "underline"

        self.STYLE_LINK_ID = 8
        self.style_link = "fore:#0000FF,underline"

        self.STYLE_HEADING_ID = 126
        self.style_heading = "bold"

        self.STYLE_COMMAND_ID = 125
        self.style_command = "fore:#6A686B"

        # Комбинации стилей
        self.STYLE_BOLD_ITALIC_UNDERLINE_ID = (self.STYLE_BOLD_ID | 
                self.STYLE_ITALIC_ID | 
                self.STYLE_UNDERLINE_ID)
        self.style_bold_italic_underline = "bold,italic,underline"

        self.STYLE_BOLD_ITALIC_ID = self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID
        self.style_bold_italic = "bold,italic"

        self.STYLE_BOLD_UNDERLINE_ID = self.STYLE_BOLD_ID | self.STYLE_UNDERLINE_ID
        self.style_bold_underline = "bold,underline"

        self.STYLE_ITALIC_UNDERLINE_ID = self.STYLE_ITALIC_ID | self.STYLE_UNDERLINE_ID
        self.style_italic_underline = "italic,underline"


        self.STYLE_BOLD_ITALIC_UNDERLINE_LINK_ID = (self.STYLE_BOLD_ID | 
                self.STYLE_ITALIC_ID |
                self.STYLE_UNDERLINE_ID |
                self.STYLE_LINK_ID )
        self.style_bold_italic_underline_link = self.style_link +  ",bold,italic,underline"

        self.STYLE_ITALIC_UNDERLINE_LINK_ID = (self.STYLE_ITALIC_ID | 
                self.STYLE_UNDERLINE_ID |
                self.STYLE_LINK_ID )
        self.style_italic_underline_link = self.style_link +  ",italic,underline"

        self.STYLE_BOLD_UNDERLINE_LINK_ID = (self.STYLE_BOLD_ID | 
                self.STYLE_UNDERLINE_ID |
                self.STYLE_LINK_ID )
        self.style_bold_underline_link = self.style_link +  ",bold,underline"

        self.STYLE_BOLD_ITALIC_LINK_ID = (self.STYLE_BOLD_ID | 
                self.STYLE_ITALIC_ID |
                self.STYLE_LINK_ID )
        self.style_bold_italic_link = self.style_link +  ",bold,italic"

        self.STYLE_ITALIC_LINK_ID = self.STYLE_ITALIC_ID | self.STYLE_LINK_ID 
        self.style_italic_link = self.style_link +  ",italic"

        self.STYLE_UNDERLINE_LINK_ID = self.STYLE_UNDERLINE_ID | self.STYLE_LINK_ID 
        self.style_underline_link = self.style_link +  ",underline"

        self.STYLE_BOLD_LINK_ID = self.STYLE_BOLD_ID | self.STYLE_LINK_ID
        self.style_bold_link = self.style_link  + ",bold"


        super (WikiEditor, self).__init__ (parent)

        self._colorizer = WikiColorizer (self)

        self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.onChange)
        self.Bind (EVT_APPLY_STYLE, self._onApplyStyle)

        self.__styleSet = False


    def setDefaultSettings (self):
        super (WikiEditor, self).setDefaultSettings()

        self.textCtrl.SetLexer (wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)
        self.textCtrl.SetStyleBits (7)

        self._setStyleBold()
        self._setStyleItalic()
        self._setStyleUnderline()

        self._setStyleCommand()
        self._setStyleLink()
        self._setStyleHeading()

        self._setStyleBoldItalic()
        self._setStyleBoldUnderline()
        self._setStyleItalicUnderline()
        self._setStyleBoldItalicUnderline()

        self._setStyleBoldItalicUnderlineLink()
        self._setStyleBoldUnderlineLink()
        self._setStyleItalicUnderlineLink()
        self._setStyleBoldItalicLink()
        self._setStyleBoldLink()
        self._setStyleItalicLink()
        self._setStyleUnderlineLink()


    def _setStyleUnderline (self):
        self._setStyleDefault (self.STYLE_UNDERLINE_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_UNDERLINE_ID, self.style_underline)


    def _setStyleBold (self):
        self._setStyleDefault (self.STYLE_BOLD_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ID, self.style_bold)


    def _setStyleItalic(self):
        self._setStyleDefault (self.STYLE_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_ID, self.style_italic)


    def _setStyleBoldItalic (self):
        self._setStyleDefault (self.STYLE_BOLD_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_ID, self.style_bold_italic)


    def _setStyleUnderlineLink (self):
        self._setStyleDefault (self.STYLE_UNDERLINE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_UNDERLINE_LINK_ID, self.style_underline_link)


    def _setStyleItalicLink (self):
        self._setStyleDefault (self.STYLE_ITALIC_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_LINK_ID, self.style_italic_link)


    def _setStyleBoldLink (self):
        self._setStyleDefault (self.STYLE_BOLD_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_LINK_ID, self.style_bold_link)


    def _setStyleBoldItalicLink (self):
        self._setStyleDefault (self.STYLE_BOLD_ITALIC_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_LINK_ID, self.style_bold_italic_link)


    def _setStyleItalicUnderlineLink (self):
        self._setStyleDefault (self.STYLE_ITALIC_UNDERLINE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_UNDERLINE_LINK_ID, 
                self.style_italic_underline_link)


    def _setStyleBoldUnderlineLink (self):
        self._setStyleDefault (self.STYLE_BOLD_UNDERLINE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_UNDERLINE_LINK_ID, 
                self.style_bold_underline_link)


    def _setStyleBoldItalicUnderlineLink (self):
        self._setStyleDefault (self.STYLE_BOLD_ITALIC_UNDERLINE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_UNDERLINE_LINK_ID, 
                self.style_bold_italic_underline_link)


    def _setStyleBoldUnderline (self):
        self._setStyleDefault (self.STYLE_BOLD_UNDERLINE_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_UNDERLINE_ID, self.style_bold_underline)


    def _setStyleItalicUnderline (self):
        self._setStyleDefault (self.STYLE_ITALIC_UNDERLINE_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_UNDERLINE_ID, self.style_italic_underline)


    def _setStyleBoldItalicUnderline (self):
        self._setStyleDefault (self.STYLE_BOLD_ITALIC_UNDERLINE_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_UNDERLINE_ID, self.style_bold_italic_underline)


    def _setStyleCommand (self):
        self._setStyleDefault (self.STYLE_COMMAND_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_COMMAND_ID, self.style_command)


    def _setStyleLink (self):
        self._setStyleDefault (self.STYLE_LINK_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_LINK_ID, self.style_link)


    def _setStyleHeading (self):
        self.textCtrl.StyleSetSize (self.STYLE_HEADING_ID, self.config.fontSize.value + 2)
        self.textCtrl.StyleSetFaceName (self.STYLE_HEADING_ID, self.config.fontName.value)
        self.textCtrl.StyleSetSpec (self.STYLE_HEADING_ID, self.style_heading)


    def _setStyleDefault (self, styleId):
        self.textCtrl.StyleSetSize (styleId, self.config.fontSize.value)
        self.textCtrl.StyleSetFaceName (styleId, self.config.fontName.value)


    def onChange (self, event):
        self.__styleSet = False


    def getTextForParse (self):
        # Табуляция в редакторе считается за несколько символов
        return self.textCtrl.GetText().replace ("\t", " ")


    def onStyleNeeded (self, event):
        if self.__styleSet:
            return

        text = self.getTextForParse()
        self._colorizer.start (text)


    def _onApplyStyle (self, event):
        if event.text == self.getTextForParse():
            self._applyStyles (event.stylebytes)
    

    def _applyStyles (self, stylebytes):
        self.textCtrl.StartStyling (0, 0xff)
        self.textCtrl.SetStyleBytes (len (stylebytes), stylebytes)
        self.__styleSet = True
