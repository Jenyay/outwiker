# -*- coding: utf-8 -*-

import os
import os.path
from typing import Optional

import wx

from outwiker.actions.addsiblingpage import AddSiblingPageAction
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction
from outwiker.actions.removepage import RemovePageAction
from outwiker.actions.editpageprop import EditPagePropertiesAction
from outwiker.actions.moving import GoToParentAction

from outwiker.api.services.attachment import attachFiles
from outwiker.api.services.messages import showError

from outwiker.app.gui.pagedialog import editPage
from outwiker.app.gui.pagepopupmenu import PagePopupMenu

from outwiker.core.commands import MessageBox, renamePage, movePage
from outwiker.core.events import PAGE_UPDATE_ICON, PAGE_UPDATE_TITLE
from outwiker.core.system import getBuiltinImagePath

from outwiker.gui.controls.notestreectrl import NotesTreeCtrl
from outwiker.gui.dropfiles import BaseDropFilesTarget


class NotesTree(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent, style=wx.TAB_TRAVERSAL)
        self._application = application
        # Переключатель устанавливается в True,
        # если "внезапно" изменяется текущая страница
        self._externalPageSelect = False

        self.toolbar = wx.ToolBar(
            parent=self,
            style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_DOCKABLE)

        self.treeCtrl = NotesTreeCtrl(self)

        self.SetSize((256, 260))
        self.__do_layout()

        self.dragItem = None
        self.popupPage = None
        self.popupMenu = None

        # Секция настроек куда сохраняем развернутость страницы
        self.pageOptionsSection = 'Tree'

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = 'Expand'

        self.__BindApplicationEvents()
        self.__BindGuiEvents()
        self._dropTarget = NotesTreeDropFilesTarget(self._application,
                                                    self.treeCtrl,
                                                    self)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.treeCtrl.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.treeCtrl.SetForegroundColour(colour)

    def getPageByItemId(self, item_id: wx.TreeItemId) -> 'outwiker.core.tree.WikiPage':
        return self.treeCtrl.GetItemData(item_id)

    def __BindApplicationEvents(self):
        """
        Подписка на события контроллера
        """
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onTreeUpdate += self.__onTreeUpdate
        self._application.onPageCreate += self.__onPageCreate
        self._application.onPageOrderChange += self.__onPageOrderChange
        self._application.onPageSelect += self.__onPageSelect
        self._application.onPageRemove += self.__onPageRemove
        self._application.onPageUpdate += self.__onPageUpdate
        self._application.onStartTreeUpdate += self.__onStartTreeUpdate
        self._application.onEndTreeUpdate += self.__onEndTreeUpdate

    def __UnBindApplicationEvents(self):
        """
        Отписка от событий контроллера
        """
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onTreeUpdate -= self.__onTreeUpdate
        self._application.onPageCreate -= self.__onPageCreate
        self._application.onPageOrderChange -= self.__onPageOrderChange
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onPageRemove -= self.__onPageRemove
        self._application.onPageUpdate -= self.__onPageUpdate
        self._application.onStartTreeUpdate -= self.__onStartTreeUpdate
        self._application.onEndTreeUpdate -= self.__onEndTreeUpdate

    def __onWikiOpen(self, root):
        self.treeCtrl.treeUpdate(root)

    def __onPageUpdate(self, page, **kwargs):
        change = kwargs['change']
        if change & PAGE_UPDATE_ICON:
            self.treeCtrl.updateIcon(page)

        if change & PAGE_UPDATE_TITLE:
            item = self.treeCtrl.getTreeItem(page)
            self.treeCtrl.SetItemText(item, page.display_title)

    def __BindGuiEvents(self):
        """
        Подписка на события интерфейса
        """
        # События, связанные с деревом
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)
        self.Bind(wx.EVT_TREE_ITEM_MIDDLE_CLICK, self.__onMiddleClick)

        # Перетаскивание элементов
        self.treeCtrl.Bind(wx.EVT_TREE_BEGIN_DRAG, self.__onBeginDrag)
        self.treeCtrl.Bind(wx.EVT_TREE_END_DRAG, self.__onEndDrag)

        # Переименование элемента
        self.treeCtrl.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.__onEndLabelEdit)

        # Показ всплывающего меню
        self.treeCtrl.Bind(wx.EVT_TREE_ITEM_MENU, self.__onPopupMenu)

        # Сворачивание/разворачивание элементов
        self.treeCtrl.Bind(wx.EVT_TREE_ITEM_COLLAPSED,
                           self.__onTreeStateChanged)
        self.treeCtrl.Bind(wx.EVT_TREE_ITEM_EXPANDED,
                           self.__onTreeStateChanged)
        self.treeCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED,
                           self.__onTreeItemActivated)

        self.Bind(wx.EVT_CLOSE, self.__onClose)

    def __onMiddleClick(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return

        page = self.treeCtrl.GetItemData(item)
        self._application.mainWindow.tabsController.openInTab(page, True)

    def __onClose(self, _event):
        self._dropTarget.destroy()
        self.__UnBindApplicationEvents()
        self.treeCtrl.DeleteAllItems()
        self._removeButtons()
        self.toolbar.ClearTools()
        self.Destroy()

    def __onPageCreate(self, newpage):
        """
        Обработка создания страницы
        """
        self.treeCtrl.createPage(newpage)

    def __onPageRemove(self, page):
        self.treeCtrl.removePageItem(page)

    def __onTreeItemActivated(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return

        page = self.treeCtrl.GetItemData(item)
        editPage(self, page)

    def __onTreeStateChanged(self, event):
        item = event.GetItem()
        assert item.IsOk()
        page = self.treeCtrl.GetItemData(item)
        self.__saveItemState(item)

        for child in page.children:
            self.treeCtrl.appendChildren(child)

    def __saveItemState(self, itemid):
        assert itemid.IsOk()

        page = self.treeCtrl.GetItemData(itemid)
        if page.readonly:
            return

        expanded = self.treeCtrl.IsExpanded(itemid)

        page_registry = page.root.registry.get_page_registry(page)
        page_registry.set(self.pageOptionExpand, expanded)

    def __onPopupMenu(self, event):
        self.popupPage = None
        popupItem = event.GetItem()
        if not popupItem.IsOk():
            return

        popupPage = self.treeCtrl.GetItemData(popupItem)
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

        selectedItem = self.treeCtrl.getTreeItem(pageToRename)
        if not selectedItem.IsOk():
            return

        self.treeCtrl.EditLabel(selectedItem)

    def __onEndLabelEdit(self, event):
        if event.IsEditCancelled():
            return

        # Новый заголовок
        label = event.GetLabel().strip()

        item = event.GetItem()
        page = self.treeCtrl.GetItemData(item)
        # Не доверяем переименовывать элементы системе
        event.Veto()
        renamePage(page, label)

    def __onStartTreeUpdate(self, _root):
        self.__unbindUpdateEvents()

    def __unbindUpdateEvents(self):
        self._application.onTreeUpdate -= self.__onTreeUpdate
        self._application.onPageCreate -= self.__onPageCreate
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onPageOrderChange -= self.__onPageOrderChange
        self.Unbind(wx.EVT_TREE_SEL_CHANGED, handler=self.__onSelChanged)

    def __onEndTreeUpdate(self, _root):
        self.__bindUpdateEvents()
        self.treeCtrl.treeUpdate(self._application.wikiroot)

    def __bindUpdateEvents(self):
        self._application.onTreeUpdate += self.__onTreeUpdate
        self._application.onPageCreate += self.__onPageCreate
        self._application.onPageSelect += self.__onPageSelect
        self._application.onPageOrderChange += self.__onPageOrderChange
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)

    def __onBeginDrag(self, event):
        event.Allow()
        self.dragItem = event.GetItem()
        self.treeCtrl.SetFocus()

    def __onEndDrag(self, event):
        if self.dragItem is not None:
            # Элемент, на который перетащили другой элемент(self.dragItem)
            endDragItem = event.GetItem()

            # Перетаскиваемая станица
            draggedPage = self.treeCtrl.GetItemData(self.dragItem)

            # Будущий родитель для страницы
            if endDragItem.IsOk():
                newParent = self.treeCtrl.GetItemData(endDragItem)

                # Moving page to itself is ignored
                if newParent != draggedPage:
                    movePage(draggedPage, newParent)
                    self.treeCtrl.expand(newParent)

        self.dragItem = None

    def __onTreeUpdate(self, sender):
        self.treeCtrl.treeUpdate(sender.root)

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

        if(ctrlstate or shiftstate) and not self._externalPageSelect:
            self._application.mainWindow.tabsController.openInTab(
                self.selectedPage,
                True)
        else:
            self._application.selectedPage = self.selectedPage

    def __onPageOrderChange(self, sender):
        """
        Изменение порядка страниц
        """
        self.__updatePage(sender)

    @property
    def selectedPage(self):
        return self.treeCtrl.selectedPage

    @selectedPage.setter
    def selectedPage(self, newSelPage):
        self.treeCtrl.selectedPage = newSelPage

    def __do_layout(self):
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
            getBuiltinImagePath("go_to_parent.png"),
            False)

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            MovePageDownAction.stringId,
            self.toolbar,
            getBuiltinImagePath("move_down.png"),
            False)

        actionController.appendToolbarButton(
            MovePageUpAction.stringId,
            self.toolbar,
            getBuiltinImagePath("move_up.png"),
            False)

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            AddSiblingPageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-insert-next.png"),
            False)

        actionController.appendToolbarButton(
            AddChildPageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-insert-child.png"),
            False)

        actionController.appendToolbarButton(
            RemovePageAction.stringId,
            self.toolbar,
            getBuiltinImagePath("node-delete.png"),
            False)

        self.toolbar.AddSeparator()

        actionController.appendToolbarButton(
            EditPagePropertiesAction.stringId,
            self.toolbar,
            getBuiltinImagePath("edit.png"),
            False)

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

    def getTreeItem(self, page: 'outwiker.core.tree.WikiPage') -> Optional[wx.TreeItemId]:
        """
        Получить элемент дерева по странице.
        Если для страницы не создан элемент дерева, возвращается None
        """
        return self.treeCtrl.getTreeItem(page)

    def __scrollToCurrentPage(self):
        """
        Если текущая страница вылезла за пределы видимости, то прокрутить к ней
        """
        selectedPage = self._application.selectedPage
        if selectedPage is None:
            return

        item = self.treeCtrl.getTreeItem(selectedPage)
        if not self.treeCtrl.IsVisible(item):
            self.treeCtrl.ScrollTo(item)

    def __updatePage(self, page):
        """
        Обновить страницу (удалить из списка и добавить снова)
        """
        # Отпишемся от обновлений страниц, чтобы не изменять выбранную страницу
        self.__unbindUpdateEvents()
        self.Freeze()

        try:
            self.treeCtrl.removePageItem(page)

            item = self.treeCtrl.insertChild(page)

            if page.root.selectedPage == page:
                # Если обновляем выбранную страницу
                self.treeCtrl.SelectItem(item)

            self.__scrollToCurrentPage()
        finally:
            self.Thaw()
            self.__bindUpdateEvents()

    def expand(self, page):
        self.treeCtrl.expand(page)


class NotesTreeDropFilesTarget(BaseDropFilesTarget):
    """
    Class to drop files to notes in the notes tree panel.
    """

    def __init__(self, application,
                 targetWindow: wx.TreeCtrl,
                 notesTree: NotesTree):
        super().__init__(application, targetWindow)
        self._notesTree = notesTree

    def OnDropFiles(self, x, y, files):
        correctedFiles = self.correctFileNames(files)
        flags_mask = wx.TREE_HITTEST_ONITEMICON | wx.TREE_HITTEST_ONITEMLABEL
        item, flags = self.targetWindow.HitTest((x, y))

        if flags & flags_mask:
            page = self._notesTree.getPageByItemId(item)
            if page is not None:
                file_names = [os.path.basename(fname)
                              for fname
                              in correctedFiles]

                text = _("Attach files to the note '{title}'?\n\n{files}").format(
                    title=page.display_title,
                    files='\n'.join(file_names)
                )

                if MessageBox(text,
                              _("Attach files to the note?"),
                              wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                    attachFiles(self._application.mainWindow,
                                page, correctedFiles)
                return True

        return False
