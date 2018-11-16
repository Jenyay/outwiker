# -*- coding: utf-8 -*-

from typing import List

import wx

from outwiker.gui.testeddialog import TestedDialog


class FilterListDialog(TestedDialog):
    def __init__(self,
                 parent: wx.Window,
                 choices: List[str],
                 title='',
                 message=''
                 ):
        super().__init__(parent,
                         title=title,
                         style=wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX)
        self._choices = choices[:]
        self._createGUI(message)
        self._bindEvents()
        self._filterTextCtrl.SetFocus()
        self._onFilterEdit(None)

    @property
    def selectedLanguage(self) -> str:
        return self._itemsList.GetStringSelection()

    def _bindEvents(self):
        self._filterTextCtrl.Bind(wx.EVT_TEXT, handler=self._onFilterEdit)
        self._itemsList.Bind(wx.EVT_LISTBOX_DCLICK,
                             handler=self._onLangListDblClick)

    def _onFilterEdit(self, event):
        filter = self._filterTextCtrl.GetValue().strip().lower()

        current_langs = [lang
                         for lang in self._choices
                         if not filter or filter in lang.lower()]
        self._itemsList.Set(current_langs)
        if current_langs:
            self._itemsList.SetSelection(0)

    def _onLangListDblClick(self, event):
        self.EndModal(wx.ID_OK)

    def _createGUI(self, message):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        # Message
        self._messageStaticText = wx.StaticText(self, label=message)
        mainSizer.Add(self._messageStaticText,
                      flag=wx.ALL | wx.ALIGN_CENTER,
                      border=2)

        # List
        self._itemsList = wx.ListBox(self)
        self._itemsList.SetMinSize((200, 200))
        mainSizer.Add(self._itemsList,
                      flag=wx.ALL | wx.EXPAND,
                      border=2)

        # Filter
        self._filterTextCtrl = wx.TextCtrl(self)
        mainSizer.Add(self._filterTextCtrl,
                      flag=wx.ALL | wx.EXPAND,
                      border=2)

        # Buttont OK / Cancel
        self._okCancelButtons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.Add(self._okCancelButtons,
                      flag=wx.ALL | wx.ALIGN_RIGHT,
                      border=2)

        self.SetSizer(mainSizer)
        self.Layout()
        self.Fit()
