# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.testeddialog import TestedDialog

from snippets.utils import getImagesPath
from snippets.gui.snippeteditor import SnippetEditor


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
        self.ID_INSERT_VARIABLE = wx.NewId()

        self._imagesPath = getImagesPath()

        self._createGUI()
        self.disableSnippetEditor()

    def disableSnippetEditor(self):
        self._snippetPanel.Disable()

    def _createTreeButtons(self, groupButtonsSizer):
        # Add a group button
        self.addGroupBtn = wx.BitmapButton(
            self,
            id=self.ID_ADD_GROUP,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "folder_add.png"))
        )
        self.addGroupBtn.SetToolTipString(_(u"Add new snippets group"))
        groupButtonsSizer.Add(self.addGroupBtn, flag=wx.ALL, border=0)

        # Add a snippet button
        self.addSnippetBtn = wx.BitmapButton(
            self,
            id=self.ID_ADD_SNIPPET,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "snippet_add.png"))
        )
        self.addSnippetBtn.SetToolTipString(_(u"Create new snippet"))
        groupButtonsSizer.Add(self.addSnippetBtn, flag=wx.ALL, border=0)

        # Remove group or snippet button
        self.removeBtn = wx.BitmapButton(
            self,
            id=self.ID_REMOVE,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "remove.png"))
        )
        self.removeBtn.SetToolTipString(_(u"Remove"))
        groupButtonsSizer.Add(self.removeBtn, flag=wx.ALL, border=0)

    def _createTreePanel(self, mainSizer):
        self._imagelist = SafeImageList(self.ICON_WIDTH, self.ICON_HEIGHT)

        self.snippetsTree = wx.TreeCtrl(
            self,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER)
        self.snippetsTree.SetMinSize((200, 200))

        self.snippetsTree.AssignImageList(self._imagelist)

        # Buttons for the snippets tree
        groupButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._createTreeButtons(groupButtonsSizer)

        # TreeSizer
        treeSizer = wx.FlexGridSizer(cols=1)
        treeSizer.AddGrowableRow(1)
        treeSizer.AddGrowableCol(0)
        treeSizer.Add(groupButtonsSizer, 1, wx.EXPAND, border=2)
        treeSizer.Add(self.snippetsTree, 1, wx.EXPAND, border=2)

        mainSizer.Add(treeSizer, 1, wx.ALL | wx.EXPAND, border=0)

    def _createSnippetButtons(self, snippetButtonsSizer, parent):
        # Insert variable
        self.insertVariableBtn = wx.BitmapButton(
            parent,
            id=self.ID_INSERT_VARIABLE,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "variables.png"))
        )
        self.insertVariableBtn.SetToolTipString(_(u"Insert variable"))
        snippetButtonsSizer.Add(self.insertVariableBtn, flag=wx.ALL, border=0)

    def _createSnippetPanel(self, mainSizer):
        self._snippetPanel = wx.Panel(self)
        # Snippet title controls
        snippetTitleLabel = wx.StaticText(self._snippetPanel, label=_(u'Snippet name'))
        self.snippetTitle = wx.TextCtrl(self._snippetPanel)

        titleSizer = wx.FlexGridSizer(cols=2)
        titleSizer.AddGrowableCol(1)

        titleSizer.Add(snippetTitleLabel,
                       flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
                       border=2)
        titleSizer.Add(self.snippetTitle,
                       flag=wx.ALL | wx.EXPAND, border=2)

        # Snippet editor
        self.snippetEditor = SnippetEditor(self._snippetPanel, self._application)

        # Buttons for snippet
        snippetButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._createSnippetButtons(snippetButtonsSizer, self._snippetPanel)

        # SnippetSizer
        snippetSizer = wx.FlexGridSizer(cols=1)
        snippetSizer.AddGrowableRow(2)
        snippetSizer.AddGrowableCol(0)

        snippetSizer.Add(titleSizer, 1, wx.EXPAND, border=2)
        snippetSizer.Add(snippetButtonsSizer, 1, wx.EXPAND, border=2)
        snippetSizer.Add(self.snippetEditor, 1, wx.EXPAND, border=2)

        self._snippetPanel.SetSizer(snippetSizer)

        mainSizer.Add(self._snippetPanel, 1, wx.ALL | wx.EXPAND, border=2)

    def _createGUI(self):
        # Main Sizer
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        self._createTreePanel(mainSizer)
        self._createSnippetPanel(mainSizer)

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
