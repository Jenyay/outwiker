# -*- coding: UTF-8 -*-

import wx
import wx.stc


def _getIdSuggests (count):
    return [wx.NewId() for n in xrange(count)]


class TextEditorMenu (wx.Menu):
    ID_ADD_WORD = wx.NewId()
    ID_ADD_WORD_LOWER = wx.NewId()
    ID_SUGGESTS = _getIdSuggests(10)


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


    def AppendSpellSubmenu (self, word, suggestList):
        assert len (suggestList) <= len (self.ID_SUGGESTS)

        spellMenu = wx.Menu()
        spellMenu.Append (self.ID_ADD_WORD, _(u'Add "{}" to dictionary').format (word))

        if word.lower() != word:
            spellMenu.Append (self.ID_ADD_WORD_LOWER, _(u'Add "{}" to dictionary').format (word.lower()))

        if suggestList:
            spellMenu.AppendSeparator()
            for n, suggest in enumerate (suggestList):
                spellMenu.Append (self.ID_SUGGESTS[n], suggest)

        self.AppendSubMenu (spellMenu, _(u'Spell'))
