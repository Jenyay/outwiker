# -*- coding: utf-8 -*-

import os.path
from typing import List

import wx

from outwiker.actions.attachfiles import AttachFilesActionForAttachPanel
from outwiker.actions.attachopenfolder import OpenAttachFolderAction
from outwiker.actions.attachpastelink import AttachPasteLinkActionForAttachPanel
from outwiker.actions.attachremove import RemoveAttachesActionForAttachPanel
from outwiker.core.attachment import Attachment
from outwiker.core.commands import MessageBox, attachFiles, showError
from outwiker.core.system import getBuiltinImagePath, getOS
from outwiker.gui.hotkey import HotKey

from .dropfiles import BaseDropFilesTarget
from .guiconfig import AttachConfig


class AttachPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self.ATTACH_ACTIONS_AREA = 'attach_panel'
        self.ID_EXECUTE = None
        self.ID_OPEN_FOLDER = None

        # List of tuples: (action, hotkey, hidden)
        self._actions = [
            (RemoveAttachesActionForAttachPanel,
                HotKey("Delete"),
                self.ATTACH_ACTIONS_AREA,
                True),
            (AttachFilesActionForAttachPanel,
                None,
                self.ATTACH_ACTIONS_AREA,
                True),
            (AttachPasteLinkActionForAttachPanel,
                HotKey("Enter", ctrl=True),
                self.ATTACH_ACTIONS_AREA,
                True)
        ]

        self.__registerActions()

        self.__toolbar = self.__createToolBar(self)
        self.__attachList = wx.ListCtrl(self,
                                        wx.ID_ANY,
                                        style=wx.LC_LIST | wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.__fileIcons = getOS().fileIcons
        self.__attachList.SetImageList(self.__fileIcons.imageList,
                                       wx.IMAGE_LIST_SMALL)
        self._dropTarget = DropAttachFilesTarget(self._application, self)

        self.__bindGuiEvents()
        self.__bindAppEvents()

    def __registerActions(self):
        actionController = self._application.actionController

        for action, hotkey, area, hidden in self._actions:
            actionController.register(
                action(self._application),
                hotkey=hotkey,
                area=area,
                hidden=hidden
            )

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.__attachList.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.__attachList.SetForegroundColour(colour)

    def __bindGuiEvents(self):
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,
                  self.__onBeginDrag, self.__attachList)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__onDoubleClick,
                  self.__attachList)

        self.Bind(wx.EVT_MENU, self.__onExecute, id=self.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.__onOpenFolder, id=self.ID_OPEN_FOLDER)
        self.Bind(wx.EVT_CLOSE, self.__onClose)

    def __unbindGuiEvents(self):
        self.Unbind(wx.EVT_LIST_BEGIN_DRAG,
                    handler=self.__onBeginDrag,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_ITEM_ACTIVATED,
                    handler=self.__onDoubleClick,
                    source=self.__attachList)

        self.Unbind(wx.EVT_MENU, handler=self.__onExecute, id=self.ID_EXECUTE)

        self.Unbind(wx.EVT_MENU, handler=self.__onOpenFolder,
                    id=self.ID_OPEN_FOLDER)

        self.Unbind(wx.EVT_CLOSE, handler=self.__onClose)

    @property
    def attachList(self):
        return self.__attachList

    @property
    def toolBar(self):
        return self.__toolbar

    def __bindAppEvents(self):
        self._application.onPageSelect += self.__onPageSelect
        self._application.onAttachListChanged += self.__onAttachListChanged
        self._application.onWikiOpen += self.__onWikiOpen

    def __unbindAppEvents(self):
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onAttachListChanged -= self.__onAttachListChanged
        self._application.onWikiOpen -= self.__onWikiOpen

    def __onClose(self, _event):
        actionController = self._application.actionController

        for action, hotkey, hidden in self._actions:
            actionController.removeHotkey(action.stringId)
            actionController.removeToolbarButton(action.stringId)

        self._dropTarget.destroy()
        self.__unbindAppEvents()
        self.__unbindGuiEvents()
        self.toolBar.ClearTools()
        self.attachList.ClearAll()
        self.__fileIcons.clear()
        self.Destroy()

    def __createToolBar(self, parent):
        toolbar = wx.ToolBar(parent, wx.ID_ANY, style=wx.TB_DOCKABLE)
        actionController = self._application.actionController

        actionController.appendToolbarButton(
            AttachFilesActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("attach.png")
        )

        actionController.appendToolbarButton(
            RemoveAttachesActionForAttachPanel.stringId,
            toolbar,
            getBuiltinImagePath("delete.png")
        )

        actionController.appendHotkey(
            RemoveAttachesActionForAttachPanel.stringId,
            self)

        toolbar.AddSeparator()

        actionController.appendToolbarButton(
                AttachPasteLinkActionForAttachPanel.stringId,
                toolbar,
                getBuiltinImagePath("paste.png")
                )

        actionController.appendHotkey(
                AttachPasteLinkActionForAttachPanel.stringId,
                self)

        self.ID_EXECUTE = toolbar.AddTool(
            wx.ID_ANY,
            _("Execute"),
            wx.Bitmap(getBuiltinImagePath("execute.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _("Execute"),
            ""
        ).GetId()

        self.ID_OPEN_FOLDER = toolbar.AddTool(
            wx.ID_ANY,
            _("Open Attachments Folder"),
            wx.Bitmap(getBuiltinImagePath("folder.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _("Open Attachments Folder"),
            ""
        ).GetId()

        toolbar.Realize()
        return toolbar

    def __set_properties(self):
        self.__attachList.SetMinSize((-1, 100))

    def __do_layout(self):
        attachSizer_copy = wx.FlexGridSizer(2, 1, 0, 0)
        attachSizer_copy.Add(self.__toolbar, 1, wx.EXPAND, 0)
        attachSizer_copy.Add(self.__attachList, 1, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(attachSizer_copy)
        attachSizer_copy.Fit(self)
        attachSizer_copy.AddGrowableRow(1)
        attachSizer_copy.AddGrowableCol(0)

        attachSizer_copy.Fit(self)
        self.SetAutoLayout(True)

    def __onWikiOpen(self, _wiki):
        self.updateAttachments()

    def __onPageSelect(self, _page):
        self.updateAttachments()

    def __sortFilesList(self, files_list):
        result = sorted(files_list, key=str.lower, reverse=True)
        result.sort(key=Attachment.sortByType)
        return result

    def updateAttachments(self):
        """
        Обновить список прикрепленных файлов
        """
        self.__attachList.Freeze()
        self.__attachList.ClearAll()
        if self._application.selectedPage is not None:
            files = Attachment(self._application.selectedPage).attachmentFull
            files = self.__sortFilesList(files)

            for fname in files:
                if (not os.path.basename(fname).startswith("__") or
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

        self.__attachList.Thaw()

    def getSelectedFiles(self):
        files = []

        item = self.__attachList.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)

        while item != -1:
            fname = self.__attachList.GetItemText(item)
            files.append(fname)

            item = self.__attachList.GetNextItem(item,
                                                 state=wx.LIST_STATE_SELECTED)

        return files

    def __onRemove(self, _event):
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

                self.updateAttachments()

    def __pasteLink(self):
        """
        Сгенерировать сообщение о том, что пользователь хочет вставить
        ссылку на приаттаченные файлы
        """
        files = self.getSelectedFiles()
        if len(files) == 0:
            showError(self._application.mainWindow,
                    _("You did not select a file to paste"))
            return

        self._application.onAttachmentPaste(files)

    def __executeFile(self):
        if self._application.selectedPage is not None:
            files = self.getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _("You did not select a file to execute"))
                return

            for file in files:
                fullpath = os.path.join(Attachment(
                    self._application.selectedPage).getAttachPath(), file)
                try:
                    getOS().startFile(fullpath)
                except OSError:
                    text = _("Can't execute file '%s'") % file
                    showError(self._application.mainWindow, text)

    def __onPaste(self, _event):
        self.__pasteLink()

    def __onOpenFolder(self, _event):
        self._application.actionController.getAction(
            OpenAttachFolderAction.stringId).run(None)

    def __onExecute(self, _event):
        self.__executeFile()

    def __onDoubleClick(self, _event):
        config = AttachConfig(self._application.config)
        if config.doubleClickAction.value == AttachConfig.ACTION_INSERT_LINK:
            self.__pasteLink()
        elif config.doubleClickAction.value == AttachConfig.ACTION_OPEN:
            self.__executeFile()

    def __onBeginDrag(self, _event):
        selectedFiles = self.getSelectedFiles()
        if not selectedFiles:
            return

        data = wx.FileDataObject()
        attach_path = Attachment(
            self._application.selectedPage).getAttachPath()

        for fname in self.getSelectedFiles():
            data.AddFile(os.path.join(attach_path, fname))

        dragSource = wx.DropSource(data, self)
        dragSource.DoDragDrop()

    def __onAttachListChanged(self, page, _params):
        if page is not None and page == self._application.selectedPage:
            self.updateAttachments()

    def SetFocus(self):
        self.__attachList.SetFocus()

        if (self.__attachList.GetItemCount() != 0 and
                self.__attachList.GetFocusedItem() == -1):
            self.__attachList.Focus(0)
            self.__attachList.Select(0)


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
                        correctedFiles)
            return True

        return False
