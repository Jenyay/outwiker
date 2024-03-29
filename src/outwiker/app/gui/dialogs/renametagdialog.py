# -*- coding: utf-8 -*-

import wx

from outwiker.gui.singletagselector import SingleTagSelector
from outwiker.gui.dialogs.messagebox import MessageBox


class RenameTagDialog(wx.Dialog):
    """Диалог для переименования меток"""

    def __init__(self, parent, tagsList):
        """
        parent - родительское окно
        tagsList - список тегов для облака тегов (экземпляр класса TagsList)
        """
        super().__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetTitle(_("Rename tag"))

        self.__createControls(tagsList)
        self.__layout()
        self.Center(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)

    def __createControls(self, tagsList):
        self.__tagSelector = SingleTagSelector(self, enable_active_tags_filter=False)
        self.__tagSelector.SetMinSize((300, 150))
        self.__tagSelector.setTags(tagsList)

        self.__selectTagLabel = wx.StaticText(
            self, -1, _("Select tag for rename"))
        self.__newTagLabel = wx.StaticText(self, -1, _("New tag name"))

        self.__newTagName = wx.TextCtrl(self, -1)

        self.__okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)

    def __layout(self):
        mainSizer = wx.FlexGridSizer(4, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        newNameSizer = wx.FlexGridSizer(1, 2, 0, 0)
        newNameSizer.AddGrowableCol(1)
        newNameSizer.Add(self.__newTagLabel, 1, flag=wx.ALL |
                         wx.ALIGN_CENTER_VERTICAL, border=4)
        newNameSizer.Add(self.__newTagName, 1, flag=wx.EXPAND |
                         wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

        mainSizer.Add(self.__selectTagLabel, 1,
                      flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)
        mainSizer.Add(self.__tagSelector, 1, flag=wx.EXPAND | wx.ALL, border=4)
        mainSizer.Add(newNameSizer, 1, flag=wx.ALL | wx.EXPAND, border=4)
        mainSizer.Add(self.__okCancel, 1, flag=wx.ALL |
                      wx.ALIGN_RIGHT, border=4)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Layout()

    @property
    def oldTagName(self):
        return self.__tagSelector.selectedTag

    @property
    def newTagName(self):
        return self.__newTagName.GetValue().strip()

    def setTagsCloudFontSize(self, minFontSize: int, maxFontSize: int):
        self.__tagSelector.setFontSize(minFontSize, maxFontSize)

    def setTagsCloudMode(self, mode: str):
        self.__tagSelector.setMode(mode)

    def enableTagsCloudTooltips(self, enable: bool = True):
        self.__tagSelector.enableTooltips(enable)

    def __onOk(self, _event):
        if self.oldTagName is None:
            MessageBox(_("Select tag for rename"), _(
                "Error"), wx.ICON_ERROR | wx.OK)
            return

        if len(self.newTagName) == 0:
            MessageBox(_("Enter new tag name"), _(
                "Error"), wx.ICON_ERROR | wx.OK)
            return

        self.EndModal(wx.ID_OK)
