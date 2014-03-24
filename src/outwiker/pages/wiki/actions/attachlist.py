#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class WikiAttachListAction (BaseAction):
    """
    Вставка команды для показа списка прикрепленных файлов
    """
    stringId = u"WikiAttachList"

    def __init__ (self, application):
        self._application = application
        self._sortStrings = [
                u"name",
                u"ext",
                u"size",
                u"date",
                ]


    @property
    def title (self):
        return _(u"Attachment (:attachlist:)")


    @property
    def description (self):
        return _(u"Insert (:attachlist:) command")


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        with AttachListDialog (self._application.mainWindow) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                params = self._getParams (dlg)
                text = u"(:attachlist {}:)".format (params)

                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.replaceText (text)


    def _getParams (self, dialog):
        """
        Возвращает строку, описывающую параметры согласно настройкам в диалоге
        """
        sortname = self._sortStrings[dialog.selectedSort]
        if dialog.isDescend:
            sortname = "descend" + sortname

        return u"sort={}".format (sortname)



class AttachListDialog (wx.Dialog):
    def __init__ (self, parent):
        super (AttachListDialog, self).__init__ (parent)
        self._sortStrings = [
                _(u"Name"),
                _(u"Extension"),
                _(u"Size"),
                _(u"Date"),
                ]

        self.SetTitle (_(u"Insert (:attachlist:) command"))

        self.__createGui ()
        self.__layout()


    def __createGui (self):
        self._sortLabel = wx.StaticText (self, label = _(u"Sort by"))

        self._sortComboBox = wx.ComboBox (self, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        self._sortComboBox.AppendItems (self._sortStrings)
        self._sortComboBox.SetSelection (0)

        self._descendCheckBox = wx.CheckBox (self, label = _("Descending sort"))
        self._buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)


    def __layout (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        mainSizer.Add (self._sortLabel, 0, flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
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
