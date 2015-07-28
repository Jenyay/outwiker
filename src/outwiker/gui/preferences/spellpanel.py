# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.spellchecker import DictsFinder
from outwiker.core.system import getSpellDirList
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class SpellPanel(BasePrefPanel):
    def __init__(self, parent):
        super (type (self), self).__init__ (parent)

        self._config = EditorConfig (Application.config)
        self._createGui()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        self._createDictsList (mainSizer)
        self.SetSizer (mainSizer)


    def _createDictsList (self, mainSizer):
        dictsLabel = wx.StaticText (self, label = _(u'Use dictionaries'))
        self.dictsList = wx.CheckListBox (self)

        mainSizer.Add (dictsLabel,
                       0,
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border=2)

        mainSizer.Add(self.dictsList,
                      0,
                      wx.ALL | wx.EXPAND,
                      border=2)


    def _fillDictsList (self):
        dicts = DictsFinder (getSpellDirList()).getLangList()
        dicts.sort()
        selectedDicts = filter (
            lambda item: item in dicts,
            self._getDictsFromConfig())


        self.dictsList.Clear()
        self.dictsList.AppendItems (dicts)
        self.dictsList.SetCheckedStrings (selectedDicts)


    def _getDictsFromConfig (self):
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip()
                for item
                in dictsStr.split(',')
                if item.strip()]


    def LoadState(self):
        self._fillDictsList ()


    def Save (self):
        self._config.spellCheckerDicts.value = u', '.join (self.dictsList.GetCheckedStrings())
