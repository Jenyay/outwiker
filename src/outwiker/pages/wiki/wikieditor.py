#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx.stc

from outwiker.gui.texteditor import TextEditor
from .wikicolorizer import WikiColorizer


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

        self._colorizer = WikiColorizer (self)

        self.textCtrl.Bind (wx.EVT_IDLE, self.onStyleNeeded)
        # self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.onChange)

        self.__styleSet = False


    def setDefaultSettings (self):
        super (WikiEditor, self).setDefaultSettings()

        self.textCtrl.SetLexer (wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)
        self.textCtrl.SetStyleBits (7)

        self._setStyleBold()
        self._setStyleItalic()
        self._setStyleBoldItalic()
        self._setStyleCommand()
        self._setStyleLink()
        self._setStyleHeading()


    def _setStyleBold (self):
        self._setStyleDefault (self.STYLE_BOLD_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ID, self.style_bold)


    def _setStyleItalic(self):
        self._setStyleDefault (self.STYLE_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_ITALIC_ID, self.style_italic)


    def _setStyleBoldItalic (self):
        self._setStyleDefault (self.STYLE_BOLD_ITALIC_ID)
        self.textCtrl.StyleSetSpec (self.STYLE_BOLD_ITALIC_ID, self.style_bold_italic)


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


    def applyStyles (self, stylebytes):
        self.textCtrl.StartStyling (0, 0xff)
        self.textCtrl.SetStyleBytes (len (stylebytes), stylebytes)
        self.__styleSet = True
