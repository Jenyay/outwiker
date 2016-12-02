# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.testeddialog import TestedDialog

from snippets.utils import getImagesPath


class EditSnippetsDialog(TestedDialog):
    '''
    Dialog to create, edit and remove snippets and folders.
    '''
    def __init__(self, parent, application):
        super(EditSnippetsDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self._application = application
        self._width = 700
        self._height = 400
        self.ICON_WIDTH = 16
        self.ICON_HEIGHT = 16

        self.ID_ADD_GROUP = wx.NewId()
        self.ID_ADD_SNIPPET = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_RENAME = wx.NewId()

        self._imagesPath = getImagesPath()

        self._createGUI()

    def _createGUI(self):
        self._imagelist = SafeImageList(self.ICON_WIDTH, self.ICON_HEIGHT)

        self._tree = wx.TreeCtrl(
            self,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER)
        self._tree.SetMinSize((200, 200))

        self._tree.AssignImageList(self._imagelist)

        # Add a group button
        self.addGroupBtn = wx.BitmapButton(
            self,
            id=self.ID_ADD_GROUP,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "folder_add.png"))
        )
        self.addGroupBtn.SetToolTipString(_(u"Add new snippets group"))

        # Add a snippet button
        self.addSnippetBtn = wx.BitmapButton(
            self,
            id=self.ID_ADD_SNIPPET,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "snippet_add.png"))
        )
        self.addSnippetBtn.SetToolTipString(_(u"Create new snippet"))

        # Remove group or snippet button
        self.removeBtn = wx.BitmapButton(
            self,
            id=self.ID_REMOVE,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "remove.png"))
        )
        self.removeBtn.SetToolTipString(_(u"Remove"))

        # Sizer for buttons for tree
        groupButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        groupButtonsSizer.Add(self.addGroupBtn, flag=wx.ALL, border=0)
        groupButtonsSizer.Add(self.addSnippetBtn, flag=wx.ALL, border=0)
        groupButtonsSizer.Add(self.removeBtn, flag=wx.ALL, border=0)

        # Main Sizer
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        # TreeSizer
        treeSizer = wx.FlexGridSizer(cols=1)
        treeSizer.AddGrowableRow(1)
        treeSizer.AddGrowableCol(0)
        treeSizer.Add(groupButtonsSizer, 1, wx.RIGHT | wx.EXPAND, border=2)
        treeSizer.Add(self._tree, 1, wx.RIGHT | wx.EXPAND, border=2)

        mainSizer.Add(treeSizer, 1, wx.ALL | wx.EXPAND, border=0)

        self.SetSizer(mainSizer)
        self.SetClientSize((self._width, self._height))
        self.Layout()


class EditSnippetsDialogController(object):
    '''
    Controller to manage EditSnippetsDialog.
    '''
    def __init__(self, application):
        self._application = application
        self._dialog = None

    def ShowDialog(self):
        if self._dialog is None:
            self._dialog = EditSnippetsDialog(self._application.mainWindow,
                                              self._application)
        self._dialog.Show()
