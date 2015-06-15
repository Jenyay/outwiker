# -*- coding: UTF-8 -*-

import os
import os.path
import ConfigParser

import wx

from outwiker.core.application import Application
import outwiker.core.commands
import outwiker.core.system
import outwiker.gui.pagedialog
from outwiker.core.config import BooleanOption
from outwiker.gui.pagepopupmenu import PagePopupMenu
from outwiker.actions.addsiblingpage import AddSiblingPageAction
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction
from outwiker.actions.removepage import RemovePageAction
from outwiker.actions.editpageprop import EditPagePropertiesAction
from outwiker.core.events import PAGE_UPDATE_ICON
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT


class NotesTree(wx.Panel):
    def __init__(self, *args, **kwds):
        self.ID_PROPERTIES_BUTTON = wx.NewId()
        self.ID_MOVE_UP = wx.NewId()
        self.ID_MOVE_DOWN = wx.NewId()
        self.ID_ADD_SIBLING_PAGE = wx.NewId()
        self.ID_ADD_CHILD_PAGE = wx.NewId()
        self.ID_REMOVE_PAGE = wx.NewId()

        # Переключатель, устанавливается в True, если "внезапно" изменяется текущая страница
        self.__externalPageSelect = False

        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.toolbar = wx.ToolBar (self,
                                   -1,
                                   style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_DOCKABLE)

        treeStyle = (wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER)

        self.treeCtrl = wx.TreeCtrl(self, style=treeStyle)

        self.__set_properties()
        self.__do_layout()

        self.defaultIcon = os.path.join (outwiker.core.system.getImagesDir(), "page.png")
        self.iconHeight = ICON_HEIGHT

        self.defaultBitmap = wx.Bitmap (self.defaultIcon)
        assert self.defaultBitmap.IsOk()

        self.defaultBitmap.SetHeight (self.iconHeight)

        self.dragItem = None

        # Картинки для дерева
        self.imagelist = wx.ImageList(ICON_WIDTH, self.iconHeight)
        self.treeCtrl.AssignImageList (self.imagelist)

        # Кеш для страниц, чтобы было проще искать элемент дерева по странице
        # Словарь. Ключ - страница, значение - элемент дерева wx.TreeItemId
        self._pageCache = {}

        self.popupMenu = None

        # Секция настроек куда сохраняем развернутость страницы
        self.pageOptionsSection = u"Tree"

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = "Expand"

        self.__BindApplicationEvents()
        self.__BindGuiEvents()


    def getTreeItem (self, page):
        """
        Получить элемент дерева по странице.
        Если для страницы не создан элемент дерева, возвращается None
        """
        if page in self._pageCache:
            return self._pageCache[page]


    def __BindApplicationEvents(self):
        """
        Подписка на события контроллера
        """
        Application.onWikiOpen += self.__onWikiOpen
        Application.onTreeUpdate += self.__onTreeUpdate
        Application.onPageCreate += self.__onPageCreate
        Application.onPageOrderChange += self.__onPageOrderChange
        Application.onPageSelect += self.__onPageSelect
        Application.onPageRemove += self.__onPageRemove
        Application.onPageUpdate += self.__onPageUpdate

        Application.onStartTreeUpdate += self.__onStartTreeUpdate
        Application.onEndTreeUpdate += self.__onEndTreeUpdate


    def __UnBindApplicationEvents(self):
        """
        Отписка от событий контроллера
        """
        Application.onWikiOpen -= self.__onWikiOpen
        Application.onTreeUpdate -= self.__onTreeUpdate
        Application.onPageCreate -= self.__onPageCreate
        Application.onPageOrderChange -= self.__onPageOrderChange
        Application.onPageSelect -= self.__onPageSelect
        Application.onPageRemove -= self.__onPageRemove
        Application.onPageUpdate -= self.__onPageUpdate

        Application.onStartTreeUpdate -= self.__onStartTreeUpdate
        Application.onEndTreeUpdate -= self.__onEndTreeUpdate


    def __onWikiOpen (self, root):
        self.__treeUpdate (root)


    def __onPageUpdate (self, sender, **kwargs):
        change = kwargs['change']
        if change == PAGE_UPDATE_ICON:
            self.__updateIcon (sender)


    def __loadIcon (self, page):
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        icon = page.icon

        if icon is not None:
            image = wx.Bitmap (icon)
            image.SetHeight (self.iconHeight)
            imageId = self.imagelist.Add (image)
        else:
            imageId = self.defaultImageId

        return imageId


    def __updateIcon (self, page):
        if page not in self._pageCache:
            # Если нет этой страницы в дереве, то не важно, изменилась иконка или нет
            return

        self.treeCtrl.SetItemImage (self._pageCache[page],
                                    self.__loadIcon (page))


    def __BindGuiEvents (self):
        """
        Подписка на события интерфейса
        """
        # События, связанные с деревом
        self.Bind (wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)
        self.Bind (wx.EVT_TREE_ITEM_MIDDLE_CLICK, self.__onMiddleClick)

        # Перетаскивание элементов
        self.treeCtrl.Bind (wx.EVT_TREE_BEGIN_DRAG, self.__onBeginDrag)
        self.treeCtrl.Bind (wx.EVT_TREE_END_DRAG, self.__onEndDrag)

        # Переименование элемента
        self.treeCtrl.Bind (wx.EVT_TREE_END_LABEL_EDIT, self.__onEndLabelEdit)

        # Показ всплывающего меню
        self.treeCtrl.Bind (wx.EVT_TREE_ITEM_MENU, self.__onPopupMenu)

        # Сворачивание/разворачивание элементов
        self.treeCtrl.Bind (wx.EVT_TREE_ITEM_COLLAPSED, self.__onTreeStateChanged)
        self.treeCtrl.Bind (wx.EVT_TREE_ITEM_EXPANDED, self.__onTreeStateChanged)

        self.treeCtrl.Bind (wx.EVT_TREE_ITEM_ACTIVATED, self.__onTreeItemActivated)

        self.Bind(wx.EVT_MENU, self.__onMoveUp, id=self.ID_MOVE_UP)
        self.Bind(wx.EVT_MENU, self.__onMoveDown, id=self.ID_MOVE_DOWN)
        self.Bind(wx.EVT_MENU, self.__onAddSiblingPage, id=self.ID_ADD_SIBLING_PAGE)
        self.Bind(wx.EVT_MENU, self.__onAddChildPage, id=self.ID_ADD_CHILD_PAGE)
        self.Bind(wx.EVT_MENU, self.__onRemovePage, id=self.ID_REMOVE_PAGE)

        self.Bind(wx.EVT_MENU, self.__onPropertiesButton, id=self.ID_PROPERTIES_BUTTON)

        self.Bind (wx.EVT_CLOSE, self.__onClose)


    def __onMiddleClick (self, event):
        item = event.GetItem()
        if not item.IsOk():
            return

        page = self.treeCtrl.GetItemData (item).GetData()
        Application.mainWindow.tabsController.openInTab (page, True)


    def __onClose (self, event):
        self.__UnBindApplicationEvents()
        self.treeCtrl.DeleteAllItems()
        self.imagelist.RemoveAll()
        self.toolbar.ClearTools()
        self.Destroy()


    def __onPageCreate (self, newpage):
        """
        Обработка создания страницы
        """
        if newpage.parent in self._pageCache:
            self.__insertChild (newpage)

            assert newpage in self._pageCache
            item = self._pageCache[newpage]
            assert item.IsOk()

            self.expand (newpage)


    def __onPropertiesButton (self, event):
        Application.actionController.getAction (EditPagePropertiesAction.stringId).run (None)


    def __onAddSiblingPage (self, event):
        Application.actionController.getAction (AddSiblingPageAction.stringId).run (None)


    def __onAddChildPage (self, event):
        Application.actionController.getAction (AddChildPageAction.stringId).run (None)


    def __onRemovePage (self, event):
        Application.actionController.getAction (RemovePageAction.stringId).run (None)


    def __onMoveUp (self, event):
        if Application.wikiroot.selectedPage is not None:
            Application.actionController.getAction (MovePageUpAction.stringId).run (None)


    def __onMoveDown (self, event):
        if Application.wikiroot.selectedPage is not None:
            Application.actionController.getAction (MovePageDownAction.stringId).run (None)


    def __onPageRemove (self, page):
        self.__removePageItem (page)


    def __onTreeItemActivated (self, event):
        item = event.GetItem()
        if not item.IsOk():
            return

        page = self.treeCtrl.GetItemData (item).GetData()
        outwiker.gui.pagedialog.editPage (self, page)


    def __onTreeStateChanged (self, event):
        item = event.GetItem()
        assert item.IsOk()
        page = self.treeCtrl.GetItemData (item).GetData()
        self.__saveItemState (item)

        for child in page.children:
            self.__appendChildren (child)


    def __saveItemState (self, itemid):
        assert itemid.IsOk()

        page = self.treeCtrl.GetItemData (itemid).GetData()
        expanded = self.treeCtrl.IsExpanded (itemid)
        expandedOption = BooleanOption (page.params, self.pageOptionsSection, self.pageOptionExpand, False)

        try:
            expandedOption.value = expanded
        except IOError, e:
            outwiker.core.commands.MessageBox (
                _(u"Can't save page options\n{}").format(unicode (e)),
                _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __getItemExpandState (self, page):
        """
        Проверить, раскрыт ли элемент в дереве для страницы page
        """
        if page is None:
            return True

        if page.parent is None:
            return True

        return self.treeCtrl.IsExpanded (self._pageCache[page])


    def __getPageExpandState (self, page):
        """
        Проверить состояние "раскрытости" страницы (что по этому поводу написано в настройках страницы)
        """
        if page is None:
            return True

        if page.parent is None:
            return True

        try:
            expanded = page.params.getbool (self.pageOptionsSection, self.pageOptionExpand)
        except ConfigParser.NoSectionError:
            return False
        except ConfigParser.NoOptionError:
            return False

        return expanded


    def __onPopupMenu (self, event):
        self.popupPage = None
        popupItem = event.GetItem()
        if not popupItem.IsOk ():
            return

        popupPage = self.treeCtrl.GetItemData (popupItem).GetData()
        self.popupMenu = PagePopupMenu (self, popupPage, Application)
        self.PopupMenu (self.popupMenu.menu)


    def beginRename (self, page=None):
        """
        Начать переименование страницы в дереве. Если page is None, то начать переименование текущей страницы
        """
        pageToRename = page if page is not None else Application.selectedPage

        if pageToRename is None or pageToRename.parent is None:
            outwiker.core.commands.MessageBox (_(u"You can't rename the root element"),
                                               _(u"Error"),
                                               wx.ICON_ERROR | wx.OK)
            return

        selectedItem = self._pageCache[pageToRename]
        if not selectedItem.IsOk():
            return

        self.treeCtrl.EditLabel (selectedItem)


    def __onEndLabelEdit (self, event):
        if event.IsEditCancelled():
            return

        # Новый заголовок
        label = event.GetLabel().strip()

        item = event.GetItem()
        page = self.treeCtrl.GetItemData (item).GetData()

        # Не доверяем переименовывать элементы системе
        event.Veto()

        outwiker.core.commands.renamePage (page, label)


    def __onStartTreeUpdate (self, root):
        self.__unbindUpdateEvents()


    def __unbindUpdateEvents (self):
        Application.onTreeUpdate -= self.__onTreeUpdate
        Application.onPageCreate -= self.__onPageCreate
        Application.onPageSelect -= self.__onPageSelect
        Application.onPageOrderChange -= self.__onPageOrderChange
        self.Unbind (wx.EVT_TREE_SEL_CHANGED, handler = self.__onSelChanged)


    def __onEndTreeUpdate (self, root):
        self.__bindUpdateEvents()
        self.__treeUpdate (Application.wikiroot)


    def __bindUpdateEvents (self):
        Application.onTreeUpdate += self.__onTreeUpdate
        Application.onPageCreate += self.__onPageCreate
        Application.onPageSelect += self.__onPageSelect
        Application.onPageOrderChange += self.__onPageOrderChange
        self.Bind (wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)


    def __onBeginDrag (self, event):
        event.Allow()
        self.dragItem = event.GetItem()
        self.treeCtrl.SetFocus()


    def __onEndDrag (self, event):
        if self.dragItem is not None:
            # Элемент, на который перетащили другой элемент (self.dragItem)
            endDragItem = event.GetItem()

            # Перетаскиваемая станица
            draggedPage = self.treeCtrl.GetItemData (self.dragItem).GetData()

            # Будущий родитель для страницы
            if endDragItem.IsOk():
                newParent = self.treeCtrl.GetItemData (endDragItem).GetData()

                # Moving page to itself is ignored
                if newParent != draggedPage:
                    outwiker.core.commands.movePage (draggedPage, newParent)
                    self.expand (newParent)

        self.dragItem = None


    def __onTreeUpdate (self, sender):
        self.__treeUpdate (sender.root)


    def __onPageSelect (self, page):
        """
        Изменение выбранной страницы
        """
        # Пометим, что изменение страницы произошло снаружи, а не из-за клика по дереву
        self.__externalPageSelect = True

        try:
            currpage = self.selectedPage
            if currpage != page:
                self.selectedPage = page
        finally:
            self.__externalPageSelect = False


    def __onSelChanged (self, event):
        ctrlstate = wx.GetKeyState(wx.WXK_CONTROL)
        shiftstate = wx.GetKeyState(wx.WXK_SHIFT)

        if (ctrlstate or shiftstate) and not self.__externalPageSelect:
            Application.mainWindow.tabsController.openInTab (self.selectedPage, True)
        else:
            Application.selectedPage = self.selectedPage


    def __onPageOrderChange (self, sender):
        """
        Изменение порядка страниц
        """
        self.__updatePage (sender)


    @property
    def selectedPage (self):
        page = None

        item = self.treeCtrl.GetSelection ()
        if item.IsOk():
            page = self.treeCtrl.GetItemData (item).GetData()

            # Проверка того, что выбрали не корневой элемент
            if page.parent is None:
                page = None

        return page


    @selectedPage.setter
    def selectedPage (self, newSelPage):
        if newSelPage is None:
            item = self.treeCtrl.GetRootItem()
        else:
            self.__expandToPage (newSelPage)
            item = self.getTreeItem (newSelPage)

        if item is not None:
            self.treeCtrl.SelectItem (item)


    def __expandToPage (self, page):
        """
        Развернуть ветви до того уровня, чтобы появился элемент для page
        """
        # Список родительских страниц, которые нужно добавить в дерево
        pages = []
        currentPage = page.parent
        while currentPage is not None:
            pages.append (currentPage)
            currentPage = currentPage.parent

        pages.reverse()
        for page in pages:
            self.expand (page)


    def __set_properties(self):
        self.SetSize((256, 260))

    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(1)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(self.toolbar, 1, wx.EXPAND, 0)
        mainSizer.Add(self.treeCtrl, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)


    def expand (self, page):
        item = self.getTreeItem (page)
        if item is not None:
            self.treeCtrl.Expand (item)


    def __treeUpdate (self, rootPage):
        """
        Обновить дерево
        """
        self.treeCtrl.DeleteAllItems()
        self.imagelist.RemoveAll()
        self.defaultImageId = self.imagelist.Add (self.defaultBitmap)

        # Ключ - страница, значение - экземпляр класса TreeItemId
        self._pageCache = {}

        if rootPage is not None:
            rootname = os.path.basename (rootPage.path)
            rootItem = self.treeCtrl.AddRoot (
                rootname,
                data = wx.TreeItemData (rootPage),
                image = self.defaultImageId)

            self._pageCache[rootPage] = rootItem
            self.__mountItem (rootItem, rootPage)
            self.__appendChildren (rootPage)

            self.selectedPage = rootPage.selectedPage
            self.expand (rootPage)


    def __appendChildren (self, parentPage):
        """
        Добавить детей в дерево
        parentPage - родительская страница, куда добавляем дочерние страницы
        """
        grandParentExpanded = self.__getItemExpandState (parentPage.parent)

        if grandParentExpanded:
            for child in parentPage.children:
                if child not in self._pageCache:
                    self.__insertChild (child)

        if self.__getPageExpandState (parentPage):
            self.expand (parentPage)


    def __mountItem (self, treeitem, page):
        """
        Оформить элемент дерева в зависимости от настроек страницы (например, пометить только для чтения)
        """
        if page.readonly:
            font = wx.SystemSettings.GetFont (wx.SYS_DEFAULT_GUI_FONT)
            font.SetStyle (wx.FONTSTYLE_ITALIC)
            self.treeCtrl.SetItemFont (treeitem, font)


    def __insertChild (self, child):
        """
        Вставить одну дочерниюю страницу (child) в ветвь
        """
        parentItem = self.getTreeItem (child.parent)
        assert parentItem is not None

        item = self.treeCtrl.InsertItemBefore (parentItem,
                                               child.order,
                                               child.title,
                                               data = wx.TreeItemData(child))

        self.treeCtrl.SetItemImage (item, self.__loadIcon (child))

        self._pageCache[child] = item
        self.__mountItem (item, child)
        self.__appendChildren (child)

        return item


    def __removePageItem (self, page):
        """
        Удалить элемент, соответствующий странице и все его дочерние страницы
        """
        for child in page.children:
            self.__removePageItem (child)

        item = self.getTreeItem (page)
        if item is not None:
            del self._pageCache[page]
            self.treeCtrl.Delete (item)


    def __updatePage (self, page):
        """
        Обновить страницу (удалить из списка и добавить снова)
        """
        # Отпишемся от обновлений страниц, чтобы не изменять выбранную страницу
        self.__unbindUpdateEvents()
        self.treeCtrl.Freeze()

        try:
            self.__removePageItem (page)

            item = self.__insertChild (page)

            if page.root.selectedPage == page:
                # Если обновляем выбранную страницу
                self.treeCtrl.SelectItem (item)

            self.__scrollToCurrentPage()
        finally:
            self.treeCtrl.Thaw()
            self.__bindUpdateEvents()


    def __scrollToCurrentPage (self):
        """
        Если текущая страница вылезла за пределы видимости, то прокрутить к ней
        """
        selectedPage = Application.selectedPage
        if selectedPage is None:
            return

        item = self.getTreeItem (selectedPage)
        if not self.treeCtrl.IsVisible (item):
            self.treeCtrl.ScrollTo (item)


    def addButtons (self):
        """
        Добавить кнопки на панель
        Т.к. текст подсказок берется из Actions, этот метод вызывается после создания окна
        """
        imagesDir = outwiker.core.system.getImagesDir()
        actionController = Application.actionController

        moveDownTitle = actionController.getTitle (MovePageDownAction.stringId)
        self.toolbar.AddLabelTool(self.ID_MOVE_DOWN,
                                  moveDownTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "move_down.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  moveDownTitle,
                                  "")


        moveUpTitle = actionController.getTitle (MovePageUpAction.stringId)
        self.toolbar.AddLabelTool(self.ID_MOVE_UP,
                                  moveUpTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "move_up.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  moveUpTitle,
                                  "")
        self.toolbar.AddSeparator()


        siblingTitle = actionController.getTitle (AddSiblingPageAction.stringId)
        self.toolbar.AddLabelTool(self.ID_ADD_SIBLING_PAGE,
                                  siblingTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "node-insert-next.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  siblingTitle,
                                  "")


        childTitle = actionController.getTitle (AddChildPageAction.stringId)
        self.toolbar.AddLabelTool(self.ID_ADD_CHILD_PAGE,
                                  childTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "node-insert-child.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  childTitle,
                                  "")


        removeTitle = actionController.getTitle (RemovePageAction.stringId)
        self.toolbar.AddLabelTool(self.ID_REMOVE_PAGE,
                                  removeTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "node-delete.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  removeTitle,
                                  "")

        self.toolbar.AddSeparator()


        propertiesTitle = actionController.getTitle (EditPagePropertiesAction.stringId)
        self.toolbar.AddLabelTool(self.ID_PROPERTIES_BUTTON,
                                  propertiesTitle,
                                  wx.Bitmap(os.path.join (imagesDir, "edit.png"),
                                            wx.BITMAP_TYPE_ANY),
                                  wx.NullBitmap,
                                  wx.ITEM_NORMAL,
                                  propertiesTitle,
                                  "")

        self.toolbar.Realize()
