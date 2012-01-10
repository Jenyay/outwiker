#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.factoryselector import FactorySelector
from outwiker.core.search import TagsList
from .iconlistctrl import IconListCtrl


class BasePageDialog(wx.Dialog):
    def __init__(self, parentPage = None, *args, **kwds):
        """
        parentPage -- родительская страница (используется, если страницу нужно создавать, а не изменять)
        """
        self.__ID_TAGS_BUTTON = wx.NewId()

        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.titleLabel = wx.StaticText(self, -1, _("Title"))
        self.titleTextCtrl = wx.TextCtrl(self, -1, "")
        self.label_tags = wx.StaticText(self, -1, _("Tags (comma separated)"))
        self.tagsButton = wx.Button (self, self.__ID_TAGS_BUTTON, u">>", style=wx.BU_EXACTFIT )
        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.typeLabel = wx.StaticText(self, -1, _("Page type"))
        self.typeCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.iconLabel = wx.StaticText(self, -1, _("Icon"))
        self.iconsList = IconListCtrl (self)

        self.__set_properties()
        self.__do_layout()

        self.parentPage = parentPage
        self._fillComboType()

        self.titleTextCtrl.SetFocus()


    def __set_properties(self):
        self.SetTitle(_("Create Page"))
        self.SetSize((500, 350))
        self.titleTextCtrl.SetMinSize((350,-1))
        self.tagsTextCtrl.SetMinSize((250, -1))
        self.iconsList.SetMinSize((500, 200))

    def __do_layout(self):
        titleSizer = wx.FlexGridSizer(1, 2, 0, 0)
        titleSizer.Add(self.titleLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        titleSizer.Add(self.titleTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
        titleSizer.AddGrowableCol(1)

        tagsSizer = wx.FlexGridSizer(1, 3, 0, 0)
        tagsSizer.Add(self.label_tags, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        tagsSizer.Add(self.tagsTextCtrl, 0, wx.ALL|wx.EXPAND, 0)
        tagsSizer.Add(self.tagsButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)
        tagsSizer.AddGrowableCol(1)

        typeSizer = wx.FlexGridSizer(1, 2, 0, 0)
        typeSizer.Add(self.typeLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        typeSizer.Add(self.typeCombo, 0, wx.ALL|wx.EXPAND, 4)
        typeSizer.AddGrowableCol(1)

        mainSizer = wx.FlexGridSizer(6, 1, 0, 0)
        mainSizer.AddGrowableRow(4)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(titleSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(tagsSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(typeSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.iconLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        mainSizer.Add(self.iconsList, 1, wx.ALL|wx.EXPAND, 2)
        self._createOkCancelButtons (mainSizer)
        self.SetSizer(mainSizer)

        self.Layout()
        self.titleTextCtrl.SetFocus()
    

    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.AddSpacer(0)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

        sizer.Fit(self)
        self.Layout()

    
    def _fillComboType (self):
        self.typeCombo.Clear()
        for factory in FactorySelector.factories:
            self.typeCombo.Append (factory.title, factory)

        if not self.typeCombo.IsEmpty():
            self.typeCombo.SetSelection (0)
    

    def _setComboPageType (self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        n = 0
        for factory in FactorySelector.factories:
            if factory.getTypeString() == FactorySelector.getFactory(pageTypeString).getTypeString():
                self.typeCombo.SetSelection (n)
                break
            n += 1


    @property
    def selectedFactory (self):
        index = self.typeCombo.GetSelection()
        return self.typeCombo.GetClientData (index)

    @property
    def pageTitle (self):
        return self.titleTextCtrl.GetValue().strip()

    @property
    def tags (self):
        tagsString = self.tagsTextCtrl.GetValue().strip()
        tags = TagsList.parseTagsList (tagsString)
        return tags

    @property
    def icon (self):
        return self.iconsList.icon

# end of class BasePageDialog


