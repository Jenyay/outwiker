# -*- coding: UTF-8 -*-

import wx

from .singletagselector import SingleTagSelector


class RenameTagDialog(wx.Dialog):
    """Диалог для переименования меток"""
    def __init__(self, parent, tagsList):
        """
        parent - родительское окно
        tagsList - список тегов для облака тегов (экземпляр класса TagsList)
        """
        super(RenameTagDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.SetTitle (_(u"Rename tag"))

        self.__createControls(tagsList)
        self.__layout()
        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)


    def __createControls (self, tagsList):
        self.__tagSelector = SingleTagSelector (self)
        self.__tagSelector.SetMinSize ((300, 150))
        self.__tagSelector.setTags (tagsList)

        self.__selectTagLabel = wx.StaticText (self, -1, _(u"Select tag for rename"))
        self.__newTagLabel = wx.StaticText (self, -1, _(u"New tag name"))

        self.__newTagName = wx.TextCtrl (self, -1)

        self.__okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)


    def __layout (self):
        mainSizer = wx.FlexGridSizer (4, 1, 0, 0)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        newNameSizer = wx.FlexGridSizer (1, 2, 0, 0)
        newNameSizer.AddGrowableCol (1)
        newNameSizer.Add (self.__newTagLabel, 1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        newNameSizer.Add (self.__newTagName, 1, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

        mainSizer.Add (self.__selectTagLabel, 1, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=4)
        mainSizer.Add (self.__tagSelector, 1, flag=wx.EXPAND | wx.ALL, border=4)
        mainSizer.Add (newNameSizer, 1, flag=wx.ALL | wx.EXPAND, border=4)
        mainSizer.Add (self.__okCancel, 1, flag=wx.ALL | wx.ALIGN_RIGHT, border=4)

        self.SetSizer (mainSizer)
        self.Fit()
        self.Layout()


    @property
    def oldTagName (self):
        return self.__tagSelector.selectedTag


    @property
    def newTagName (self):
        return self.__newTagName.GetValue().strip()


    def __onOk (self, event):
        from outwiker.core.commands import MessageBox

        if self.oldTagName is None:
            MessageBox (_(u"Select tag for rename"), _(u"Error"), wx.ICON_ERROR | wx.OK)
            return

        if len (self.newTagName) == 0:
            MessageBox (_(u"Enter new tag name"), _(u"Error"), wx.ICON_ERROR | wx.OK)
            return

        self.EndModal (wx.ID_OK)
