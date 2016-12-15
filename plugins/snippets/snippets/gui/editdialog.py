# -*- coding: UTF-8 -*-

import re
import os
import shutil

import wx

from outwiker.gui.controls.popupbutton import (PopupButton,
                                               EVT_POPUP_BUTTON_MENU_CLICK)
from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox
from outwiker.core.system import getSpecialDirList
from outwiker.utilites.textfile import readTextFile, writeTextFile

from snippets.actions.updatemenu import UpdateMenuAction
from snippets.events import RunSnippetParams
from snippets.gui.snippeteditor import SnippetEditor
from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.utils import getImagesPath, findUniquePath, createFile
import snippets.defines as defines


class TreeItemInfo(object):
    def __init__(self, path, root=False):
        self.path = path
        self.root = root


class EditSnippetsDialog(TestedDialog):
    '''
    Dialog to create, edit and remove snippets and folders.
    '''
    def __init__(self, parent):
        super(EditSnippetsDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        global _
        _ = get_()

        self._width = 800
        self._height = 500
        self.ICON_WIDTH = 16
        self.ICON_HEIGHT = 16

        self.ID_ADD_GROUP = wx.NewId()
        self.ID_ADD_SNIPPET = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_RENAME = wx.NewId()
        self.ID_RUN = wx.NewId()

        self._imagesPath = getImagesPath()
        self._dirImageId = None
        self._snippetImageId = None

        self.addGroupBtn = None
        self.addSnippetBtn = None

        self._varMenuItems = [
            (_(u'Selected text'), defines.VAR_SEL_TEXT),
            (_(u'Page title'), defines.VAR_TITLE),
            (_(u'Page tags list'), defines.VAR_TAGS),
            (_(u'Attachments path'), defines.VAR_ATTACH),
            (_(u'Path to page'), defines.VAR_FOLDER),
            (_(u'Page Id'), defines.VAR_PAGE_ID),
            (_(u'Relative page path'), defines.VAR_SUBPATH),
            (_(u'Current date'), defines.VAR_DATE),
            (_(u'Page creation date'), defines.VAR_DATE_CREATING),
            (_(u'Page modification date'), defines.VAR_DATE_EDITIND),
            (_(u'Page type'), defines.VAR_PAGE_TYPE),
            (_(u'Attachments list'), defines.VAR_ATTACHLIST),
            (_(u'Child pages'), defines.VAR_CHILDLIST),
        ]

        self._blocksMenuItems = [
            (_('{% if %}'), (u'{% if %}', '{% endif %}')),
            (_('{% include %}'), (u"{% include '", u"' %}")),
            (_('{# comment #}'), (u'{# ', ' #}')),
        ]

        self._createGUI()
        self.SetTitle(_(u'Snippets'))
        self.disableSnippetEditor()

    def disableSnippetEditor(self):
        self.snippetEditor.SetText(u'')
        self._snippetPanel.Disable()
        self.runSnippetBtn.Disable()

    def enableSnippetEditor(self):
        self._snippetPanel.Enable()
        self.runSnippetBtn.Enable()

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

        # Run snippet
        self.runSnippetBtn = wx.BitmapButton(
            self,
            id=self.ID_RUN,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "run.png"))
        )
        self.runSnippetBtn.SetToolTipString(_(u"Run snippet"))
        groupButtonsSizer.Add(self.runSnippetBtn, flag=wx.ALL, border=0)

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

        mainSizer.Add(treeSizer, 1, wx.ALL | wx.EXPAND, border=2)

    def _createSnippetButtons(self, snippetButtonsSizer, parent):
        # Insert variable
        self.insertVariableBtn = PopupButton(
            parent,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath,
                                          "variables-menu.png"))
        )
        self.insertVariableBtn.SetToolTipString(_(u"Insert variable"))

        for menuitem in self._varMenuItems:
            data = u'{{' + menuitem[1] + u'}}'
            title = u'{var} - {title}'.format(var=data, title=menuitem[0])
            self.insertVariableBtn.appendMenuItem(title, data)

        self.insertVariableBtn.appendMenuItem(_(u'Other variable...'), None)

        snippetButtonsSizer.Add(self.insertVariableBtn, flag=wx.ALL, border=0)

        # Insert block
        self.insertBlockBtn = PopupButton(
            parent,
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "block-menu.png"))
        )
        self.insertBlockBtn.SetToolTipString(_(u"Insert block"))

        for menuitem in self._blocksMenuItems:
            data = menuitem[1]
            title = menuitem[0]
            self.insertBlockBtn.appendMenuItem(title, data)

        snippetButtonsSizer.Add(self.insertBlockBtn, flag=wx.ALL, border=0)

    def _createSnippetPanel(self, mainSizer):
        self._snippetPanel = wx.Panel(self)

        # Snippet editor
        self.snippetEditor = SnippetEditor(self._snippetPanel)

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

    def _createBottomButtons(self, mainSizer):
        mainSizer.AddStretchSpacer()
        self.closeBtn = wx.Button(self, id=wx.ID_CLOSE)
        mainSizer.Add(self.closeBtn, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
        self.SetEscapeId(wx.ID_CLOSE)

    def _createGUI(self):
        # Main Sizer
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0, 1)
        mainSizer.AddGrowableCol(1, 3)
        mainSizer.AddGrowableRow(0)

        self._createTreePanel(mainSizer)
        self._createSnippetPanel(mainSizer)
        self._createBottomButtons(mainSizer)

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
        self._dialog = EditSnippetsDialog(self._application.mainWindow)
        self._bind()

    def _bind(self):
        self._dialog.Bind(wx.EVT_CLOSE, handler=self._onClose)

        # Buttons
        self._dialog.closeBtn.Bind(wx.EVT_BUTTON, handler=self._onCloseBtn)
        self._dialog.addGroupBtn.Bind(wx.EVT_BUTTON, handler=self._onAddGroup)
        self._dialog.addSnippetBtn.Bind(wx.EVT_BUTTON,
                                        handler=self._onAddSnippet)
        self._dialog.removeBtn.Bind(wx.EVT_BUTTON, handler=self._onRemove)
        self._dialog.renameBtn.Bind(wx.EVT_BUTTON, handler=self._onRenameClick)
        self._dialog.runSnippetBtn.Bind(wx.EVT_BUTTON,
                                        handler=self._onRunSnippet)

        self._dialog.insertVariableBtn.Bind(EVT_POPUP_BUTTON_MENU_CLICK,
                                            handler=self._onInsertVariable)
        self._dialog.insertBlockBtn.Bind(EVT_POPUP_BUTTON_MENU_CLICK,
                                         handler=self._onInsertBlock)

        # Snippets tree
        self.snippetsTree.Bind(wx.EVT_TREE_SEL_CHANGED,
                               handler=self._onTreeItemChanged)
        self.snippetsTree.Bind(wx.EVT_TREE_SEL_CHANGING,
                               handler=self._onTreeItemChanging)
        self.snippetsTree.Bind(wx.EVT_TREE_END_LABEL_EDIT,
                               handler=self._onRenameEnd)
        self.snippetsTree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,
                               handler=self._onRenameBegin)
        self.snippetsTree.Bind(wx.EVT_TREE_BEGIN_DRAG,
                               handler=self._onTreeItemDragBegin)
        self.snippetsTree.Bind(wx.EVT_TREE_END_DRAG,
                               handler=self._onTreeItemDragEnd)

    def ShowDialog(self):
        self._updateSnippetsTree()
        self._dialog.Show()

    def _updateSnippetsTree(self, selectedPath=None):
        snippets_tree = self._loadSnippetsTree()
        if selectedPath is None:
            selectedPath = snippets_tree.path
        self._fillSnippetsTree(snippets_tree, selectedPath)

    def _loadSnippetsTree(self):
        rootdir = getSpecialDirList(defines.SNIPPETS_DIR)[-1]
        sl = SnippetsLoader(rootdir)
        snippets_tree = sl.getSnippets()
        return snippets_tree

    def _fillSnippetsTree(self, snippetsCollection, selectedPath):
        self.snippetsTree.DeleteAllItems()
        info = TreeItemInfo(snippetsCollection.path, True)
        rootId = self._dialog.appendDirTreeItem(None, _(u'Snippets'), info)
        self._buildSnippetsTree(rootId, snippetsCollection, selectedPath)
        self.snippetsTree.ExpandAll()

        if selectedPath == snippetsCollection.path:
            self.snippetsTree.SelectItem(rootId)
            self._dialog.disableSnippetEditor()

    def _buildSnippetsTree(self, parentItemId, snippetsCollection, selectedPath):
        # Append snippet directories
        for subcollection in sorted(snippetsCollection.dirs,
                                    key=lambda x: x.name):
            name = subcollection.name
            path = os.path.join(snippetsCollection.path, name)
            data = TreeItemInfo(path)
            dirItemId = self._dialog.appendDirTreeItem(parentItemId,
                                                       name,
                                                       data)
            self._buildSnippetsTree(dirItemId, subcollection, selectedPath)
            if selectedPath == path:
                self.snippetsTree.SelectItem(dirItemId)

        # Append snippets
        for snippet in sorted(snippetsCollection.snippets):
            name = os.path.basename(snippet)[:-len(defines.EXTENSION)]
            data = TreeItemInfo(snippet)
            snippetItem = self._dialog.appendSnippetTreeItem(
                parentItemId,
                name,
                data)
            if selectedPath == snippet:
                self.snippetsTree.SelectItem(snippetItem)

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
        parent_path = self._getItemData(parentItem).path

        path = self._getItemData(item).path
        path_base = os.path.basename(path)
        result = MessageBox(_(u'Remove directory "{}" and all snippets inside?').format(path_base),
                            _(u"Remove snippets directory"),
                            wx.YES | wx.NO | wx.ICON_QUESTION)
        if result == wx.YES:
            try:
                shutil.rmtree(path)
                snippets_tree = self._loadSnippetsTree()
                self._fillSnippetsTree(snippets_tree, parent_path)
                self._updateMenu()
            except EnvironmentError:
                MessageBox(
                    _(u'Can\'t remove directory "{}"').format(path_base),
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

    def _removeSnippet(self, item):
        parentItem = self.snippetsTree.GetItemParent(item)
        parent_path = self._getItemData(parentItem).path
        path = self._getItemData(item).path
        path_base = os.path.basename(path)[:-len(defines.EXTENSION)]
        result = MessageBox(_(u'Remove snippet "{}"?').format(path_base),
                            _(u"Remove snippet"),
                            wx.YES | wx.NO | wx.ICON_QUESTION)
        if result == wx.YES:
            try:
                os.remove(path)
                snippets_tree = self._loadSnippetsTree()
                self._fillSnippetsTree(snippets_tree, parent_path)
                self._updateMenu()
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
        newpath = findUniquePath(rootdir, _(defines.NEW_DIR_NAME))

        try:
            os.mkdir(newpath)
            snippets_tree = self._loadSnippetsTree()
            self._fillSnippetsTree(snippets_tree, newpath)
            newitem = self.snippetsTree.GetSelection()
            self.snippetsTree.EditLabel(newitem)
            self._updateMenu()
        except EnvironmentError:
            MessageBox(
                _(u"Can't create directory\n{}").format(newpath),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)

    def _isDirItem(self, treeItem):
        '''
        Return True if treeItem is directory item
        '''
        path = self._getItemData(treeItem).path
        return os.path.isdir(path)

    def _checkName(self, label):
        return (label != u'..' and
                label != u'.' and
                len(label) != 0 and
                u'/' not in label and
                u'\\' not in label)

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

        if not self._checkName(newlabel):
            event.Veto()
            return

        if isdir:
            # Rename directory
            newpath = findUniquePath(os.path.dirname(oldpath), newlabel)
        else:
            # Rename snippet
            newpath = findUniquePath(os.path.dirname(oldpath),
                                     newlabel + defines.EXTENSION,
                                     defines.EXTENSION)

        try:
            self._getItemData(item).path = newpath
            os.rename(oldpath, newpath)
            self._updateSnippetsTree(newpath)
        except EnvironmentError as e:
            print(e)

        event.Veto()
        self._updateMenu()

    def _onTreeItemChanged(self, event):
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

    def _getItemData(self, item):
        if not item.IsOk():
            return None
        info = self.snippetsTree.GetItemData(item).GetData()
        return info

    def _getSelectedItemData(self):
        item = self.snippetsTree.GetSelection()
        return self._getItemData(item)

    def _updateMenu(self):
        '''
        Update 'Snippets' menu in main menu.
        '''
        actionController = self._application.actionController
        actionController.getAction(UpdateMenuAction.stringId).run(None)

    def _onAddSnippet(self, event):
        selectedItem = self._getSelectedItemData()
        assert selectedItem is not None
        rootdir = selectedItem.path

        if not os.path.isdir(rootdir):
            rootdir = os.path.dirname(rootdir)

        # Find unique file name for snippets
        newpath = findUniquePath(
            rootdir,
            _(defines.NEW_SNIPPET_NAME) + defines.EXTENSION,
            defines.EXTENSION
        )

        try:
            createFile(newpath)
            snippets_tree = self._loadSnippetsTree()
            self._fillSnippetsTree(snippets_tree, newpath)
            newitem = self.snippetsTree.GetSelection()
            self.snippetsTree.EditLabel(newitem)
            self._updateMenu()
        except EnvironmentError:
            MessageBox(
                _(u"Can't create snippet\n{}").format(newpath),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)

    def _saveItemSnippet(self, item):
        if not item.IsOk():
            return

        path = self._getItemData(item).path
        if os.path.isdir(path):
            return
        try:
            writeTextFile(path, self._dialog.snippetEditor.GetText())
        except EnvironmentError:
            MessageBox(
                _(u"Can't save snippet\n{}").format(path),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)
            raise

    def _onTreeItemChanging(self, event):
        item = event.GetOldItem()
        try:
            self._saveItemSnippet(item)
        except EnvironmentError:
            event.Veto()

    def _onClose(self, event):
        item = self.snippetsTree.GetSelection()
        try:
            self._saveItemSnippet(item)
            self._dialog.Hide()
        except EnvironmentError:
            if event.CanVeto():
                event.Veto()

    def _onCloseBtn(self, event):
        self._dialog.Close()

    def _onInsertBlock(self, event):
        text_left = event.data[0]
        text_right = event.data[1]
        self._dialog.snippetEditor.turnText(text_left, text_right)
        self._dialog.snippetEditor.SetFocus()

    def _onRunSnippet(self, event):
        snippet_fname = self._getSelectedItemData().path
        assert not os.path.isdir(snippet_fname)

        self._dialog.Close()
        if self._application.selectedPage is not None:
            eventParams = RunSnippetParams(snippet_fname, u'')
            self._application.customEvents(defines.EVENT_RUN_SNIPPET,
                                           eventParams)

    def _onInsertVariable(self, event):
        text = event.data
        if text is None:
            with wx.TextEntryDialog(self._dialog,
                                    _(u'Enter variable name (English leters, numbers and _ only)'),
                                    _(u'Variable name'),
                                    u'varname') as dlg:
                name_ok = False
                while not name_ok:
                    result = dlg.ShowModal()
                    if result != wx.ID_OK:
                        return
                    text = dlg.GetValue()
                    name_ok = self._checkVarName(text)
                    if not name_ok:
                        MessageBox(
                            _(u'Invalid variable name "{}"').format(text),
                            _(u"Error"),
                            wx.ICON_ERROR | wx.OK)
                    text = u'{{' + text + u'}}'

        self._dialog.snippetEditor.replaceText(text)
        self._dialog.snippetEditor.SetFocus()

    def _checkVarName(self, name):
        regex = re.compile('[a-zA-Z][a-zA-Z0-9_]*$')
        result = (name is not None and
                  len(name) > 0 and
                  regex.match(name) is not None)
        return result

    def _onTreeItemDragBegin(self, event):
        item = event.GetItem()
        if self._isRootItem(item):
            return

        event.Allow()
        self._treeDragSource = self._getItemData(item).path

    def _onTreeItemDragEnd(self, event):
        treeDragTarget = event.GetItem()
        dropPath = self._getItemData(treeDragTarget).path
        sourceParent = os.path.dirname(self._treeDragSource)

        if not os.path.isdir(dropPath):
            dropPath = os.path.dirname(dropPath)

        if dropPath.startswith(self._treeDragSource):
            return

        if sourceParent == dropPath:
            return

        print('{} -> {}'.format(self._treeDragSource, dropPath))
        self._updateSnippetsTree(dropPath)
