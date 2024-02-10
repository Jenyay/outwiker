# -*- coding: utf-8 -*-

import wx
import wx.stc

from outwiker.actions.polyactionsid import (
    CLIPBOARD_COPY_ID,
    CLIPBOARD_CUT_ID,
    CLIPBOARD_PASTE_ID,
    REDO_ID,
    SELECT_ALL_ID,
    UNDO_ID,
)


class TextEditorMenu(wx.Menu):
    def __init__(self, application):
        super().__init__()
        self._application = application
        self._spellMenu = None

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(UNDO_ID),
            id=self.Append(wx.ID_ANY, _("Undo")).GetId(),
        )

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(REDO_ID),
            id=self.Append(wx.ID_ANY, _("Redo")).GetId(),
        )

        self.AppendSeparator()

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(CLIPBOARD_CUT_ID),
            id=self.Append(wx.ID_ANY, _("Cut")).GetId(),
        )

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(CLIPBOARD_COPY_ID),
            id=self.Append(wx.ID_ANY, _("Copy")).GetId(),
        )

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(CLIPBOARD_PASTE_ID),
            id=self.Append(wx.ID_ANY, _("Paste")).GetId(),
        )

        self.AppendSeparator()

        self.Bind(
            wx.EVT_MENU,
            handler=self._getEventHandler(SELECT_ALL_ID),
            id=self.Append(wx.ID_ANY, _("Select all")).GetId(),
        )

        self.ID_ADD_WORD = wx.Window.NewControlId()
        self.ID_ADD_WORD_LOWER = wx.Window.NewControlId()

    def _getEventHandler(self, action_id: str):
        def _handler(event):
            action_controller = self._application.actionController
            action = action_controller.getAction(action_id)
            action.run(None)

        return _handler

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
