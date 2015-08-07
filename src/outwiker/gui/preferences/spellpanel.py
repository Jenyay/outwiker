# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.application import Application
from outwiker.core.system import getSpellDirList, writeTextFile, readTextFile
from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.spellchecker.dictsfinder import DictsFinder
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
        mainSizer.AddGrowableRow (3)

        self._createDictsList (mainSizer)
        self._createCustomDict (mainSizer)
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


    def _createCustomDict (self, mainSizer):
        dictLabel = wx.StaticText (self, label = _(u'Custom dictonary (one word per line)'))
        self.customDict = wx.TextCtrl (self, style=wx.TE_MULTILINE)

        mainSizer.Add (dictLabel,
                       0,
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border=2)

        mainSizer.Add(self.customDict,
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


    def _loadCustomDict (self):
        """
        Load and show custom dictionary
        """
        self.customDict.SetValue (u'')
        try:
            text = readTextFile (self._getCustomDictFileName())
        except (IOError, SystemError):
            return

        self.customDict.SetValue (self._sanitizeDictText (text))


    def _sanitizeDictText (self, text):
        text = u'\n'.join ([item.strip()
                            for item
                            in text.split (u'\n')
                            if len (item.strip()) > 0])
        return text


    def _saveCustomDict (self):
        text = self._sanitizeDictText (self.customDict.GetValue())
        try:
            writeTextFile (self._getCustomDictFileName(), text)
        except (IOError, SystemError):
            pass


    def _getCustomDictFileName (self):
        return os.path.join (getSpellDirList()[-1], CUSTOM_DICT_FILE_NAME)


    def _getDictsFromConfig (self):
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip()
                for item
                in dictsStr.split(',')
                if item.strip()]


    def LoadState(self):
        self._fillDictsList ()
        self._loadCustomDict ()


    def Save (self):
        self._config.spellCheckerDicts.value = u', '.join (self.dictsList.GetCheckedStrings())
        self._saveCustomDict()
