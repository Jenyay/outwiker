# -*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.system import getSpellDirList
from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.spellchecker.dictsfinder import DictsFinder
from outwiker.core.spellchecker.spelldict import (get_words_from_dic_file,
                                                  write_to_dic_file)
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class SpellPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super(type(self), self).__init__(parent)

        self._config = EditorConfig(application.config)
        self._createGui()
        self.SetupScrolling()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(4)

        self._skipDigitsCheckBox = self._createCheckBox(
            _(u'Skip words with digits'),
            mainSizer
        )
        self._createDictsList(mainSizer)
        self._createCustomDict(mainSizer)

        self.SetSizer(mainSizer)

    def _createDictsList(self, mainSizer):
        dictsLabel = wx.StaticText(self, label=_(u'Use dictionaries'))
        self.dictsList = wx.CheckListBox(self)

        mainSizer.Add(dictsLabel,
                      0,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        mainSizer.Add(self.dictsList,
                      0,
                      wx.ALL | wx.EXPAND,
                      border=2)

    def _createCustomDict(self, mainSizer):
        dictLabel = wx.StaticText(
            self,
            label=_(u'Custom dictonary (one word per line)'))
        self.customDict = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        mainSizer.Add(dictLabel,
                      0,
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        mainSizer.Add(self.customDict,
                      0,
                      wx.ALL | wx.EXPAND,
                      border=2)

    def _fillDictsList(self):
        dicts = DictsFinder(getSpellDirList()).getLangList()
        dicts.sort()
        selectedDicts = [item
                         for item in self._getDictsFromConfig()
                         if item in dicts]

        self.dictsList.Clear()
        self.dictsList.AppendItems(dicts)
        self.dictsList.SetCheckedStrings(selectedDicts)

    def _loadCustomDict(self):
        """
        Load and show custom dictionary
        """
        self.customDict.SetValue(u'')
        try:
            words = get_words_from_dic_file(self._getCustomDictFileName())
            text = '\n'.join(words)
            self.customDict.SetValue(text)
        except (IOError, SystemError):
            pass

    def _saveCustomDict(self):
        words = [item.strip()
                 for item in self.customDict.GetValue().split('\n')
                 if item.strip()]

        try:
            write_to_dic_file(self._getCustomDictFileName(), words)
        except (IOError, SystemError):
            pass

    def _getCustomDictFileName(self):
        return os.path.join(getSpellDirList()[-1], CUSTOM_DICT_FILE_NAME)

    def _getDictsFromConfig(self):
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip()
                for item
                in dictsStr.split(',')
                if item.strip()]

    def LoadState(self):
        self._fillDictsList()
        self._loadCustomDict()
        self._skipDigitsCheckBox.SetValue(self._config.spellSkipDigits.value)

    def Save(self):
        self._config.spellCheckerDicts.value = u', '.join(self.dictsList.GetCheckedStrings())
        self._saveCustomDict()
        self._config.spellSkipDigits.value = self._skipDigitsCheckBox.GetValue()
