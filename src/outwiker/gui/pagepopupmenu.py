# -*- coding: utf-8 -*-

import wx

import outwiker.gui.pagedialog
import outwiker.core.commands
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.addsiblingpage import AddSiblingPageAction
from outwiker.actions.removepage import RemovePageAction
from outwiker.actions.renamepage import RenamePageAction
from outwiker.actions.editpageprop import EditPagePropertiesAction
from outwiker.actions.openattachfolder import OpenAttachFolderAction
from outwiker.gui.pagedialog import createSiblingPage, createChildPage


class PagePopupMenu (object):
    def __init__(self, parent, popupPage, application):
        self.ID_ADD_CHILD = None
        self.ID_ADD_SIBLING = None
        self.ID_RENAME = None
        self.ID_REMOVE = None
        self.ID_PROPERTIES_POPUP = None

        self.ID_COPY_PATH = None
        self.ID_COPY_ATTACH_PATH = None
        self.ID_COPY_TITLE = None
        self.ID_COPY_LINK = None
        self.ID_OPEN_ATTACH_FOLDER = None

        self.parent = parent
        self._application = application

        # Страница, над элементом которой вызывается контекстное меню
        self.popupPage = popupPage
        self.menu = self.__createPopupMenu(self.popupPage)

        self._application.onTreePopupMenu(self.menu, popupPage)

    def __bindPopupMenuEvents(self, popupMenu):
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onAddChild,
                       id=self.ID_ADD_CHILD)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onAddSibling,
                       id=self.ID_ADD_SIBLING)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onRemove,
                       id=self.ID_REMOVE)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onRename,
                       id=self.ID_RENAME)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onCopyTitle,
                       id=self.ID_COPY_TITLE)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onCopyPath,
                       id=self.ID_COPY_PATH)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onCopyAttachPath,
                       id=self.ID_COPY_ATTACH_PATH)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onCopyLink,
                       id=self.ID_COPY_LINK)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onOpenAttachFolder,
                       id=self.ID_OPEN_ATTACH_FOLDER)
        popupMenu.Bind(wx.EVT_MENU,
                       self.__onPropertiesPopup,
                       id=self.ID_PROPERTIES_POPUP)

    def __onAddChild(self, event):
        assert self.popupPage is not None
        createChildPage(self.parent, self.popupPage)

    def __onAddSibling(self, event):
        assert self.popupPage is not None
        createSiblingPage(self.parent, self.popupPage)

    def __onPropertiesPopup(self, event):
        assert self.popupPage is not None
        if self.popupPage.parent is not None:
            outwiker.gui.pagedialog.editPage(self.parent, self.popupPage)

    def __createPopupMenu(self, popupPage):
        self.popupPage = popupPage
        actionController = self._application.actionController

        popupMenu = wx.Menu()

        self.ID_ADD_CHILD = popupMenu.Append(wx.ID_ANY, actionController.getTitle(AddChildPageAction.stringId)).GetId()
        self.ID_ADD_SIBLING = popupMenu.Append(wx.ID_ANY, actionController.getTitle(AddSiblingPageAction.stringId)).GetId()
        self.ID_REMOVE = popupMenu.Append(wx.ID_ANY, actionController.getTitle(RemovePageAction.stringId)).GetId()
        self.ID_RENAME = popupMenu.Append(wx.ID_ANY, actionController.getTitle(RenamePageAction.stringId)).GetId()

        popupMenu.AppendSeparator()

        self.ID_COPY_TITLE = popupMenu.Append(wx.ID_ANY, _(u"Copy Page Title")).GetId()
        self.ID_COPY_PATH = popupMenu.Append(wx.ID_ANY, _(u"Copy Page Path")).GetId()
        self.ID_COPY_ATTACH_PATH = popupMenu.Append(wx.ID_ANY, _(u"Copy Attachments Path")).GetId()
        self.ID_COPY_LINK = popupMenu.Append(wx.ID_ANY, _(u"Copy Page Link")).GetId()
        self.ID_OPEN_ATTACH_FOLDER = popupMenu.Append(wx.ID_ANY, _(u"Open Attachments Folder")).GetId()

        popupMenu.AppendSeparator()

        self.ID_PROPERTIES_POPUP = popupMenu.Append(wx.ID_ANY, actionController.getTitle(EditPagePropertiesAction.stringId)).GetId()

        self.__bindPopupMenuEvents(popupMenu)

        return popupMenu

    def __onRemove(self, event):
        """
        Удалить страницу
        """
        assert self.popupPage is not None
        if self.popupPage is not None:
            outwiker.core.commands.removePage(self.popupPage)

    def __onRename(self, event):
        """
        Переименовать страницу
        """
        assert self.popupPage is not None
        self._application.mainWindow.treePanel.beginRename(self.popupPage)

    def __onCopyLink(self, event):
        """
        Копировать ссылку на страницу в буфер обмена
        """
        assert self.popupPage is not None
        outwiker.core.commands.copyLinkToClipboard(self.popupPage)

    def __onOpenAttachFolder(self, event):
        assert self.popupPage is not None
        self._application.actionController.getAction(
            OpenAttachFolderAction.stringId).run(None)

    def __onCopyTitle(self, event):
        """
        Копировать заголовок страницы в буфер обмена
        """
        assert self.popupPage is not None
        outwiker.core.commands.copyTitleToClipboard(self.popupPage)

    def __onCopyPath(self, event):
        """
        Копировать путь до страницы в буфер обмена
        """
        assert self.popupPage is not None
        outwiker.core.commands.copyPathToClipboard(self.popupPage)

    def __onCopyAttachPath(self, event):
        """
        Копировать путь до прикрепленных файлов в буфер обмена
        """
        assert self.popupPage is not None
        outwiker.core.commands.copyAttachPathToClipboard(self.popupPage)
