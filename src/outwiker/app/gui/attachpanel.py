# -*- coding: utf-8 -*-

import logging
import os.path
from typing import List
from datetime import datetime

import wx

from outwiker.app.actions.clipboard import CopyAttachPathAction

from outwiker.app.actions.attachcreatesubdir import AttachCreateSubdirActionForAttachPanel
from outwiker.app.actions.attachexecute import AttachExecuteFilesAction
from outwiker.app.actions.attachfiles import AttachFilesActionForAttachPanel
from outwiker.app.actions.attachfolder import AttachFolderActionForAttachPanel
from outwiker.app.actions.attachpastelink import AttachPasteLinkActionForAttachPanel
from outwiker.app.actions.attachselectall import AttachSelectAllAction
from outwiker.app.actions.attachopenfolder import OpenAttachFolderActionForAttachPanel
from outwiker.app.actions.attachrename import RenameAttachActionForAttachPanel
from outwiker.app.actions.attachremove import RemoveAttachesActionForAttachPanel

from outwiker.app.gui.dropfiles import BaseDropFilesTarget
from outwiker.app.gui.mainwindowtools import addStatusBarItem, setStatusText

from outwiker.app.services.attachment import attachFiles, renameAttach
from outwiker.app.services.messages import showError

from outwiker.core.attachment import Attachment
from outwiker.core.events import (BeginAttachRenamingParams,
                                  AttachSelectionChangedParams)
from outwiker.core.system import getBuiltinImagePath, getOS

from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.gui.guiconfig import AttachConfig, GeneralGuiConfig


logger = logging.getLogger('outwiker.gui.attachpanel')


class AttachPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self._attach_config = AttachConfig(self._application.config)
        self._general_config = GeneralGuiConfig(self._application.config)
        self.GO_TO_PARENT_ITEM_NAME = '..'
        self._ATTACH_STATUS_ITEM = 'STATUSBAR_ATTACH'

        # Store old file name before renaming
        self._oldEditedAttachName = None
        self._oldEditedAttachItemIndex = None

        # Actions with hot keys for attach panel
        self._localHotKeys = [
            RemoveAttachesActionForAttachPanel,
            AttachSelectAllAction,
            AttachPasteLinkActionForAttachPanel,
            AttachExecuteFilesAction,
            RenameAttachActionForAttachPanel,
            AttachCreateSubdirActionForAttachPanel]

        self.__attachList = wx.ListCtrl(self,
                                        wx.ID_ANY,
                                        style=wx.LC_LIST | wx.LC_EDIT_LABELS | wx.SUNKEN_BORDER)

        self.__toolbar = self._createGui(self)
        self.__attachList.SetMinSize((-1, 100))
        self._do_layout()

        self.__fileIcons = getOS().fileIcons
        self.__attachList.SetImageList(self.__fileIcons.imageList,
                                       wx.IMAGE_LIST_SMALL)
        self._dropTarget = DropAttachFilesTarget(self._application, self)

        self._bindGuiEvents()
        self._bindAppEvents()
        addStatusBarItem(self._ATTACH_STATUS_ITEM, position=1)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.__attachList.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.__attachList.SetForegroundColour(colour)

    def _isSubdirectory(self, root_dirname, sub_dirname):
        full_dir = os.path.join(root_dirname, sub_dirname)
        return os.path.exists(full_dir) and os.path.isdir(full_dir)

    def _bindGuiEvents(self):
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,
                  self._onBeginDrag,
                  self.__attachList)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
                  self._onDoubleClick,
                  self.__attachList)

        self.Bind(wx.EVT_CLOSE, self._onClose)

        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT,
                  self._onBeginLabelEdit,
                  self.__attachList)

        self.Bind(wx.EVT_LIST_END_LABEL_EDIT,
                  self._onEndLabelEdit,
                  self.__attachList)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED,
                  self._onAttachSelected,
                  self.__attachList)

        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                  self._onAttachSelected,
                  self.__attachList)

    def _unbindGuiEvents(self):
        self.Unbind(wx.EVT_LIST_BEGIN_DRAG,
                    handler=self._onBeginDrag,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_ITEM_ACTIVATED,
                    handler=self._onDoubleClick,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_BEGIN_LABEL_EDIT,
                    handler=self._onBeginLabelEdit,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_END_LABEL_EDIT,
                    handler=self._onEndLabelEdit,
                    source=self.__attachList)

        self.Unbind(wx.EVT_CLOSE, handler=self._onClose)

        self.Unbind(wx.EVT_LIST_ITEM_SELECTED,
                    handler=self._onAttachSelected,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_ITEM_DESELECTED,
                    handler=self._onAttachSelected,
                    source=self.__attachList)

    @property
    def attachList(self):
        return self.__attachList

    @property
    def toolBar(self):
        return self.__toolbar

    def _bindAppEvents(self):
        self._application.onPageSelect += self._onPageSelect
        self._application.onAttachListChanged += self._onAttachListChanged
        self._application.onAttachSubdirChanged += self._onAttachSubdirChanged
        self._application.onWikiOpen += self._onWikiOpen
        self._application.onBeginAttachRenaming += self._onBeginAttachRenaming
        self._application.onPreferencesDialogClose += self._onPreferencesDialogClose

    def _unbindAppEvents(self):
        self._application.onPageSelect -= self._onPageSelect
        self._application.onAttachListChanged -= self._onAttachListChanged
        self._application.onAttachSubdirChanged -= self._onAttachSubdirChanged
        self._application.onWikiOpen -= self._onWikiOpen
        self._application.onBeginAttachRenaming -= self._onBeginAttachRenaming
        self._application.onPreferencesDialogClose -= self._onPreferencesDialogClose

    def _onClose(self, _event):
        actionController = self._application.actionController

        for action, hotkey, hidden in self._actions:
            actionController.removeHotkey(action.stringId)
            actionController.removeToolbarButton(action.stringId)

        self._dropTarget.destroy()
        self._unbindAppEvents()
        self._unbindGuiEvents()
        self.toolBar.ClearTools()
        self.attachList.ClearAll()
        self.__fileIcons.clear()
        self.Destroy()

    def _enableHotkeys(self):
        actionController = self._application.actionController
        for action in self._localHotKeys:
            actionController.appendHotkey(action.stringId, self)

    def _disableHotkeys(self):
        actionController = self._application.actionController
        for action in self._localHotKeys:
            actionController.removeHotkey(action.stringId)

    def _createGui(self, parent):
        toolbar = wx.ToolBar(parent, wx.ID_ANY, style=wx.TB_DOCKABLE)
        actionController = self._application.actionController
        self._enableHotkeys()

        # Attach files
        actionController.appendToolbarButton(
            AttachFilesActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("attach.svg")
        )

        # Attach Folder
        actionController.appendToolbarButton(
            AttachFolderActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("attach_folder.svg")
        )

        # Create subdir
        actionController.appendToolbarButton(
            AttachCreateSubdirActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("folder_add.svg")
        )

        # Delete files
        actionController.appendToolbarButton(
            RemoveAttachesActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("delete.png")
        )

        # Rename file
        actionController.appendToolbarButton(
            RenameAttachActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("rename.svg")
        )

        # Select all files
        actionController.appendToolbarButton(
            AttachSelectAllAction.stringId,
            toolbar,
            getBuiltinImagePath("select_all.png")
        )

        toolbar.AddSeparator()

        # Paste link to files
        actionController.appendToolbarButton(
            AttachPasteLinkActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("paste.png")
        )

        # Execute attachments
        actionController.appendToolbarButton(
            AttachExecuteFilesAction.stringId,
            toolbar,
            getBuiltinImagePath("execute.png")
        )

        # Open attach folder
        actionController.appendToolbarButton(
            OpenAttachFolderActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("folder_open.png")
        )

        # Copy path to clipboard
        actionController.appendToolbarButton(
            CopyAttachPathAction.stringId,
            toolbar,
            getBuiltinImagePath("folder_clipboard.png")
        )

        toolbar.Realize()
        return toolbar

    def _do_layout(self):
        attachSizer_copy = wx.FlexGridSizer(2, 1, 0, 0)
        attachSizer_copy.Add(self.__toolbar, 1, wx.EXPAND, 0)
        attachSizer_copy.Add(self.__attachList, 1, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(attachSizer_copy)
        attachSizer_copy.Fit(self)
        attachSizer_copy.AddGrowableRow(1)
        attachSizer_copy.AddGrowableCol(0)

        attachSizer_copy.Fit(self)
        self.SetAutoLayout(True)

    def _onWikiOpen(self, _wiki):
        self.updateAttachments()

    def _onPageSelect(self, _page):
        self.updateAttachments()

    def _sortFilesList(self, files_list):
        result = sorted(files_list, key=str.lower, reverse=True)
        result.sort(key=Attachment.sortByType)
        return result

    def updateAttachments(self):
        """
        Обновить список прикрепленных файлов
        """
        showHiddenDirs = self._attach_config.showHiddenDirs.value

        self.__attachList.Freeze()
        page = self._application.selectedPage

        # Store selected items
        selected_items = []
        selectedItem = self.__attachList.GetFirstSelected()
        while selectedItem != -1:
            selected_items.append(self.__attachList.GetItemText(selectedItem))
            selectedItem = self.__attachList.GetNextSelected(selectedItem)

        self.__attachList.ClearAll()
        if page is not None:
            files = Attachment(self._application.selectedPage).getAttachFull(
                page.currentAttachSubdir)
            files = self._sortFilesList(files)

            for fname in files:
                if (showHiddenDirs or
                        not os.path.basename(fname).startswith("__") or
                        not page.isCurrentAttachSubdirRoot() or
                        not os.path.isdir(fname)):
                    # Отключим уведомления об ошибках во всплывающих окнах
                    # иначе они появляются при попытке прочитать
                    # испорченные иконки
                    # На результат работы это не сказывается,
                    # все-равно бракованные иконки отлавливаются.
                    wx.Log.EnableLogging(False)

                    imageIndex = self.__fileIcons.getFileImage(fname)

                    # Вернем всплывающие окна с ошибками
                    wx.Log.EnableLogging(True)

                    self.__attachList.InsertItem(
                        0,
                        os.path.basename(fname),
                        imageIndex)

            if not page.isCurrentAttachSubdirRoot():
                self.__attachList.InsertItem(
                    0,
                    self.GO_TO_PARENT_ITEM_NAME,
                    self.__fileIcons.GO_TO_PARENT_ICON)

            # Restore selected items
            for item_name in selected_items:
                index = self.__attachList.FindItem(-1, item_name)
                if index != -1:
                    self.__attachList.Select(index)

        self.__attachList.Thaw()
        self._sendAttachSelectedEvent()

    def _selectFile(self, fname):
        if fname is None:
            return

        if self.__attachList.GetItemCount() == 0:
            return

        for n in range(self.__attachList.GetItemCount()):
            if self.__attachList.GetItemText(n) == fname:
                self.__attachList.Select(n)
            else:
                self.__attachList.Select(n, 0)

    def getSelectedFiles(self):
        page = self._application.selectedPage

        files = []
        item = self.__attachList.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)

        prefix_list = ['./', '.\\']
        while item != -1:
            item_text = self.__attachList.GetItemText(item)

            if item_text != self.GO_TO_PARENT_ITEM_NAME:
                fname = os.path.join(page.currentAttachSubdir, item_text)

                # Remove prefixes
                for prefix in prefix_list:
                    if fname.startswith(prefix):
                        fname = fname[len(prefix):]

                files.append(fname)

            item = self.__attachList.GetNextItem(item,
                                                 state=wx.LIST_STATE_SELECTED)

        return files

    def _onRemove(self, _event):
        if self._application.selectedPage is not None:
            files = self.getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _("You did not select any file to remove"))
                return

            if MessageBox(_("Remove selected files?"),
                          _("Remove files?"),
                          wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                try:
                    Attachment(
                        self._application.selectedPage).removeAttach(files)
                except IOError as e:
                    showError(self._application.mainWindow, str(e))

    def _onDoubleClick(self, event):
        config = AttachConfig(self._application.config)
        actionController = self._application.actionController
        page = self._application.selectedPage

        attach_dir = Attachment(
            self._application.selectedPage).getAttachPath(create=False)
        selected_item = event.GetText()
        subdir = os.path.normpath(os.path.join(page.currentAttachSubdir,
                                               selected_item))
        if self._isSubdirectory(attach_dir, subdir):
            self._application.selectedPage.currentAttachSubdir = subdir
        elif config.doubleClickAction.value == AttachConfig.ACTION_INSERT_LINK:
            actionController.getAction(
                AttachPasteLinkActionForAttachPanel.stringId).run(None)
        elif config.doubleClickAction.value == AttachConfig.ACTION_OPEN:
            actionController.getAction(
                AttachExecuteFilesAction.stringId).run(None)

    def _onBeginDrag(self, _event):
        selectedFiles = self.getSelectedFiles()
        if not selectedFiles:
            return

        page = self._application.selectedPage
        data = wx.FileDataObject()
        attach_path = Attachment(page).getAttachPath(page.currentAttachSubdir)

        for fname in self.getSelectedFiles():
            data.AddFile(os.path.join(attach_path, fname))

        dragSource = wx.DropSource(data, self)
        dragSource.DoDragDrop()

    def _onAttachListChanged(self, page, _params):
        if page is not None and page == self._application.selectedPage:
            self.updateAttachments()

    def _onAttachSubdirChanged(self, page, _params):
        if page is not None and page == self._application.selectedPage:
            self.updateAttachments()

    def _onBeginAttachRenaming(self, page, params: BeginAttachRenamingParams):
        self.updateAttachments()
        if self._application.selectedPage is not None:
            if params.renamed_item:
                self._selectFile(params.renamed_item)

            if not self._application.testMode:
                self._beginRenaming()

    def SetFocus(self):
        self.__attachList.SetFocus()

        if (self.__attachList.GetItemCount() != 0 and
                self.__attachList.GetFocusedItem() == -1):
            self.__attachList.Focus(0)
            self.__attachList.Select(0)

    def selectAllAttachments(self):
        for index in range(self.__attachList.GetItemCount()):
            if self.__attachList.GetItemText(index) != self.GO_TO_PARENT_ITEM_NAME:
                self.__attachList.SetItemState(index,
                                               wx.LIST_STATE_SELECTED,
                                               wx.LIST_STATE_SELECTED)

    def _beginRenaming(self):
        selectedItem = self.__attachList.GetFirstSelected()
        if selectedItem == -1:
            return

        if self.__attachList.GetItemText(selectedItem) == self.GO_TO_PARENT_ITEM_NAME:
            return

        self.__attachList.EditLabel(selectedItem)

    def _onBeginLabelEdit(self, event):
        if event.GetText() == self.GO_TO_PARENT_ITEM_NAME:
            event.Veto()
            return

        self._oldEditedAttachName = os.path.join(
            self._application.selectedPage.currentAttachSubdir,
            event.GetItem().GetText())
        self._oldEditedAttachItemIndex = event.GetIndex()

        self._disableHotkeys()

    def _onEndLabelEdit(self, event):
        self._enableHotkeys()
        event.Veto()

        if (event.IsEditCancelled()
                or self._oldEditedAttachName is None
                or self._oldEditedAttachItemIndex != event.GetIndex()):
            self._oldEditedAttachName = None
            self._oldEditedAttachItemIndex = None
            return

        # New attachment name
        newName = os.path.join(self._application.selectedPage.currentAttachSubdir,
                               event.GetLabel().strip())

        logger.debug('Renaming attachment: %s -> %s',
                     self._oldEditedAttachName, newName)

        if newName == self._oldEditedAttachName:
            self._oldEditedAttachName = None
            self._oldEditedAttachItemIndex = None
            return

        rename = renameAttach(self._application.mainWindow,
                              self._application.wikiroot.selectedPage,
                              self._oldEditedAttachName, newName)
        self._oldEditedAttachName = None
        if rename:
            self._selectFile(event.GetLabel().strip())

    def _onPreferencesDialogClose(self, dialog):
        self.updateAttachments()

    def _onAttachSelected(self, event):
        text = ''
        page = self._application.selectedPage
        if page is not None:
            files = self.getSelectedFiles()
            attach = Attachment(page)
            root = attach.getAttachPath()
            full_path = [os.path.join(root, fname)
                         for fname in files
                         if os.path.isfile(os.path.join(root, fname))]
            if len(full_path) == 1:
                text = self._getStatusTextForSingleFile(full_path[0], root)
            elif len(full_path) > 0:
                text = self._getStatusTextForManyFiles(full_path)

        setStatusText(self._ATTACH_STATUS_ITEM, text)
        self._sendAttachSelectedEvent()

    def _getStatusTextForSingleFile(self, fname_full: str, root_path: str) -> str:
        tpl = _('{name}   -   {size} KB   -   {date}')
        name = os.path.relpath(fname_full, root_path)
        size = ('{:,.2f}'.format(os.path.getsize(fname_full) / 1024)).replace(',', ' ')
        datetime_format = self._general_config.dateTimeFormat.value
        date = datetime.fromtimestamp(os.path.getmtime(fname_full)).strftime(datetime_format)

        return tpl.format(name=name, size=size, date=date)

    def _getStatusTextForManyFiles(self, fname_full) -> str:
        tpl = _('{count} file(s)  -  {size} KB')
        count = len(fname_full)
        size = 0.0
        for fname in fname_full:
            size += os.path.getsize(fname)

        size /= 1024
        size_str = ('{:,.2f}'.format(size)).replace(',', ' ')
        return tpl.format(count=count, size=size_str)

    def _sendAttachSelectedEvent(self):
        page = self._application.selectedPage
        if page is not None:
            files = self.getSelectedFiles()
            params = AttachSelectionChangedParams(files)
            self._application.onAttachSelectionChanged(page, params)


class DropAttachFilesTarget(BaseDropFilesTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и панелью с прикрепленными файлами.
    """

    def OnDropFiles(self, x: int, y: int, files: List[str]) -> bool:
        correctedFiles = self.correctFileNames(files)

        if (self._application.wikiroot is not None and
                self._application.wikiroot.selectedPage is not None):
            attachFiles(self._application.mainWindow,
                        self._application.wikiroot.selectedPage,
                        correctedFiles,
                        self._application.wikiroot.selectedPage.currentAttachSubdir)
            return True

        return False
