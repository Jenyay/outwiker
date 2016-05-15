# -*- coding: UTF-8 -*-

import wx
import wx.stc


class TextEditorMenu (wx.Menu):
    def __init__ (self):
        super (type (self), self).__init__()

        self.Append (wx.ID_UNDO, _(u'Undo'))
        self.Append (wx.ID_REDO, _(u'Redo'))
        self.AppendSeparator ()
        self.Append (wx.ID_CUT, _(u'Cut'))
        self.Append (wx.ID_COPY, _(u'Copy'))
        self.Append (wx.ID_PASTE, _(u'Paste'))
        self.AppendSeparator ()
        self.Append (wx.ID_SELECTALL, _(u'Select All'))

        self.ID_ADD_WORD = wx.Window.NewControlId()
        self.ID_ADD_WORD_LOWER = wx.Window.NewControlId()


    def AppendSpellSubmenu (self, word, suggestList):
        self._spellMenu = wx.Menu()
        self._spellMenu.Append (self.ID_ADD_WORD, _(u'Add "{}" to dictionary').format (word))

        if word.lower() != word:
            self._spellMenu.Append (self.ID_ADD_WORD_LOWER, _(u'Add "{}" to dictionary').format (word.lower()))

        suggestMenuItems = []
        if suggestList:
            self._spellMenu.AppendSeparator()
            for n, suggest in enumerate (suggestList):
                menuItem = self._spellMenu.Append (wx.ID_ANY, suggest)
                suggestMenuItems.append (menuItem)

        self.AppendSubMenu (self._spellMenu, _(u'Spell'))
        return suggestMenuItems
