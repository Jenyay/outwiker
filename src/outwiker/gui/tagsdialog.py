# -*- coding: UTF-8 -*-

import wx

from outwiker.core.tagslist import TagsList
from .tagsselector import TagsSelector


class TagsDialog (wx.Dialog):
    def __init__ (self, parent, application):
        super (TagsDialog, self).__init__ (
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.__application = application

        self.__createControls()
        self.__setTagsList()
        self.__tagsSelector.SetFocus()
        self.Center(wx.CENTRE_ON_SCREEN)


    def __setTagsList (self):
        assert self.__application.wikiroot is not None

        tagslist = TagsList (self.__application.wikiroot)
        self.__tagsSelector.setTagsList (tagslist)


    def __createControls (self):
        self.__tagsSelector = TagsSelector (self)
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)

        mainSizer = wx.FlexGridSizer (2, 1, 0, 0)
        mainSizer.AddGrowableRow (0)
        mainSizer.AddGrowableCol (0)

        mainSizer.Add (self.__tagsSelector, 1, wx.EXPAND | wx.BORDER, 4)
        mainSizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.BORDER, 4)

        self.SetSizer (mainSizer)
        self.Fit()
        self.Layout()


    @property
    def tags (self):
        return self.__tagsSelector.tags
