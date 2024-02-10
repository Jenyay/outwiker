# -*- coding: utf-8 -*-

import wx
import wx.stc


class TextEditorMenu(wx.Menu):
    def __init__(self):
        super().__init__()
        self._spellMenu = None

        self.Append(wx.ID_UNDO, _("Undo"))
        self.Append(wx.ID_REDO, _("Redo"))
        self.AppendSeparator()
        self.Append(wx.ID_CUT, _("Cut"))
        self.Append(wx.ID_COPY, _("Copy"))
        self.Append(wx.ID_PASTE, _("Paste"))
        self.AppendSeparator()
        self.Append(wx.ID_SELECTALL, _("Select All"))

        self.ID_ADD_WORD = wx.Window.NewControlId()
        self.ID_ADD_WORD_LOWER = wx.Window.NewControlId()

    def AppendSpellSubmenu(self, word, suggestList):
        self._spellMenu = wx.Menu()
        self._spellMenu.Append(
            self.ID_ADD_WORD, _('Add "{}" to dictionary').format(word)
        )

        if word.lower() != word:
            self._spellMenu.Append(
                self.ID_ADD_WORD_LOWER, _('Add "{}" to dictionary').format(word.lower())
            )

        suggestMenuItems = []
        if suggestList:
            self._spellMenu.AppendSeparator()
            for suggest in suggestList:
                menuItem = self._spellMenu.Append(wx.ID_ANY, suggest)
                suggestMenuItems.append(menuItem)

        self.AppendSubMenu(self._spellMenu, _("Spell"))
        return suggestMenuItems
