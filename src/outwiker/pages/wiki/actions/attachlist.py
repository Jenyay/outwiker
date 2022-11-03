# -*- coding: utf-8 -*-

from typing import List

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.attachfilters import getNotHiddenDirOnlyFilter
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox


class WikiAttachListAction(BaseAction):
    """
    Вставка команды для показа списка прикрепленных файлов
    """
    stringId = "WikiAttachList"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Attachment (:attachlist:)")

    @property
    def description(self):
        return _("Insert (:attachlist:) command")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None
        assert self._application.selectedPage is not None

        with AttachListDialog(self._application.mainWindow, self._application.selectedPage) as dlg:
            controller = AttachListDialogController(dlg)

            text = controller.getDialogResult()
            if text is not None:
                self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(
                    text)


class AttachListDialogController:
    def __init__(self, dialog: 'AttachListDialog'):
        self._sortStringsDialog = [
            _("Name"),
            _("Extension"),
            _("Size"),
            _("Date"),
        ]

        self._sortStrings = [
            "name",
            "ext",
            "size",
            "date",
        ]

        self._dialog = dialog

        self._dialog.setSortStrings(self._sortStringsDialog)
        self._dialog.selectedSort = 0

    def getDialogResult(self):
        if self._dialog.ShowModal() == wx.ID_OK:
            return self._getCommand()

    def _getCommand(self):
        return "(:attachlist {}:)".format(self._getParams())

    def _getParams(self) -> str:
        """
        Возвращает строку, описывающую параметры согласно настройкам в диалоге
        """
        params: List[str] = []
        sortname = self._sortStrings[self._dialog.selectedSort]
        if self._dialog.isDescend:
            sortname = "descend" + sortname

        params.append("sort={}".format(sortname))

        if self._dialog.subdir != '.':
            params.append('subdir="{}"'.format(self._dialog.subdir))

        return ' '.join(params)


class AttachListDialog(TestedDialog):
    def __init__(self, parent, page):
        super(AttachListDialog, self).__init__(parent)
        self._page = page

        self.SetTitle(_('Insert (:attachlist:) command'))

        self.__createGui()
        self.__layout()

    def setSortStrings(self, sortStrings):
        self._sortComboBox.Clear()
        self._sortComboBox.AppendItems(sortStrings)

    def __createGui(self):
        self._subdirLabel = wx.StaticText(self, label=_('Directory'))

        self._subdirCtrl = FilesTreeComboBox(self)
        attach_dir = Attachment(self._page).getAttachPath(create=True)
        self._subdirCtrl.SetRootDir(attach_dir)
        self._subdirCtrl.SetFilterFunc(getNotHiddenDirOnlyFilter(self._page))
        self._subdirCtrl.SetValue('.')

        self._sortLabel = wx.StaticText(self, label=_('Sort by'))

        self._sortComboBox = wx.ComboBox(
            self, style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self._descendCheckBox = wx.CheckBox(self, label=_('Descending sort'))
        self._buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

    def __layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        main_sizer.Add(self._subdirLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        main_sizer.Add(self._subdirCtrl, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=2)

        sort_sizer = wx.FlexGridSizer(cols=2)
        sort_sizer.AddGrowableCol(0)
        sort_sizer.AddGrowableCol(1)

        sort_sizer.Add(self._sortLabel, 0, flag=wx.ALL |
                      wx.ALIGN_CENTER_VERTICAL, border=2)
        sort_sizer.Add(self._sortComboBox, 0, flag=wx.EXPAND |
                      wx.ALL, border=2)
        sort_sizer.Add(self._descendCheckBox, 0, flag=wx.ALL |
                      wx.ALIGN_CENTER_VERTICAL, border=2)
        sort_sizer.AddStretchSpacer()
        sort_sizer.AddStretchSpacer()
        sort_sizer.Add(self._buttonsSizer, 0, flag=wx.ALL |
                      wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, border=2)

        main_sizer.Add(sort_sizer, flag=wx.ALL | wx.EXPAND, border=2)
        self.SetSizer(main_sizer)
        self.Fit()

    @property
    def selectedSort(self):
        """
        Возвращает номер выбранного пункта списка
        """
        return self._sortComboBox.GetSelection()

    @selectedSort.setter
    def selectedSort(self, value):
        self._sortComboBox.SetSelection(value)

    @property
    def isDescend(self):
        return self._descendCheckBox.IsChecked()

    @isDescend.setter
    def isDescend(self, value):
        self._descendCheckBox.SetValue(value)

    @property
    def subdir(self):
        return self._subdirCtrl.GetValue()
