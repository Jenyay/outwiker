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
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, _("Title"))
        self.titleTextCtrl = wx.TextCtrl(self, -1, "")
        self.label_2 = wx.StaticText(self, -1, _("Tags (comma separated)"))
        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.label_3 = wx.StaticText(self, -1, _("Page type"))
        self.comboType = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_icon = wx.StaticText(self, -1, _("Icon"))
        self.iconsList = IconListCtrl (self)

        self.__set_properties()
        self.__do_layout()

        self.parentPage = parentPage
        self._fillComboType()

        self.titleTextCtrl.SetFocus()


    def testPageTitle (self, title):
        """
        Возвращает True, если возможно создать страницу с таким заголовком
        """
        striptitle = title.strip()

        if ("/" in striptitle or 
            "\\" in striptitle or
            striptitle.startswith ("__") or
            len (striptitle) == 0 or
            striptitle == "."):
            return False

        return True
    

    def __set_properties(self):
        self.SetTitle(_("Create Page"))
        self.SetSize((500, 350))
        self.titleTextCtrl.SetMinSize((350,-1))
        self.tagsTextCtrl.SetMinSize((250, -1))
        self.iconsList.SetMinSize((500, 200))

    def __do_layout(self):
        grid_sizer_1 = wx.FlexGridSizer(6, 1, 0, 0)
        grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_3 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_2.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_2.Add(self.titleTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
        grid_sizer_2.AddGrowableCol(1)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_3.Add(self.tagsTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
        grid_sizer_3.AddGrowableCol(1)
        grid_sizer_1.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_4.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_4.Add(self.comboType, 0, wx.ALL|wx.EXPAND, 4)
        grid_sizer_4.AddGrowableCol(1)
        grid_sizer_1.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_icon, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.iconsList, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(4)
        grid_sizer_1.AddGrowableCol(0)
        self.Layout()
    
        self._createOkCancelButtons (grid_sizer_1)
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
        self.comboType.Clear()
        for factory in FactorySelector.factories:
            self.comboType.Append (factory.title, factory)

        if not self.comboType.IsEmpty():
            self.comboType.SetSelection (0)
    

    def _setComboPageType (self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        n = 0
        for factory in FactorySelector.factories:
            if factory.getTypeString() == FactorySelector.getFactory(pageTypeString).getTypeString():
                self.comboType.SetSelection (n)
                break
            n += 1


    @property
    def selectedFactory (self):
        index = self.comboType.GetSelection()
        return self.comboType.GetClientData (index)

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


