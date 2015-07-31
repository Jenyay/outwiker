# -*- coding: UTF-8 -*-

import wx
import wx.stc


class TextEditorMenu (wx.Menu):


    def __init__ (self, editor):
        super (type (self), self).__init__()
        self._editor = editor


    def RefreshItems (self):
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
