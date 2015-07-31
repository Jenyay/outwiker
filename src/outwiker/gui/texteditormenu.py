# -*- coding: UTF-8 -*-

import wx
import wx.stc


class TextEditorMenu (wx.Menu):
    def __init__ (self, editor):
        super (type (self), self).__init__()
        self._editor = editor


    def RefreshItems (self, pos_byte):
        """
        Remove all items and add standard items
        """
        for item in self.GetMenuItems():
            self.RemoveItem (item)

        self.Append (wx.ID_UNDO, _(u'Undo'))
        self.Append (wx.ID_REDO, _(u'Redo'))
        self.AppendSeparator ()
        self.Append (wx.ID_CUT, _(u'Cut'))
        self.Append (wx.ID_COPY, _(u'Copy'))
        self.Append (wx.ID_PASTE, _(u'Paste'))
        self.AppendSeparator ()
        self.Append (wx.ID_SELECTALL, _(u'Select All'))

        # wordStartByte = self._editor.textCtrl.WordStartPosition (pos_byte, True)
        # wordEndByte = self._editor.textCtrl.WordEndPosition (pos_byte, True)
        #
        # text = self._editor.textCtrl.GetTextRange (wordStartByte, wordEndByte)
        #
        # if not self._editor.checkSpellWord (text):
        #     self.AppendSeparator ()
        #     self.Append (-1, text)
