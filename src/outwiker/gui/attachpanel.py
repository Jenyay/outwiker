#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.application import Application
from outwiker.core.commands import MessageBox
from outwiker.core.system import getOS, getImagesDir
from outwiker.core.attachment import Attachment
from outwiker.actions.attachfiles import AttachFilesAction
from outwiker.core.events import PAGE_UPDATE_ATTACHMENT


class AttachPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        self.ID_ATTACH = wx.NewId()
        self.ID_REMOVE = wx.NewId()
        self.ID_PASTE = wx.NewId()
        self.ID_EXECUTE = wx.NewId()
        self.ID_REFRESH = wx.NewId()

        wx.Panel.__init__(self, *args, **kwds)
        self.__toolbar = self.__createToolBar(self, -1)
        self.__attachList = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.__fileIcons = getOS().fileIcons
        self.__attachList.SetImageList (self.__fileIcons.imageList, wx.IMAGE_LIST_SMALL)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.__onBeginDrag, self.__attachList)

        self.Bind(wx.EVT_MENU, self.__onAttach, id=self.ID_ATTACH)
        self.Bind(wx.EVT_MENU, self.__onRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_MENU, self.__onPaste, id=self.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.__onExecute, id=self.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.__onRefresh, id=self.ID_REFRESH)
        self.Bind (wx.EVT_CLOSE, self.__onClose)

        self.__bindAppEvents()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__onPaste, self.__attachList)


    @property
    def attachList (self):
        return self.__attachList


    @property
    def toolBar (self):
        return self.__toolbar


    def __bindAppEvents (self):
        Application.onPageSelect += self.__onPageSelect
        Application.onPageUpdate += self.__onPageUpdate
        Application.onWikiOpen += self.__onWikiOpen

    
    def __unbindAppEvents (self):
        Application.onPageSelect -= self.__onPageSelect
        Application.onPageUpdate -= self.__onPageUpdate
        Application.onWikiOpen -= self.__onWikiOpen


    def __onClose (self, event):
        self.__unbindAppEvents()
        self.toolBar.ClearTools()
        self.attachList.ClearAll()
        self.__fileIcons.clear()
        self.Destroy()


    def __createToolBar (self, parent, id):
        imagesDir = getImagesDir()

        toolbar = wx.ToolBar (parent, id, style=wx.TB_DOCKABLE)

        toolbar.AddLabelTool(self.ID_ATTACH, 
                _(u"Attach Files…"), 
                wx.Bitmap(os.path.join (imagesDir, "attach.png"),
                    wx.BITMAP_TYPE_ANY),
                wx.NullBitmap, 
                wx.ITEM_NORMAL,
                _(u"Attach Files…"), 
                "")

        toolbar.AddLabelTool(self.ID_REMOVE, 
                _(u"Remove Files…"), 
                wx.Bitmap(os.path.join (imagesDir, "delete.png"),
                    wx.BITMAP_TYPE_ANY),
                wx.NullBitmap, 
                wx.ITEM_NORMAL,
                _(u"Remove Files…"), 
                "")

        toolbar.AddSeparator()

        toolbar.AddLabelTool(self.ID_PASTE, 
                _(u"Paste"), 
                wx.Bitmap(os.path.join (imagesDir, "paste.png"),
                    wx.BITMAP_TYPE_ANY),
                wx.NullBitmap, 
                wx.ITEM_NORMAL,
                _(u"Paste"), 
                "")

        toolbar.AddLabelTool(self.ID_EXECUTE, 
                _(u"Execute"), 
                wx.Bitmap(os.path.join (imagesDir, "execute.png"),
                    wx.BITMAP_TYPE_ANY),
                wx.NullBitmap, 
                wx.ITEM_NORMAL,
                _(u"Execute"), 
                "")


        toolbar.AddLabelTool(self.ID_REFRESH, 
                _(u"Refresh"), 
                wx.Bitmap(os.path.join (imagesDir, "reload.png"),
                    wx.BITMAP_TYPE_ANY),
                wx.NullBitmap, 
                wx.ITEM_NORMAL,
                _(u"Refresh"), 
                "")

        toolbar.Realize()
        return toolbar


    def __set_properties(self):
        self.__attachList.SetMinSize((-1, 100))

    def __do_layout(self):
        attachSizer_copy = wx.FlexGridSizer(2, 1, 0, 0)
        attachSizer_copy.Add(self.__toolbar, 1, wx.EXPAND, 0)
        attachSizer_copy.Add(self.__attachList, 1, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(attachSizer_copy)
        attachSizer_copy.Fit(self)
        attachSizer_copy.AddGrowableRow(1)
        attachSizer_copy.AddGrowableCol(0)

        attachSizer_copy.Fit(self)
        self.SetAutoLayout(True)


    def __onWikiOpen (self, wiki):
        self.updateAttachments()


    def __onPageSelect (self, page):
        self.updateAttachments ()


    def __onPageUpdate (self, page, **kwargs):
        if (Application.selectedPage != None and 
                Application.selectedPage == page and
                kwargs['change'] == PAGE_UPDATE_ATTACHMENT):
            self.updateAttachments ()


    def updateAttachments (self):
        """
        Обновить список прикрепленных файлов
        """
        self.__attachList.Freeze()
        self.__attachList.ClearAll()
        if Application.selectedPage != None:
            files = Attachment (Application.selectedPage).attachmentFull
            files.sort(Attachment.sortByName, reverse=True)

            for fname in files:
                if not os.path.basename(fname).startswith("__") or not os.path.isdir (fname):
                    # Отключим уведомления об ошибках во всплывающих окнах
                    # иначе они появляются при попытке прочитать испорченные иконки
                    # На результат работы это не сказывается, все-равно бракованные
                    # иконки отлавливаются.
                    wx.Log_EnableLogging(False)

                    imageIndex = self.__fileIcons.getFileImage (fname)

                    # Вернем всплывающие окна с ошибками
                    wx.Log_EnableLogging(True)

                    self.__attachList.InsertImageStringItem (0, os.path.basename (fname), imageIndex)

        self.__attachList.Thaw()


    def __getSelectedFiles (self):
        files = []

        item = self.__attachList.GetNextItem (-1, state = wx.LIST_STATE_SELECTED)

        while item != -1:
            fname = self.__attachList.GetItemText (item)
            files.append (fname)

            item = self.__attachList.GetNextItem (item, state = wx.LIST_STATE_SELECTED)

        return files


    def __onAttach(self, event):
        Application.actionController.getAction (AttachFilesAction.stringId).run (None)


    def __onRemove(self, event):
        if Application.selectedPage != None:
            files = self.__getSelectedFiles ()

            if len (files) == 0:
                MessageBox (_(u"You did not select a file to remove"), 
                    _(u"Error"),
                    wx.OK  | wx.ICON_ERROR)
                return

            if MessageBox (_(u"Remove selected files?"), 
                    _(u"Remove files?"),
                    wx.YES_NO  | wx.ICON_QUESTION) == wx.YES:
                try:
                    Attachment (Application.selectedPage).removeAttach (files)
                except IOError as e:
                    MessageBox (unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

                self.updateAttachments ()


    def __onPaste(self, event):
        """
        Сгенерировать сообщение о том, что пользователь хочет вставить ссылку на приаттаченные файлы
        """
        files = self.__getSelectedFiles ()
        if len (files) == 0:
            MessageBox (_(u"You did not select a file to paste"), 
                _(u"Error"),
                wx.OK  | wx.ICON_ERROR)
            return

        Application.onAttachmentPaste (files)


    def __onRefresh (self, event):
        self.updateAttachments()


    def __onExecute(self, event):
        if Application.selectedPage != None:
            files = self.__getSelectedFiles()

            if len (files) == 0:
                MessageBox (_(u"You did not select a file to execute"), 
                    _(u"Error"),
                    wx.OK  | wx.ICON_ERROR)
                return

            for file in files:
                fullpath = os.path.join (Attachment (Application.selectedPage).getAttachPath(), file)
                try:
                    getOS().startFile (fullpath)
                except OSError:
                    text = _(u"Can't execute file '%s'") % file
                    MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __onBeginDrag(self, event):
        data = getOS().dragFileDataObject()

        for fname in self.__getSelectedFiles():
            data.AddFile (os.path.join (Attachment (Application.selectedPage).getAttachPath(), fname) )

        dragSource = wx.DropSource (self)
        dragSource.SetData(data)

        result = dragSource.DoDragDrop ()


