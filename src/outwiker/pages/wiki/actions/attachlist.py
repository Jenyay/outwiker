# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog


class WikiAttachListAction (BaseAction):
    """
    Вставка команды для показа списка прикрепленных файлов
    """
    stringId = u"WikiAttachList"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Attachment (:attachlist:)")


    @property
    def description (self):
        return _(u"Insert (:attachlist:) command")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        with AttachListDialog (self._application.mainWindow) as dlg:
            controller = AttachListDialogController (dlg)

            text = controller.getDialogResult()
            if text is not None:
                self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText (text)



class AttachListDialogController (object):
    def __init__ (self, dialog):
        self._sortStringsDialog = [
            _(u"Name"),
            _(u"Extension"),
            _(u"Size"),
            _(u"Date"),
        ]

        self._sortStrings = [
            u"name",
            u"ext",
            u"size",
            u"date",
        ]

        self._dialog = dialog
        self._dialog.setSortStrings (self._sortStringsDialog)
        self._dialog.selectedSort = 0


    def getDialogResult (self):
        if self._dialog.ShowModal() == wx.ID_OK:
            return self._getCommand()


    def _getCommand (self):
        return u"(:attachlist {}:)".format (self._getParams())


    def _getParams (self):
        """
        Возвращает строку, описывающую параметры согласно настройкам в диалоге
        """
        sortname = self._sortStrings[self._dialog.selectedSort]
        if self._dialog.isDescend:
            sortname = "descend" + sortname

        return u"sort={}".format (sortname)


class AttachListDialog (TestedDialog):
    def __init__ (self, parent):
        super (AttachListDialog, self).__init__ (parent)

        self.SetTitle (_(u"Insert (:attachlist:) command"))

        self.__createGui ()
        self.__layout()


    def setSortStrings (self, sortStrings):
        self._sortComboBox.Clear()
        self._sortComboBox.AppendItems (sortStrings)


    def __createGui (self):
        self._sortLabel = wx.StaticText (self, label = _(u"Sort by"))

        self._sortComboBox = wx.ComboBox (self, style = wx.CB_DROPDOWN | wx.CB_READONLY)

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


    @selectedSort.setter
    def selectedSort (self, value):
        self._sortComboBox.SetSelection (value)


    @property
    def isDescend (self):
        return self._descendCheckBox.IsChecked()


    @isDescend.setter
    def isDescend (self, value):
        self._descendCheckBox.SetValue (value)
