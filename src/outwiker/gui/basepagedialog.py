#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path

import wx

from outwiker.core.factoryselector import FactorySelector
from outwiker.core.application import Application
from outwiker.core.tagslist import TagsList
from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList
from .guiconfig import PageDialogConfig
from .iconlistctrl import IconListCtrl
from .tagsselector import TagsSelector


class BasePageDialog(wx.Dialog):
    def __init__(self, parentPage = None, *args, **kwds):
        """
        parentPage - родительская страница (используется, если страницу нужно создавать, а не изменять)
        """
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)

        # Используется для редактирования существующей страницы
        self.currentPage = None

        self.config = PageDialogConfig (Application.config)

        self.notebook = wx.Notebook (self, -1)

        self.generalPanel = GeneralPanel (self.notebook)
        self.iconPanel = IconPanel (self.notebook)
        self.appearancePanel = AppearancePanel (self.notebook)

        self.notebook.AddPage (self.generalPanel, _("General"))
        self.notebook.AddPage (self.iconPanel, _("Icon"))
        self.notebook.AddPage (self.appearancePanel, _("Appearance"))

        self.__set_properties()
        self.__do_layout()

        self.parentPage = parentPage
        self._fillComboType()
        self._setTagsList()

        self.generalPanel.titleTextCtrl.SetFocus()
        self._stylesList = StylesList (getStylesDirList ())
        self.Center(wx.CENTRE_ON_SCREEN)


    def __set_properties(self):
        self.SetTitle(_(u"Create Page"))
        self.SetSize((self.config.width.value, self.config.height.value))


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add (self.notebook, 0, wx.EXPAND, 0)
        self._createOkCancelButtons (mainSizer)
        self.SetSizer(mainSizer)

        self.Layout()


    def saveParams (self):
        width, height = self.GetSizeTuple()
        self.config.width.value = width
        self.config.height.value = height

        styleIndex =  self.appearancePanel.styleCombo.GetSelection()
        styleName = self.appearancePanel.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае, 
        # если изменяется существующая страница
        if (self.currentPage == None):
            self.config.recentStyle.value = styleName


    def _fillStyleCombo (self, styleslist, page=None):
        """
        Заполняет self.appearancePanel.styleCombo списком стилей
        styleslist - список путей до загруженных стилей
        page - страница, для которой вызывается диалог. Если page != None, то первый стиль в списке - это стиль данной страницы
        """
        names = []
        if page != None:
            names.append (_(u"Do not change"))

        names.append (_(u"Default") )
        style_names = [os.path.basename (style) for style in styleslist]

        names += style_names

        self.appearancePanel.styleCombo.Clear()
        self.appearancePanel.styleCombo.AppendItems (names)

        # Определение последнего используемого стиля
        recentStyle = self.config.recentStyle.value
        names_lower = [name.lower() for name in names]
        try:
            recentStyleIndex = names_lower.index (recentStyle.lower())
        except ValueError:
            recentStyleIndex = 0

        self.appearancePanel.styleCombo.SetSelection (recentStyleIndex)



    def _setTagsList (self):
        assert Application.wikiroot != None

        tagslist = TagsList (Application.wikiroot)
        self.generalPanel.tagsSelector.setTagsList (tagslist)


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)


    def _fillComboType (self):
        self.generalPanel.typeCombo.Clear()
        for factory in FactorySelector.factories:
            self.generalPanel.typeCombo.Append (factory.title, factory)

        if not self.generalPanel.typeCombo.IsEmpty():
            self.generalPanel.typeCombo.SetSelection (0)


    def _setComboPageType (self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        n = 0
        for factory in FactorySelector.factories:
            if factory.getTypeString() == FactorySelector.getFactory(pageTypeString).getTypeString():
                self.generalPanel.typeCombo.SetSelection (n)
                break
            n += 1


    @property
    def selectedFactory (self):
        index = self.generalPanel.typeCombo.GetSelection()
        return self.generalPanel.typeCombo.GetClientData (index)


    @property
    def pageTitle (self):
        return self.generalPanel.titleTextCtrl.GetValue().strip()


    @property
    def tags (self):
        return self.generalPanel.tagsSelector.tags


    @property
    def icon (self):
        return self.iconPanel.iconsList.icon



class GeneralPanel (wx.Panel):
    """
    Класс панели, расположенной на вкладке "Общее"
    """
    def __init__ (self, parent):
        super (GeneralPanel, self).__init__ (parent)

        self.__createGeneralControls()
        self.__layout ()


    def __layout (self):
        titleSizer = wx.FlexGridSizer(1, 2, 0, 0)
        titleSizer.Add(self.titleLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        titleSizer.Add(self.titleTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
        titleSizer.AddGrowableCol(1)

        typeSizer = wx.FlexGridSizer(1, 2, 0, 0)
        typeSizer.Add(self.typeLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        typeSizer.Add(self.typeCombo, 0, wx.ALL|wx.EXPAND, 4)
        typeSizer.AddGrowableCol(1)

        generalSizer = wx.FlexGridSizer(3, 1, 0, 0)
        generalSizer.AddGrowableRow(2)
        generalSizer.AddGrowableCol(0)
        generalSizer.Add(titleSizer, 0, wx.EXPAND, 0)
        generalSizer.Add(typeSizer, 0, wx.EXPAND, 0)
        generalSizer.Add(self.tagsSelector, 0, wx.EXPAND, 0)

        self.SetSizer (generalSizer)
        self.Layout()


    def __createGeneralControls (self):
        self.titleLabel = wx.StaticText(self, -1, _(u"Title"))
        
        self.titleTextCtrl = wx.TextCtrl(self, -1, "")
        self.titleTextCtrl.SetMinSize((350, -1))

        self.typeCombo = wx.ComboBox(self, 
                -1, 
                choices=[], 
                style=wx.CB_DROPDOWN|wx.CB_READONLY)

        self.tagsSelector = TagsSelector (self)
        self.typeLabel = wx.StaticText(self, -1, _(u"Page type"))


class IconPanel (wx.Panel):
    """
    Класс панели, расположенной на вкладке "Значок"
    """
    def __init__ (self, parent):
        super (IconPanel, self).__init__ (parent)

        self.iconsList = IconListCtrl (self)
        self.iconsList.SetMinSize((200, 150))

        self.__layout()


    def __layout (self):
        iconSizer = wx.FlexGridSizer(1, 1, 0, 0)
        iconSizer.AddGrowableRow(0)
        iconSizer.AddGrowableCol(0)
        iconSizer.Add(self.iconsList, 1, wx.ALL|wx.EXPAND, 2)

        self.SetSizer (iconSizer)
        self.Layout()


class AppearancePanel (wx.Panel):
    def __init__ (self, parent):
        super (AppearancePanel, self).__init__ (parent)

        self.styleText = wx.StaticText (self, -1, _("Page style"))
        self.styleCombo = wx.ComboBox (
                self, 
                -1, 
                choices=[], 
                style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY
                )

        self.__layout ()


    def __layout (self):
        styleSizer = wx.FlexGridSizer (1, 2, 0, 0)
        styleSizer.AddGrowableCol (1)
        styleSizer.Add (self.styleText, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        styleSizer.Add (self.styleCombo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 4)

        self.SetSizer (styleSizer)
        self.Layout()
