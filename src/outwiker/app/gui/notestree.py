# -*- coding: utf-8 -*-

import os
import os.path
from typing import List, Optional, Tuple

import wx

from outwiker.app.actions.addsiblingpage import AddSiblingPageAction
from outwiker.app.actions.editpageprop import EditPagePropertiesAction
from outwiker.app.actions.movepagedown import MovePageDownAction
from outwiker.app.actions.movepageup import MovePageUpAction
from outwiker.app.actions.moving import GoToParentAction
from outwiker.app.actions.removepage import RemovePageAction

from outwiker.app.services.attachment import attachFiles
from outwiker.app.services.messages import showError
from outwiker.app.services.tree import renamePage, movePage

from outwiker.app.actions.addchildpage import AddChildPageAction

from outwiker.app.gui.dropfiles import BaseDropFilesTarget
from outwiker.app.gui.pagedialog import editPage
from outwiker.app.gui.pagepopupmenu import PagePopupMenu

from outwiker.core.events import (
    PAGE_UPDATE_ICON,
    PAGE_UPDATE_TITLE,
    PAGE_UPDATE_COLOR,
    BookmarksChangedParams,
    NotesTreeItemsPreparingParams,
)
from outwiker.core.system import getBuiltinImagePath, getExtraIconPath
from outwiker.core.tree import BasePage, WikiPage

from outwiker.gui.guiconfig import TreeConfig
from outwiker.gui.controls.notestreectrl2 import (
    NotesTreeCtrl2,
    EVT_NOTES_TREE_SEL_CHANGED,
    EVT_NOTES_TREE_EXPAND_CHANGED,
    EVT_NOTES_TREE_RIGHT_BUTTON_UP,
    EVT_NOTES_TREE_MIDDLE_BUTTON_UP,
    EVT_NOTES_TREE_ITEM_ACTIVATE,
    EVT_NOTES_TREE_END_ITEM_EDIT,
    EVT_NOTES_TREE_DROP_ITEM,
    EVT_NOTES_TREE_CHANGE_ORDER_ITEM,
    EVT_NOTES_TREE_ITEMS_PREPARING,
    EVT_NOTES_TREE_SCALE,
    NotesTreeItem,
)
from outwiker.gui.dialogs.messagebox import MessageBox


class NotesTree(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent, style=wx.TAB_TRAVERSAL)
        self._application = application
        # Переключатель устанавливается в True,
        # если "внезапно" изменяется текущая страница
        self._externalPageSelect = False
        self._treeConfig = TreeConfig(application.config)

        self.toolbar = wx.ToolBar(
            parent=self, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_DOCKABLE
        )

        # Extra icons for notes tree
        self._EXTRA_ICON_BOOKMARK = 0
        self._EXTRA_ICON_BOOKMARK_TITLE = "bookmark"

        self._EXTRA_ICON_READONLY = 1
        self._EXTRA_ICON_READONLY_TITLE = "readonly"

        # (title, iconId)
        self._pagesExtraIcons: List[Tuple[str, str]] = []

        self.treeCtrl = NotesTreeCtrl2(self)
        self._initTreeCtrl()

        self.SetSize((256, 260))
        self._do_layout()

        self.popupPage = None
        self.popupMenu = None

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = "Expand"

        self._bindApplicationEvents()
        self._bindGuiEvents()
        self._dropTarget = NotesTreeDropFilesTarget(
            self._application, self.treeCtrl, self
        )

    def _initTreeCtrl(self):
        self.treeCtrl.setFontSize(self._treeConfig.fontSize.value)
        self._pagesExtraIcons.append(
            (
                self._EXTRA_ICON_BOOKMARK_TITLE,
                getExtraIconPath("bookmark.svg"),
            )
        )
        self._pagesExtraIcons.append(
            (
                self._EXTRA_ICON_READONLY_TITLE,
                getExtraIconPath("lock.svg"),
            )
        )

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.treeCtrl.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.treeCtrl.SetForegroundColour(colour)

    def getPageByItemId(self, item_id: wx.TreeItemId) -> "outwiker.core.tree.WikiPage":
        return self.treeCtrl.GetItemData(item_id)

    def _bindApplicationEvents(self):
        """
        Подписка на события контроллера
        """
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onTreeUpdate += self.__onTreeUpdate
        self._application.onPageCreate += self.__onPageCreate
        self._application.onPageOrderChange += self.__onPageOrderChange
        self._application.onPageSelect += self.__onPageSelect
        self._application.onPageUpdate += self.__onPageUpdate
        self._application.onStartTreeUpdate += self.__onStartTreeUpdate
        self._application.onEndTreeUpdate += self.__onEndTreeUpdate
        self._application.onPreferencesDialogClose += self.__onPreferences
        self._application.onBookmarksChanged += self.__onBookmarkChanged
        self._application.onForceNotesTreeItemsUpdate += self.__onForceNotesTreeItemsUpdate

    def __UnBindApplicationEvents(self):
        """
        Отписка от событий контроллера
        """
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onTreeUpdate -= self.__onTreeUpdate
        self._application.onPageCreate -= self.__onPageCreate
        self._application.onPageOrderChange -= self.__onPageOrderChange
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onPageUpdate -= self.__onPageUpdate
        self._application.onStartTreeUpdate -= self.__onStartTreeUpdate
        self._application.onEndTreeUpdate -= self.__onEndTreeUpdate
        self._application.onPreferencesDialogClose -= self.__onPreferences
        self._application.onBookmarksChanged -= self.__onBookmarkChanged
        self._application.onForceNotesTreeItemsUpdate -= self.__onForceNotesTreeItemsUpdate

    def __bindUpdateEvents(self):
        self._application.onTreeUpdate += self.__onTreeUpdate
        self._application.onPageCreate += self.__onPageCreate
        self._application.onPageSelect += self.__onPageSelect
        self._application.onPageOrderChange += self.__onPageOrderChange
        self._application.onForceNotesTreeItemsUpdate += self.__onForceNotesTreeItemsUpdate
        self.treeCtrl.Bind(EVT_NOTES_TREE_SEL_CHANGED, self.__onSelChanged)

    def __unbindUpdateEvents(self):
        self._application.onTreeUpdate -= self.__onTreeUpdate
        self._application.onPageCreate -= self.__onPageCreate
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onPageOrderChange -= self.__onPageOrderChange
        self._application.onForceNotesTreeItemsUpdate -= self.__onForceNotesTreeItemsUpdate
        self.treeCtrl.Unbind(EVT_NOTES_TREE_SEL_CHANGED, handler=self.__onSelChanged)

    def __onForceNotesTreeItemsUpdate(self, page, params):
        for forced_page in params.pages:
            self.treeCtrl.updateItem(forced_page)

    def __onPreferences(self, dialog):
        self.treeCtrl.setFontSize(self._treeConfig.fontSize.value)

    def __onWikiOpen(self, root):
        self._setRoot(root)

    def __onPageUpdate(self, page, **kwargs):
        change = kwargs["change"]
        if (
            (change & PAGE_UPDATE_ICON)
            or (change & PAGE_UPDATE_TITLE)
            or (change & PAGE_UPDATE_COLOR)
        ):
            self.treeCtrl.updateItem(page)

    def _bindGuiEvents(self):
        """
        Подписка на события интерфейса
        """
        self.treeCtrl.Bind(EVT_NOTES_TREE_END_ITEM_EDIT, handler=self.__onEndLabelEdit)
        self.treeCtrl.Bind(EVT_NOTES_TREE_SEL_CHANGED, handler=self.__onSelChanged)
        self.treeCtrl.Bind(EVT_NOTES_TREE_RIGHT_BUTTON_UP, handler=self.__onPopupMenu)
        self.treeCtrl.Bind(
            EVT_NOTES_TREE_MIDDLE_BUTTON_UP, handler=self.__onMiddleClick
        )
        self.treeCtrl.Bind(
            EVT_NOTES_TREE_EXPAND_CHANGED, handler=self.__onTreeExpandChanged
        )
        self.treeCtrl.Bind(
            EVT_NOTES_TREE_ITEM_ACTIVATE, handler=self.__onTreeItemActivated
        )
        self.treeCtrl.Bind(EVT_NOTES_TREE_DROP_ITEM, handler=self.__onTreeItemDrop)
        self.treeCtrl.Bind(
            EVT_NOTES_TREE_CHANGE_ORDER_ITEM, handler=self.__onTreeItemChangeOrder
        )
        self.treeCtrl.Bind(
            EVT_NOTES_TREE_ITEMS_PREPARING, handler=self.__onTreeItemsPreparing
        )
        self.treeCtrl.Bind(EVT_NOTES_TREE_SCALE, handler=self.__onTreeScale)

        self.Bind(wx.EVT_CLOSE, self.__onClose)

    def __onTreeScale(self, event):
        self._treeConfig.fontSize.value = event.fontSize

    def __onMiddleClick(self, event):
        self._application.mainWindow.tabsController.openInTab(event.page, True)

    def __onClose(self, _event):
        self._dropTarget.destroy()
        self.__UnBindApplicationEvents()
        self.treeCtrl.clear()
        self._removeButtons()
        self.toolbar.ClearTools()
        self.Destroy()

    def __onPageCreate(self, newpage):
        """
        Обработка создания страницы
        """
        self.treeCtrl.addPage(newpage, update=False)
        self.treeCtrl.expand(newpage, update=False)
        self.treeCtrl.expand(newpage.parent, update=True)

    def __onTreeItemActivated(self, event):
        editPage(self, event.page)

    def __onTreeExpandChanged(self, event):
        if self._application.wikiroot is None:
            return

        page = event.page
        expanded = event.expanded

        if not page.readonly:
            page_registry = page.root.registry.get_page_registry(page)
            page_registry.set(self.pageOptionExpand, expanded)

        if expanded:
            for child in page.children:
                self._appendChildren(child)

    def __onPopupMenu(self, event):
        self.popupPage = None
        popupPage = event.page
        self.popupMenu = PagePopupMenu(self, popupPage, self._application)
        self.PopupMenu(self.popupMenu.menu)

    def beginRename(self, page=None):
        """
        Начать переименование страницы в дереве. Если page is None,
        то начать переименование текущей страницы
        """
        pageToRename = page if page is not None else self._application.selectedPage

        if pageToRename is None or pageToRename.parent is None:
            mainWindow = self._application.mainWindow
            showError(mainWindow, _("You can't rename the root element"))
            return

        self.treeCtrl.editItem(pageToRename)

    def __onEndLabelEdit(self, event):
        renamePage(event.page, event.new_title)

    def __onStartTreeUpdate(self, _root):
        self.__unbindUpdateEvents()

    def __onEndTreeUpdate(self, _root):
        self.__bindUpdateEvents()
        self._setRoot(self._application.wikiroot)

    def __onTreeItemDrop(self, event):
        draggedPage = event.srcPage
        newParent = event.destPage
        if newParent != draggedPage:
            movePage(draggedPage, newParent)
            self.treeCtrl.expand(newParent, update=False)
            self.treeCtrl.setSelectedPage(self._application.selectedPage)

    def __onTreeItemChangeOrder(self, event):
        srcPage = event.srcPage
        beforePage = event.beforePage
        afterPage = event.afterPage
        assert beforePage is not None or afterPage is not None
        newParent = beforePage.parent if beforePage is not None else afterPage.parent
        newOrder = beforePage.order if beforePage is not None else afterPage.order + 1
        srcPage.moveTo(newParent)
        srcPage.order = newOrder

    def __onTreeUpdate(self, sender):
        self._setRoot(sender.root)

    def __onTreeItemsPreparing(self, event):
        items = event.items
        self._updateExtraIcons(items)

        page = self._application.selectedPage
        params = NotesTreeItemsPreparingParams(items)
        self._application.onNotesTreeItemsPreparing(page, params)

    def _updateExtraIcons(self, items: List[NotesTreeItem]):
        wikiroot = self._application.wikiroot
        if wikiroot is None:
            return

        enableBookmarkExtraIcons = self._treeConfig.extraIconBookmark.value
        enableReadOnlyExtraIcons = self._treeConfig.extraIconReadOnly.value

        for item in items:
            item.clearExtraIcons()
            if enableBookmarkExtraIcons and wikiroot.bookmarks.pageMarked(item.getPage()):
                item.addExtraIcon(*self._pagesExtraIcons[self._EXTRA_ICON_BOOKMARK])

            if enableReadOnlyExtraIcons and item.getPage().readonly:
                item.addExtraIcon(*self._pagesExtraIcons[self._EXTRA_ICON_READONLY])

    def __onPageSelect(self, page):
        """
        Изменение выбранной страницы
        """
        # Пометим, что изменение страницы произошло снаружи,
        # а не из-за клика по дереву
        self._externalPageSelect = True

        try:
            currpage = self.selectedPage
            if currpage != page:
                self.selectedPage = page
        finally:
            self._externalPageSelect = False

    def __onSelChanged(self, _event):
        ctrlstate = wx.GetKeyState(wx.WXK_CONTROL)
        shiftstate = wx.GetKeyState(wx.WXK_SHIFT)

        if (ctrlstate or shiftstate) and not self._externalPageSelect:
            self._application.mainWindow.tabsController.openInTab(
                self.selectedPage, True
            )
        else:
            self._application.selectedPage = self.selectedPage

    def __onPageOrderChange(self, sender):
        """
        Изменение порядка страниц
        """
        self.treeCtrl.updateTree()

    def __onBookmarkChanged(self, params: BookmarksChangedParams):
        self.treeCtrl.updateItem(params.page)

    @property
    def selectedPage(self):
        return self.treeCtrl.getSelectedPage()

    @selectedPage.setter
    def selectedPage(self, newSelPage):
        if newSelPage is not None:
            if not self.treeCtrl.pageInTree(newSelPage):
                self._addTreeItemsToPage(newSelPage)

            self.treeCtrl.expandToPage(newSelPage, update=False)
        self.treeCtrl.setSelectedPage(newSelPage)

    def _addTreeItemsToPage(self, page: WikiPage):
        current_page = page
        pages: List[WikiPage] = page.children[:]
        while current_page is not None and not self.treeCtrl.pageInTree(current_page):
            parent = current_page.parent
            if parent is not None:
                pages = parent.children + pages
            else:
                pages.insert(0, current_page)
            current_page = parent

        for page in pages:
            self.treeCtrl.addPage(page, update=False)

        self.treeCtrl.updateTree()

    def _do_layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(1)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(self.toolbar, 1, wx.EXPAND, 0)
        mainSizer.Add(self.treeCtrl, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        self.Layout()

    def addButtons(self):
        """
        Add the buttons to notes tree panel.
        """
        actionController = self._application.actionController

        actionController.appendToolbarButton(
            GoToParentAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-go-to-parent.svg"),
            False,
        )

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            AddSiblingPageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-insert-next.svg"),
            False,
        )

        actionController.appendToolbarButton(
            AddChildPageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-insert-child.svg"),
            False,
        )

        actionController.appendToolbarButton(
            RemovePageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-delete.svg"),
            False,
        )

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            MovePageDownAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-move-down.svg"),
            False,
        )

        actionController.appendToolbarButton(
            MovePageUpAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-move-up.svg"),
            False,
        )

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            EditPagePropertiesAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-properties.svg"),
            False,
        )

        self.toolbar.Realize()
        self.Layout()

    def _removeButtons(self):
        actionController = self._application.actionController

        actions = [
            GoToParentAction,
            MovePageDownAction,
            MovePageUpAction,
            AddSiblingPageAction,
            AddChildPageAction,
            RemovePageAction,
            EditPagePropertiesAction,
        ]
        for action in actions:
            actionController.removeToolbarButton(action.stringId)

    def expand(self, page):
        self.treeCtrl.expand(page)

    def _setRoot(self, rootPage: Optional[BasePage]):
        """
        Обновить дерево
        """
        self.treeCtrl.clear(update=False)

        if rootPage is not None:
            self.treeCtrl.addRoot(rootPage, update=False)
            self._appendChildren(rootPage)
            self.treeCtrl.setSelectedPage(self._application.selectedPage)
        else:
            self.treeCtrl.updateTree()

    def _appendChildren(self, parentPage: BasePage):
        """
        Добавить детей в дерево
        parentPage - родительская страница, куда добавляем дочерние страницы
        """
        grandParentExpanded = self.treeCtrl.isExpanded(parentPage.parent)

        if grandParentExpanded:
            for child in parentPage.children:
                self.treeCtrl.addPage(child, update=False)
                self._appendChildren(child)


class NotesTreeDropFilesTarget(BaseDropFilesTarget):
    """
    Class to drop files to notes in the notes tree panel.
    """

    def __init__(self, application, targetWindow: NotesTreeCtrl2, notesTree: NotesTree):
        super().__init__(application, targetWindow)
        self._notesTree = notesTree

    def OnDropFiles(self, x, y, files):
        correctedFiles = self.correctFileNames(files)
        page = self.targetWindow.HitTest((x, y))
        if page is not None:
            file_names = [os.path.basename(fname) for fname in correctedFiles]

            text = _("Attach files to the note '{title}'?\n\n{files}").format(
                title=page.display_title, files="\n".join(file_names)
            )

            if (
                MessageBox(
                    text,
                    _("Attach files to the note?"),
                    wx.YES_NO | wx.ICON_QUESTION,
                )
                == wx.YES
            ):
                attachFiles(self._application.mainWindow, page, correctedFiles)
            return True
        return False
