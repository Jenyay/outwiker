# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox
from outwiker.core.system import getSpecialDirList
from outwiker.utilites.textfile import readTextFile

from snippets.utils import getImagesPath
from snippets.gui.snippeteditor import SnippetEditor
from snippets.snippetsloader import SnippetsLoader
from snippets.i18n import get_
import snippets.defines as defines


class TreeItemInfo(object):
    def __init__(self, path):
        self.path = path


class EditSnippetsDialog(TestedDialog):
    '''
    Dialog to create, edit and remove snippets and folders.
    '''
    def __init__(self, parent, application):
        super(EditSnippetsDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        global _
        _ = get_()

        self._application = application
        self._width = 800
        self._height = 500
        self.ICON_WIDTH = 16
        self.ICON_HEIGHT = 16

        self.ID_ADD_GROUP = wx.NewId()
        self.ID_ADD_SNIPPET = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_RENAME = wx.NewId()
        self.ID_INSERT_VARIABLE = wx.NewId()

        self._imagesPath = getImagesPath()
        self._dirImageId = None
        self._snippetImageId = None

        self._createGUI()
        self.SetTitle(_(u'Snippets'))
        self.disableSnippetEditor()

        self.snippetsTree.Bind(wx.EVT_TREE_SEL_CHANGED,
                               handler=self._onTreeClick)

    def setSnippetsTree(self, rootdir, snippetsCollection):
        self.snippetsTree.DeleteAllItems()

        info = TreeItemInfo(rootdir)
        rootId = self.snippetsTree.AddRoot(_(u'Snippets'),
                                           self._dirImageId,
                                           data=wx.TreeItemData(info))
        self._buildSnippetsTree(rootId, snippetsCollection, rootdir)
        self.snippetsTree.ExpandAll()

    def disableSnippetEditor(self):
        self._snippetPanel.Disable()

    def enableSnippetEditor(self):
        self._snippetPanel.Enable()

    def _onTreeClick(self, event):
        item = event.GetItem()
        info = self.snippetsTree.GetItemData(item).GetData()
        if os.path.isdir(info.path):
            self.disableSnippetEditor()
            self.snippetEditor.SetText('')
        else:
            self.enableSnippetEditor()
            self._showSnippet(info)

    def _showSnippet(self, info):
        try:
            text = readTextFile(info.path).rstrip()
            self.snippetEditor.SetText(text)
        except EnvironmentError:
            MessageBox(
                _(u"Can't read the snippet\n{}").format(info.path),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)

    def _buildSnippetsTree(self, parentItemId, snippetsCollection, rootdir):
        for subcollection in snippetsCollection.dirs:
            name = subcollection.name
            path = os.path.join(rootdir, name)
            data = wx.TreeItemData(TreeItemInfo(path))
            dirItemId = self.snippetsTree.AppendItem(parentItemId,
                                                     name,
                                                     self._dirImageId,
                                                     data=data)
            self._buildSnippetsTree(dirItemId, subcollection, path)

        for snippet in snippetsCollection.snippets:
            name = os.path.basename(snippet)[:-4]
            data = wx.TreeItemData(TreeItemInfo(snippet))
            self.snippetsTree.AppendItem(parentItemId,
                                         name,
                                         self._snippetImageId,
                                         data=data)

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

    def _createImagesList(self):
        self._imagelist = SafeImageList(self.ICON_WIDTH, self.ICON_HEIGHT)

        self._dirImageId = self._imagelist.Add(
            wx.Bitmap(os.path.join(self._imagesPath, u'folder.png'))
        )

        self._snippetImageId = self._imagelist.Add(
            wx.Bitmap(os.path.join(self._imagesPath, u'snippet.png'))
        )

    def _createTreePanel(self, mainSizer):
        self._createImagesList()

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

        # Snippet editor
        self.snippetEditor = SnippetEditor(self._snippetPanel, self._application)

        # Buttons for snippet
        snippetButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._createSnippetButtons(snippetButtonsSizer, self._snippetPanel)

        # SnippetSizer
        snippetSizer = wx.FlexGridSizer(cols=1)
        snippetSizer.AddGrowableRow(1)
        snippetSizer.AddGrowableCol(0)

        snippetSizer.Add(snippetButtonsSizer, 1, wx.EXPAND, border=2)
        snippetSizer.Add(self.snippetEditor, 1, wx.EXPAND, border=2)

        self._snippetPanel.SetSizer(snippetSizer)
        mainSizer.Add(self._snippetPanel, 1, wx.ALL | wx.EXPAND, border=2)

    def _createGUI(self):
        # Main Sizer
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0, 1)
        mainSizer.AddGrowableCol(1, 3)
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

        rootdir = getSpecialDirList(defines.SNIPPETS_DIR)[-1]
        sl = SnippetsLoader(rootdir)
        snippets_tree = sl.getSnippets()
        self._dialog.setSnippetsTree(rootdir, snippets_tree)
        self._dialog.Show()
