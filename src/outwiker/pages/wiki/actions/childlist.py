#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class WikiChildListAction (BaseAction):
    """
    Вставка команды для показа списка дочерних страниц
    """
    stringId = u"WikiChildList"

    def __init__ (self, application):
        self._application = application

        self._sortStrings = [
                u"order",
                u"name",
                ]


    @property
    def title (self):
        return _(u"Children (:childlist:)")


    @property
    def description (self):
        return _(u"Insert (:childlist:) command")
    

    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        with ChildListDialog (self._application.mainWindow) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                params = self._getParams (dlg)
                text = u"(:childlist{}:)".format (params)

                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.replaceText (text)


    def _getParams (self, dialog):
        """
        Возвращает строку, описывающую параметры согласно настройкам в диалоге
        """
        sortIndex = dialog.selectedSort
        descend = dialog.isDescend

        if sortIndex == 0 and not descend:
            return u""

        sortname = self._sortStrings[sortIndex]
        if descend:
            sortname = "descend" + sortname

        return u" sort={}".format (sortname)


class ChildListDialog (wx.Dialog):
    """
    Диалог для вставки команды (:childlist:)
    """
    def __init__ (self, parent):
        super (ChildListDialog, self).__init__ (parent)
        self._sortStrings = [
                _(u"as in tree"),
                _(u"by name"),
                ]

        self.SetTitle (_(u"Insert (:childlist:) command"))

        self.__createGui ()
        self.__layout()


    def __createGui (self):
        self._sortLabel = wx.StaticText (self, label = _(u"Sort"))

        self._sortComboBox = wx.ComboBox (self, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        self._sortComboBox.AppendItems (self._sortStrings)
        self._sortComboBox.SetSelection (0)

        self._descendCheckBox = wx.CheckBox (self, label = _("Descending sort"))
        self._buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)


    def __layout (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        mainSizer.Add (self._sortLabel, 0, flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        mainSizer.Add (self._sortComboBox, 0, flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        mainSizer.Add (self._descendCheckBox, 0, flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        mainSizer.AddStretchSpacer()
        mainSizer.AddStretchSpacer()
        mainSizer.Add (self._buttonsSizer, 0, flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, border = 2)

        self.SetSizer (mainSizer)
        self.Fit()


    @property
    def selectedSort (self):
        """
        Возвращает номер выбранного пункта списка
        """
        return self._sortComboBox.GetSelection()


    @property
    def isDescend (self):
        return self._descendCheckBox.IsChecked()
