# -*- coding: UTF-8 -*-

import os
import shutil

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox
from outwiker.core.system import getSpecialDirList
from outwiker.utilites.textfile import readTextFile

from snippets.actions.updatemenu import UpdateMenuAction
from snippets.gui.snippeteditor import SnippetEditor
from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.utils import getImagesPath
import snippets.defines as defines


class TreeItemInfo(object):
    def __init__(self, path, root=False):
        self.path = path
        self.root = root


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

        self.addGroupBtn = None
        self.addSnippetBtn = None

        self._createGUI()
        self.SetTitle(_(u'Snippets'))
        self.disableSnippetEditor()

    def disableSnippetEditor(self):
        self._snippetPanel.Disable()

    def enableSnippetEditor(self):
        self._snippetPanel.Enable()

    def appendDirTreeItem(self, parentItem, name, data):
        itemData = wx.TreeItemData(data)
        if parentItem is not None:
            newItemId = self.snippetsTree.AppendItem(parentItem,
                                                     name,
                                                     self._dirImageId,
                                                     data=itemData)
        else:
            newItemId = self.snippetsTree.AddRoot(name,
                                                  self._dirImageId,
                                                  data=itemData)
        return newItemId

    def appendSnippetTreeItem(self, parentItem, name, data):
        itemData = wx.TreeItemData(data)
        newItemId = self.snippetsTree.AppendItem(parentItem,
                                                 name,
                                                 self._snippetImageId,
                                                 data=itemData)
        return newItemId

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

        # Rename group or snippet button
        self.renameBtn = wx.BitmapButton(
            self,
            id=self.ID_RENAME,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "rename.png"))
        )
        self.renameBtn.SetToolTipString(_(u"Rename"))
        groupButtonsSizer.Add(self.renameBtn, flag=wx.ALL, border=0)

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
        global _
        _ = get_()
        self._application = application
        self._dialog = EditSnippetsDialog(self._application.mainWindow,
                                          self._application)
        self._bind()

    def _bind(self):
        self._dialog.addGroupBtn.Bind(wx.EVT_BUTTON, handler=self._onAddGroup)
        self._dialog.removeBtn.Bind(wx.EVT_BUTTON, handler=self._onRemove)
        self._dialog.renameBtn.Bind(wx.EVT_BUTTON, handler=self._onRenameClick)

        self.snippetsTree.Bind(wx.EVT_TREE_SEL_CHANGED,
                               handler=self._onTreeItemClick)
        self.snippetsTree.Bind(wx.EVT_TREE_END_LABEL_EDIT,
                               handler=self._onRenameEnd)
        self.snippetsTree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,
                               handler=self._onRenameBegin)

    def ShowDialog(self):
        rootdir = getSpecialDirList(defines.SNIPPETS_DIR)[-1]
        sl = SnippetsLoader(rootdir)
        snippets_tree = sl.getSnippets()
        self._fillSnippetsTree(rootdir, snippets_tree)
        self._dialog.Show()

    def _fillSnippetsTree(self, rootdir, snippetsCollection):
        self.snippetsTree.DeleteAllItems()
        info = TreeItemInfo(rootdir, True)
        rootId = self._dialog.appendDirTreeItem(None, _(u'Snippets'), info)
        self._buildSnippetsTree(rootId, snippetsCollection, rootdir)
        self.snippetsTree.ExpandAll()
        self.snippetsTree.SelectItem(rootId)

    def _buildSnippetsTree(self, parentItemId, snippetsCollection, rootdir):
        # Append snippet directories
        for subcollection in sorted(snippetsCollection.dirs, key=lambda x: x.name):
            name = subcollection.name
            path = os.path.join(rootdir, name)
            data = TreeItemInfo(path)
            dirItemId = self._dialog.appendDirTreeItem(parentItemId,
                                                       name,
                                                       data)
            self._buildSnippetsTree(dirItemId, subcollection, path)

        # Append snippets
        for snippet in sorted(snippetsCollection.snippets):
            name = os.path.basename(snippet)[:-len(defines.EXTENSION)]
            data = TreeItemInfo(snippet)
            self._dialog.appendSnippetTreeItem(parentItemId, name, data)

    @property
    def snippetsTree(self):
        return self._dialog.snippetsTree

    def _onRemove(self, event):
        item = self.snippetsTree.GetSelection()
        if self._isRootItem(item):
            return

        if self._isDirItem(item):
            self._removeDir(item)
        else:
            self._removeSnippet(item)

    def _removeDir(self, item):
        parentItem = self.snippetsTree.GetItemParent(item)
        path = self._getItemData(item).path
        path_base = os.path.basename(path)
        result = MessageBox(_(u'Remove directory "{}" and all snippets inside?').format(path_base),
                            _(u"Remove snippets directory"),
                            wx.YES | wx.NO | wx.ICON_QUESTION)
        if result == wx.YES:
            try:
                shutil.rmtree(path)
                self.snippetsTree.Delete(item)
                self.snippetsTree.SelectItem(parentItem)
                self._application.actionController.getAction(UpdateMenuAction.stringId).run(None)
            except EnvironmentError:
                MessageBox(
                    _(u'Can\'t remove directory "{}"').format(path_base),
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

    def _removeSnippet(self, item):
        parentItem = self.snippetsTree.GetItemParent(item)
        path = self._getItemData(item).path
        path_base = os.path.basename(path)[:-len(defines.EXTENSION)]
        result = MessageBox(_(u'Remove snippet "{}"?').format(path_base),
                            _(u"Remove snippet"),
                            wx.YES | wx.NO | wx.ICON_QUESTION)
        if result == wx.YES:
            try:
                os.remove(path)
                self.snippetsTree.Delete(item)
                self.snippetsTree.SelectItem(parentItem)
                self._application.actionController.getAction(UpdateMenuAction.stringId).run(None)
            except EnvironmentError:
                MessageBox(
                    _(u'Can\'t remove snippet "{}"').format(path_base),
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

    def _onAddGroup(self, event):
        '''
        Add group button click
        '''
        selectedItem = self._getSelectedItemData()
        assert selectedItem is not None
        rootdir = selectedItem.path

        if not os.path.isdir(rootdir):
            rootdir = os.path.dirname(rootdir)

        # Find unique directory for snippets
        newpath = self._findUniquePath(
            os.path.join(rootdir, _(defines.NEW_DIR_NAME))
        )

        try:
            os.mkdir(newpath)
            self._addChildDir(newpath)
        except EnvironmentError:
            MessageBox(
                _(u"Can't create directory\n{}").format(newpath),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)

    def _addChildDir(self, newpath):
        item = self.snippetsTree.GetSelection()
        assert item.IsOk()

        if not self._isDirItem(item):
            item = self.snippetsTree.GetItemParent(item)

        name = os.path.basename(newpath)
        data = TreeItemInfo(newpath)
        newitem = self._dialog.appendDirTreeItem(item, name, data)
        self.snippetsTree.SelectItem(newitem)
        self.snippetsTree.EditLabel(newitem)

    def _isDirItem(self, treeItem):
        '''
        Return True if treeItem is directory item
        '''
        path = self._getItemData(treeItem).path
        return os.path.isdir(path)

    def _onRenameEnd(self, event):
        '''
        Rename button event handler
        '''
        if event.IsEditCancelled():
            return

        item = event.GetItem()
        newlabel = event.GetLabel()
        selectedItem = self._getSelectedItemData()
        assert selectedItem is not None
        oldpath = selectedItem.path
        isdir = os.path.isdir(oldpath)

        if isdir:
            # Rename directory
            newpath = self._findUniquePath(
                os.path.join(os.path.dirname(oldpath), newlabel)
            )
        else:
            # Rename snippet
            newpath = self._findUniquePath(
                os.path.join(os.path.dirname(oldpath),
                             newlabel + defines.EXTENSION)
            )

        try:
            self._getItemData(item).path = newpath
            os.rename(oldpath, newpath)
        except EnvironmentError:
            event.Veto()
            self._application.actionController.getAction(UpdateMenuAction.stringId).run(None)

    def _onTreeItemClick(self, event):
        item = event.GetItem()
        info = self._getItemData(item)
        if os.path.isdir(info.path):
            # Selected item is directory
            self._dialog.disableSnippetEditor()
            self._dialog.snippetEditor.SetText('')
        else:
            # Selected item is snippet
            self._dialog.enableSnippetEditor()
            self._showSnippet(info)

    def _onRenameBegin(self, event):
        item = event.GetItem()
        assert item.IsOk()
        if self._isRootItem(item):
            event.Veto()

    def _isRootItem(self, item):
        return self.snippetsTree.GetRootItem() == item

    def _onRenameClick(self, event):
        item = self.snippetsTree.GetSelection()
        assert item.IsOk()
        self.snippetsTree.EditLabel(item)

    def _showSnippet(self, info):
        try:
            text = readTextFile(info.path).rstrip()
            self._dialog.snippetEditor.SetText(text)
        except EnvironmentError:
            MessageBox(
                _(u"Can't read the snippet\n{}").format(info.path),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)

    def _findUniquePath(self, path):
        index = 1
        result = path

        while os.path.exists(result):
            suffix = u' ({})'.format(index)
            result = path + suffix
            index += 1
            return result

    def _getItemData(self, item):
        if not item.IsOk():
            return None
        info = self.snippetsTree.GetItemData(item).GetData()
        return info

    def _getSelectedItemData(self):
        item = self.snippetsTree.GetSelection()
        return self._getItemData(item)
