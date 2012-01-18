#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path

import wx

from outwiker.core.factoryselector import FactorySelector
from outwiker.core.tagslist import TagsList
from outwiker.core.application import Application
from outwiker.core.system import getImagesDir
from outwiker.core.tagscommands import parseTagsList

from .iconlistctrl import IconListCtrl
from .tagspopup import TagsPopup
from .tagscloud import TagsCloud
from .taglabel import EVT_TAG_CLICK


class BasePageDialog(wx.Dialog):
    def __init__(self, parentPage = None, *args, **kwds):
        """
        parentPage -- родительская страница (используется, если страницу нужно создавать, а не изменять)
        """
        self.__ID_TAGS_BUTTON = wx.NewId()
        self.__tagsWidth = 350
        self.__tagsHeight = 150

        self.__tagBitmap = wx.Bitmap (os.path.join (getImagesDir(), "tag.png"), 
                wx.BITMAP_TYPE_PNG)

        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.titleLabel = wx.StaticText(self, -1, _(u"Title"))
        self.titleTextCtrl = wx.TextCtrl(self, -1, "")
        self.label_tags = wx.StaticText(self, -1, _(u"Tags (comma separated)"))

        self.tagsButton = wx.BitmapButton (self, 
                self.__ID_TAGS_BUTTON, 
                self.__tagBitmap)

        self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
        self.typeLabel = wx.StaticText(self, -1, _(u"Page type"))
        self.typeCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.iconLabel = wx.StaticText(self, -1, _(u"Icon"))
        self.iconsList = IconListCtrl (self)

        self.__set_properties()
        self.__do_layout()

        self.parentPage = parentPage
        self._fillComboType()

        self.__tagsCloud = TagsPopup (self)
        self.__tagsCloud.SetSize ((self.__tagsWidth, self.__tagsHeight))
        self.__tagsCloud.Bind (EVT_TAG_CLICK, self.__onTagClick)

        self.__fillTagsList()

        self.titleTextCtrl.SetFocus()

        self.Bind(wx.EVT_BUTTON, self.__onShowTags, id=self.__ID_TAGS_BUTTON)


    def __onTagClick (self, event):
        self.__addTagText (event.text)


    def __addTagText (self, tagname):
        currentText = self.tagsTextCtrl.GetValue().strip()

        if len (currentText) == 0:
            newtext = tagname
        elif currentText[-1] == ",":
            newtext = currentText + " " + tagname
        else:
            newtext = currentText + ", " + tagname

        self.tagsTextCtrl.SetValue (newtext)
        self.tagsTextCtrl.SetFocus()
        self.tagsTextCtrl.SetSelection (len (newtext), len (newtext))


    def __fillTagsList (self):
        assert Application.wikiroot != None

        tagslist = TagsList (Application.wikiroot)
        self.__tagsCloud.setTags (tagslist)


    def __onShowTags (self, event):
        if self.__tagsCloud.IsShown():
            self.__tagsCloud.Hide()
        else:
            (buttonx, buttony) = self.tagsButton.GetPositionTuple()
            (buttonw, buttonh) = self.tagsButton.GetSizeTuple()

            (screenx, screeny) = self.ClientToScreenXY (buttonx + buttonw - self.__tagsWidth,
                    buttony + buttonh)

            self.__tagsCloud.SetPosition ((screenx, screeny))

            self.__tagsCloud.Popup()


    def __set_properties(self):
        self.SetTitle(_(u"Create Page"))
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
        tags = parseTagsList (tagsString)
        return tags

    @property
    def icon (self):
        return self.iconsList.icon

# end of class BasePageDialog


