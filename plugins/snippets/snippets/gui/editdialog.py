# -*- coding: utf-8 -*-

import re
import os
import shutil

import wx

from outwiker.api.app.config import MainWindowConfig
from outwiker.api.app.application import getSpecialDirList
from outwiker.api.gui.dialogs import MessageBox
from outwiker.api.gui.controls import PopupButton, EVT_POPUP_BUTTON_MENU_CLICK
from outwiker.api.gui.controls import SafeImageList
from outwiker.api.core.text import readTextFile, writeTextFile

from snippets.events import RunSnippetParams
from snippets.gui.snippeteditor import SnippetEditor
from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.utils import (
    getImagesPath,
    findUniquePath,
    createFile,
    moveSnippetsTo,
    openHelp,
)
import snippets.defines as defines
from snippets.snippetparser import SnippetParser, SnippetException
from snippets.config import SnippetsConfig


class TreeItemInfo(object):
    def __init__(self, path, root=False):
        self.path = path
        self.root = root


class EditSnippetsDialog(wx.Frame):
    """
    Dialog to create, edit and remove snippets and folders.
    """

    def __init__(self, parent, application):
        super().__init__(
            parent,
            style=wx.CAPTION
            | wx.CLOSE
            | wx.SYSTEM_MENU
            | wx.MINIMIZE_BOX
            | wx.MAXIMIZE_BOX
            | wx.CLOSE_BOX
            | wx.RESIZE_BORDER
            | wx.FRAME_TOOL_WINDOW
            | wx.FRAME_NO_TASKBAR
            | wx.FRAME_FLOAT_ON_PARENT,
        )
        global _
        _ = get_()

        self._application = application

        self.ICON_WIDTH = 16
        self.ICON_HEIGHT = 16

        self._imagesPath = getImagesPath()
        self._dirImageId = None
        self._snippetImageId = None

        self.addGroupBtn = None
        self.addSnippetBtn = None

        self._varMenuItems = [
            (_("Selected text"), defines.VAR_SEL_TEXT),
            (_("Current date"), defines.VAR_DATE),
            (_("Page title"), defines.VAR_TITLE),
            (_("Page type"), defines.VAR_PAGE_TYPE),
            (_("Page tags list"), defines.VAR_TAGS),
            (_("Attachments path"), defines.VAR_ATTACH),
            (_("Path to page"), defines.VAR_FOLDER),
            (_("Relative page path"), defines.VAR_SUBPATH),
            (_("Page creation date"), defines.VAR_DATE_CREATING),
            (_("Page modification date"), defines.VAR_DATE_EDITIND),
            (_("Page Id"), defines.VAR_PAGE_ID),
            (_("Attachments list"), defines.VAR_ATTACHLIST),
            (_("Child pages"), defines.VAR_CHILDLIST),
        ]

        self._blocksMenuItems = [
            (_("{% if %}"), ("{% if %}", "{% elif %}{% else %}{% endif %}")),
            (_("{% include %}"), ("{% include '", "' %}")),
            (_("{# comment #}"), ("{# ", " #}")),
        ]

        self._createGUI()
        self.SetTitle(_("Snippets management"))
        self.disableSnippetEditor()

    def disableSnippetEditor(self):
        self.snippetEditor.SetText("")
        self._snippetPanel.Disable()
        self.runSnippetBtn.Disable()

    def enableSnippetEditor(self):
        self._snippetPanel.Enable()
        self.runSnippetBtn.Enable()

    def appendDirTreeItem(self, parentItem, name, data):
        itemData = data
        if parentItem is not None:
            newItemId = self.snippetsTree.AppendItem(
                parentItem, name, self._dirImageId, data=itemData
            )
        else:
            newItemId = self.snippetsTree.AddRoot(name, self._dirImageId, data=itemData)
        return newItemId

    def appendSnippetTreeItem(self, parentItem, name, data):
        itemData = data
        newItemId = self.snippetsTree.AppendItem(
            parentItem, name, self._snippetImageId, data=itemData
        )
        return newItemId

    def _createTreeButtons(self, groupButtonsSizer):
        # Add a group button
        self.addGroupBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "folder_add.png"))
        )
        self.addGroupBtn.SetToolTip(_("Add new snippets group"))
        groupButtonsSizer.Add(self.addGroupBtn, flag=wx.ALL, border=0)

        # Add a snippet button
        self.addSnippetBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "snippet_add.png"))
        )
        self.addSnippetBtn.SetToolTip(_("Create new snippet"))
        groupButtonsSizer.Add(self.addSnippetBtn, flag=wx.ALL, border=0)

        # Rename group or snippet button
        self.renameBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "rename.png"))
        )
        self.renameBtn.SetToolTip(_("Rename"))
        groupButtonsSizer.Add(self.renameBtn, flag=wx.ALL, border=0)

        # Remove group or snippet button
        self.removeBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "remove.png"))
        )
        self.removeBtn.SetToolTip(_("Remove"))
        groupButtonsSizer.Add(self.removeBtn, flag=wx.ALL, border=0)

        # Run snippet
        self.runSnippetBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "run.png"))
        )
        self.runSnippetBtn.SetToolTip(_("Run snippet"))
        groupButtonsSizer.Add(self.runSnippetBtn, flag=wx.ALL, border=0)

        # Open help
        self.openHelpBtn = wx.BitmapButton(
            self, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "help.png"))
        )
        self.openHelpBtn.SetToolTip(_("Open help..."))
        groupButtonsSizer.Add(self.openHelpBtn, flag=wx.ALL, border=0)

    def _createImagesList(self):
        self._imagelist = SafeImageList(self.ICON_WIDTH, self.ICON_HEIGHT)

        self._dirImageId = self._imagelist.Add(
            wx.Bitmap(os.path.join(self._imagesPath, "folder.png"))
        )

        self._snippetImageId = self._imagelist.Add(
            wx.Bitmap(os.path.join(self._imagesPath, "snippet.png"))
        )

    def _createTreePanel(self, mainSizer):
        self._createImagesList()

        self.snippetsTree = wx.TreeCtrl(
            self, style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER
        )
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
            bitmap=wx.Bitmap(os.path.join(self._imagesPath, "variables-menu.png")),
        )
        self.insertVariableBtn.SetToolTip(_("Insert variable"))

        for menuitem in self._varMenuItems:
            data = "{{" + menuitem[1] + "}}"
            title = "{var} - {title}".format(var=data, title=menuitem[0])
            self.insertVariableBtn.appendMenuItem(title, data)

        self.insertVariableBtn.appendMenuItem(_("Other variable..."), None)

        snippetButtonsSizer.Add(self.insertVariableBtn, flag=wx.ALL, border=0)

        # Insert block
        self.insertBlockBtn = PopupButton(
            parent, bitmap=wx.Bitmap(os.path.join(self._imagesPath, "block-menu.png"))
        )
        self.insertBlockBtn.SetToolTip(_("Insert block"))

        for menuitem in self._blocksMenuItems:
            data = menuitem[1]
            title = menuitem[0]
            self.insertBlockBtn.appendMenuItem(title, data)

        snippetButtonsSizer.Add(self.insertBlockBtn, flag=wx.ALL, border=0)

    def _createSnippetPanel(self, mainSizer):
        self._snippetPanel = wx.Panel(self)

        # Snippet editor
        self.snippetEditor = SnippetEditor(self._snippetPanel, self._application)

        # Buttons for snippet
        snippetButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._createSnippetButtons(snippetButtonsSizer, self._snippetPanel)

        # Errors messages
        self.errorsTextCtrl = wx.TextCtrl(
            self._snippetPanel, style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        self.errorsTextCtrl.SetMinSize((-1, 100))

        # SnippetSizer
        snippetSizer = wx.FlexGridSizer(cols=1)
        snippetSizer.AddGrowableRow(1)
        snippetSizer.AddGrowableCol(0)

        snippetSizer.Add(snippetButtonsSizer, 1, wx.EXPAND, border=2)
        snippetSizer.Add(self.snippetEditor, 1, wx.EXPAND, border=2)
        snippetSizer.Add(self.errorsTextCtrl, 1, wx.EXPAND, border=2)

        self._snippetPanel.SetSizer(snippetSizer)
        mainSizer.Add(self._snippetPanel, 1, wx.ALL | wx.EXPAND, border=2)

    def _createBottomButtons(self, mainSizer):
        mainSizer.AddStretchSpacer()
        self.closeBtn = wx.Button(self, id=wx.ID_CLOSE, label=_("Close"))
        mainSizer.Add(self.closeBtn, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)

    def _createMenu(self):
        self._menuBar = wx.MenuBar()
        editMenu = self._createEditMenu()
        fileMenu = self._createFileMenu()
        helpMenu = self._createHelpMenu()
        self._menuBar.Append(fileMenu, _("File"))
        self._menuBar.Append(editMenu, _("Edit"))
        self._menuBar.Append(helpMenu, _("Help"))
        self.SetMenuBar(self._menuBar)

    def _createFileMenu(self):
        menu = wx.Menu()
        menu.Append(
            self.addGroupBtn.GetId(), _("Add new snippets group") + "\tCtrl+Shift+N"
        )
        menu.Append(self.addSnippetBtn.GetId(), _("Create new snippet") + "\tCtrl+N")
        menu.Append(self.renameBtn.GetId(), _("Rename") + "\tF2")
        menu.Append(self.removeBtn.GetId(), _("Remove") + "\tCtrl+Del")
        menu.Append(self.runSnippetBtn.GetId(), _("Run snippet") + "\tF5")
        return menu

    def _createHelpMenu(self):
        menu = wx.Menu()
        menu.Append(self.openHelpBtn.GetId(), _("Open help...") + "\tF1")
        return menu

    def _createEditMenu(self):
        menu = wx.Menu()
        menu.Append(wx.ID_UNDO, _("Undo") + "\tCtrl+Z")
        menu.Append(wx.ID_REDO, _("Redo") + "\tCtrl+Y")
        menu.AppendSeparator()
        menu.Append(wx.ID_CUT, _("Cut") + "\tCtrl+X")
        menu.Append(wx.ID_COPY, _("Copy") + "\tCtrl+C")
        menu.Append(wx.ID_PASTE, _("Paste") + "\tCtrl+V")
        menu.AppendSeparator()
        menu.Append(wx.ID_SELECTALL, _("Select All") + "\tCtrl+A")
        return menu

    def _createGUI(self):
        # Main Sizer
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0, 1)
        mainSizer.AddGrowableCol(1, 3)
        mainSizer.AddGrowableRow(0)

        self._createTreePanel(mainSizer)
        self._createSnippetPanel(mainSizer)
        self._createBottomButtons(mainSizer)
        self._createMenu()

        self.SetSizer(mainSizer)
        self.Layout()

    @property
    def currentSnippet(self):
        return self.snippetEditor.GetText().replace("\r\n", "\n")

    def setError(self, text):
        self.errorsTextCtrl.SetValue(text)


class EditSnippetsDialogController(object):
    """
    Controller to manage EditSnippetsDialog.
    """

    def __init__(self, application):
        global _
        _ = get_()
        self._application = application
        self._snippetChanged = False
        self._dialog = EditSnippetsDialog(self._application.mainWindow, self._application)
        self._config = SnippetsConfig(self._application.config)
        self._mainWindowconfig = MainWindowConfig(self._application.config)
        self._dialog.SetClientSize(
            (self._config.editDialogWidth, self._config.editDialogHeight)
        )
        self._dialog.SetBackgroundColour(
            self._mainWindowconfig.mainPanesBackgroundColor.value
        )
        self._bind()

    def _bind(self):
        self._dialog.Bind(wx.EVT_CLOSE, handler=self._onClose)

        # Buttons
        self._dialog.closeBtn.Bind(wx.EVT_BUTTON, handler=self._onCloseBtn)

        self._dialog.addGroupBtn.Bind(wx.EVT_BUTTON, handler=self._onAddGroup)
        self._dialog.Bind(
            wx.EVT_MENU, id=self._dialog.addGroupBtn.GetId(), handler=self._onAddGroup
        )

        self._dialog.addSnippetBtn.Bind(wx.EVT_BUTTON, handler=self._onAddSnippet)
        self._dialog.Bind(
            wx.EVT_MENU,
            id=self._dialog.addSnippetBtn.GetId(),
            handler=self._onAddSnippet,
        )

        self._dialog.removeBtn.Bind(wx.EVT_BUTTON, handler=self._onRemove)
        self._dialog.Bind(
            wx.EVT_MENU, id=self._dialog.removeBtn.GetId(), handler=self._onRemove
        )

        self._dialog.renameBtn.Bind(wx.EVT_BUTTON, handler=self._onRenameClick)
        self._dialog.Bind(
            wx.EVT_MENU, id=self._dialog.renameBtn.GetId(), handler=self._onRenameClick
        )

        self._dialog.runSnippetBtn.Bind(wx.EVT_BUTTON, handler=self._onRunSnippet)
        self._dialog.Bind(
            wx.EVT_MENU,
            id=self._dialog.runSnippetBtn.GetId(),
            handler=self._onRunSnippet,
        )

        self._dialog.openHelpBtn.Bind(wx.EVT_BUTTON, handler=self._onOpenHelp)
        self._dialog.Bind(
            wx.EVT_MENU, id=self._dialog.openHelpBtn.GetId(), handler=self._onOpenHelp
        )

        self._dialog.insertVariableBtn.Bind(
            EVT_POPUP_BUTTON_MENU_CLICK, handler=self._onInsertVariable
        )
        self._dialog.insertBlockBtn.Bind(
            EVT_POPUP_BUTTON_MENU_CLICK, handler=self._onInsertBlock
        )

        # Snippets tree
        self.snippetsTree.Bind(wx.EVT_TREE_SEL_CHANGED, handler=self._onTreeItemChanged)
        self.snippetsTree.Bind(
            wx.EVT_TREE_SEL_CHANGING, handler=self._onTreeItemChanging
        )
        self.snippetsTree.Bind(wx.EVT_TREE_END_LABEL_EDIT, handler=self._onRenameEnd)
        self.snippetsTree.Bind(
            wx.EVT_TREE_BEGIN_LABEL_EDIT, handler=self._onRenameBegin
        )
        self.snippetsTree.Bind(
            wx.EVT_TREE_BEGIN_DRAG, handler=self._onTreeItemDragBegin
        )
        self.snippetsTree.Bind(wx.EVT_TREE_END_DRAG, handler=self._onTreeItemDragEnd)

        # Snippet editor
        self._dialog.snippetEditor.Bind(
            wx.stc.EVT_STC_CHANGE, handler=self._onSnippetEdit
        )
        self._dialog.snippetEditor.Bind(wx.EVT_IDLE, handler=self._onSnippetEditIdle)

    def ShowDialog(self):
        self._updateSnippetsTree()
        self._dialog.Show()

    def _onSnippetEdit(self, event):
        self._snippetChanged = True

    def _onSnippetEditIdle(self, event):
        if not self._snippetChanged:
            return

        path = self._getSelectedItemData().path
        if os.path.isdir(path):
            return

        snippet_text = self._dialog.currentSnippet
        parser = SnippetParser(snippet_text, os.path.dirname(path), self._application)
        try:
            parser.getVariables()
        except SnippetException as e:
            self._dialog.setError(e.message)
        else:
            self._dialog.setError(_("No snippet errors"))

        self._snippetChanged = False

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
        rootId = self._dialog.appendDirTreeItem(None, _("Snippets"), info)
        self._buildSnippetsTree(rootId, snippetsCollection, selectedPath)
        self.snippetsTree.ExpandAll()

        if selectedPath == snippetsCollection.path:
            self.snippetsTree.SelectItem(rootId)
            self._dialog.disableSnippetEditor()

    def _buildSnippetsTree(self, parentItemId, snippetsCollection, selectedPath):
        # Append snippet directories
        for subcollection in sorted(snippetsCollection.dirs, key=lambda x: x.name):
            name = subcollection.name
            path = os.path.join(snippetsCollection.path, name)
            data = TreeItemInfo(path)
            dirItemId = self._dialog.appendDirTreeItem(parentItemId, name, data)
            self._buildSnippetsTree(dirItemId, subcollection, selectedPath)
            if selectedPath == path:
                self.snippetsTree.SelectItem(dirItemId)

        # Append snippets
        for snippet in sorted(snippetsCollection.snippets):
            name = os.path.basename(snippet)
            data = TreeItemInfo(snippet)
            snippetItem = self._dialog.appendSnippetTreeItem(parentItemId, name, data)
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
        result = MessageBox(
            _('Remove directory "{}" and all snippets inside?').format(path_base),
            _("Remove snippets directory"),
            wx.YES | wx.NO | wx.ICON_QUESTION,
        )
        if result == wx.YES:
            try:
                shutil.rmtree(path)
                snippets_tree = self._loadSnippetsTree()
                self._fillSnippetsTree(snippets_tree, parent_path)
                self._updateMenu()
            except EnvironmentError:
                MessageBox(
                    _('Can\'t remove directory "{}"').format(path_base),
                    _("Error"),
                    wx.ICON_ERROR | wx.OK,
                )

    def _removeSnippet(self, item):
        parentItem = self.snippetsTree.GetItemParent(item)
        parent_path = self._getItemData(parentItem).path
        path = self._getItemData(item).path
        path_base = os.path.basename(path)
        result = MessageBox(
            _('Remove snippet "{}"?').format(path_base),
            _("Remove snippet"),
            wx.YES | wx.NO | wx.ICON_QUESTION,
        )
        if result == wx.YES:
            try:
                os.remove(path)
                snippets_tree = self._loadSnippetsTree()
                self._fillSnippetsTree(snippets_tree, parent_path)
                self._updateMenu()
            except EnvironmentError:
                MessageBox(
                    _('Can\'t remove snippet "{}"').format(path_base),
                    _("Error"),
                    wx.ICON_ERROR | wx.OK,
                )

    def _onAddGroup(self, event):
        """
        Add group button click
        """
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
            self._scrollToSelectedItem()
        except EnvironmentError:
            MessageBox(
                _("Can't create directory\n{}").format(newpath),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )

    def _isDirItem(self, treeItem):
        """
        Return True if treeItem is directory item
        """
        path = self._getItemData(treeItem).path
        return os.path.isdir(path)

    def _checkName(self, label):
        return (
            label != ".."
            and label != "."
            and len(label) != 0
            and "/" not in label
            and "\\" not in label
        )

    def _onRenameEnd(self, event):
        """
        Rename button event handler
        """
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
            newpath = findUniquePath(os.path.dirname(oldpath), newlabel, "")

        try:
            self._getItemData(item).path = newpath
            os.rename(oldpath, newpath)
            self._updateSnippetsTree(newpath)
            self._scrollToSelectedItem()
        except EnvironmentError as e:
            MessageBox(
                _("Can't rename the snippet '{}'\n{}").format(oldpath, e),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )

        event.Veto()
        self._updateMenu()

    def _onTreeItemChanged(self, event):
        item = event.GetItem()
        info = self._getItemData(item)
        if os.path.isdir(info.path):
            # Selected item is directory
            self._dialog.disableSnippetEditor()
            self._dialog.snippetEditor.SetText("")
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
                _("Can't read the snippet\n{}").format(info.path),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )

    def _getItemData(self, item):
        if not item.IsOk():
            return None
        info = self.snippetsTree.GetItemData(item)
        return info

    def _getSelectedItemData(self):
        item = self.snippetsTree.GetSelection()
        return self._getItemData(item)

    def _scrollToSelectedItem(self):
        item = self.snippetsTree.GetSelection()
        if item.IsOk():
            self.snippetsTree.ScrollTo(item)

    def _updateMenu(self):
        """
        Update 'Snippets' menu in main menu.
        """
        self._application.customEvents(defines.EVENT_UPDATE_MENU, None)

    def _onAddSnippet(self, event):
        selectedItem = self._getSelectedItemData()
        assert selectedItem is not None
        rootdir = selectedItem.path

        if not os.path.isdir(rootdir):
            rootdir = os.path.dirname(rootdir)

        # Find unique file name for snippets
        newpath = findUniquePath(rootdir, _(defines.NEW_SNIPPET_NAME), "")

        try:
            createFile(newpath)
            snippets_tree = self._loadSnippetsTree()
            self._fillSnippetsTree(snippets_tree, newpath)
            newitem = self.snippetsTree.GetSelection()
            self.snippetsTree.EditLabel(newitem)
            self._updateMenu()
            self._scrollToSelectedItem()
        except EnvironmentError:
            MessageBox(
                _("Can't create snippet\n{}").format(newpath),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )

    def _saveItemSnippet(self, item):
        if not item.IsOk():
            return

        path = self._getItemData(item).path
        if os.path.isdir(path):
            return
        try:
            writeTextFile(path, self._dialog.currentSnippet)
        except EnvironmentError:
            MessageBox(
                _("Can't save snippet\n{}").format(path),
                _("Error"),
                wx.ICON_ERROR | wx.OK,
            )
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
                return

        try:
            w, h = self._dialog.GetClientSize()
            self._config.editDialogWidth = w
            self._config.editDialogHeight = h
        except EnvironmentError:
            pass

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
            eventParams = RunSnippetParams(snippet_fname)
            self._application.customEvents(defines.EVENT_RUN_SNIPPET, eventParams)

    def _onOpenHelp(self, event):
        openHelp()

    def _onInsertVariable(self, event):
        text = event.data
        if text is None:
            with wx.TextEntryDialog(
                self._dialog,
                _("Enter variable name (English leters, numbers and _ only)"),
                _("Variable name"),
                "varname",
            ) as dlg:
                name_ok = False
                while not name_ok:
                    result = dlg.ShowModal()
                    if result != wx.ID_OK:
                        return
                    text = dlg.GetValue()
                    name_ok = self._checkVarName(text)
                    if not name_ok:
                        MessageBox(
                            _('Invalid variable name "{}"').format(text),
                            _("Error"),
                            wx.ICON_ERROR | wx.OK,
                        )
                    text = "{{" + text + "}}"

        self._dialog.snippetEditor.replaceText(text)
        self._dialog.snippetEditor.SetFocus()

    def _checkVarName(self, name):
        regex = re.compile("[a-zA-Z][a-zA-Z0-9_]*$")
        result = name is not None and len(name) > 0 and regex.match(name) is not None
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

        result_path = moveSnippetsTo(self._treeDragSource, dropPath)
        self._updateSnippetsTree(result_path)
        self._updateMenu()
        self._scrollToSelectedItem()
