# coding: utf-8

import logging
import os
from typing import Dict, Optional, List

from outwiker.core.tree import BasePage, WikiDocument, WikiPage
import wx

from outwiker.core.defines import ICON_HEIGHT
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache

logger = logging.getLogger("outwiker.gui.controls.notestreectrl2")

class NotesTreeItem:
    def __init__(self, title: str, page: BasePage, depth) -> None:
        self._title = title
        self._page = page
        self._depth = depth
        self._line = 0
        self._children: List["NotesTreeItem"] = []
        self._imageId = -1
        self._bold = False
        self._italic = False
        self._fontColor = wx.Colour(0, 0, 0)
        self._backColor = wx.Colour(0, 0, 0)
        self._expanded = False

    def getDepth(self) -> int:
        return self._depth

    def getLine(self) -> int:
        return self._line

    def setLine(self, line: int) -> "NotesTreeItem":
        self._line = line
        return self

    def addChild(self, child: "NotesTreeItem") -> "NotesTreeItem":
        self._children.append(child)
        return self

    def setImageId(self, imageId) -> "NotesTreeItem":
        self._imageId = imageId
        return self

    def isExpanded(self) -> bool:
        return self._expanded

    def expand(self, expanded=True) -> "NotesTreeItem":
        self._expanded = expanded
        return self

    def insertChild(self, index: int, child: "NotesTreeItem") -> "NotesTreeItem":
        if index < 0:
            index = 0
        if index >= len(self._children):
            index = len(self._children)

        self._children.insert(index, child)
        return self


class NotesTreeCtrl2(wx.ScrolledCanvas):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self._iconHeight = ICON_HEIGHT
        self._lineHeight = self._iconHeight + 6
        self._indent = 16
        self._fontSize = 12
        self._linesGap = 3
        self._expandCtrlWidth = 8
        self._expandCtrlHeight = 8
        self._expandCtrlLeftGap = 3
        self._expandCtrlRightGap = 3
        self.SetScrollRate(0, 0)

        self.defaultIcon = getBuiltinImagePath('page.svg')

        # Картинки для дерева
        self._iconsCache = ImageListCache(self.defaultIcon)

        # Кеш для страниц, чтобы было проще искать элемент дерева по странице
        # Словарь. Ключ - страница, значение - элемент дерева NotesTreeItem
        self._pageCache: Dict[BasePage, NotesTreeItem] = {}

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = 'Expand'

        self._items: List[NotesTreeItem] = []
        self._lineCount = 0

        self.Bind(wx.EVT_CLOSE, self._onClose)
        self.Bind(wx.EVT_PAINT, handler=self._onPaint)

    def _onPaint(self, event):
        with wx.PaintDC(self) as dc:
            back_color = self.GetBackgroundColour()
            dc.SetBrush(wx.Brush(back_color))
            dc.SetPen(wx.Pen(back_color))
            width, height = self.GetClientSize()
            dc.DrawRectangle(0, 0, width, height)

    def _onClose(self, event):
        self._iconsCache.clear()

    def _createRootNotesTreeItem(self, rootPage: WikiDocument) -> "NotesTreeItem":
        rootname = os.path.basename(rootPage.path)
        return (NotesTreeItem(rootname, rootPage, 0)
                .setImageId(self._iconsCache.getDefaultImageId())
        )

    def _createNotesTreeItem(self, page: WikiPage) -> "NotesTreeItem":
        title = page.display_title
        parent_page = page.parent
        assert parent_page is not None

        parent_item = self._pageCache[parent_page]

        return (NotesTreeItem(title, page, parent_item.getDepth() + 1)
                .setImageId(self._loadIcon(page))
                )

    def treeUpdate(self, rootPage):
        """
        Обновить дерево
        """
        self._iconsCache.clear()
        self._pageCache.clear()
        self._items.clear()

        if rootPage is not None:
            root_item = self._createRootNotesTreeItem(rootPage)
            self._pageCache[rootPage] = root_item
            self.appendChildren(rootPage)

            self.selectedPage = rootPage.selectedPage
            self.expand(rootPage)

    def appendChildren(self, parentPage):
        """
        Добавить детей в дерево
        parentPage - родительская страница, куда добавляем дочерние страницы
        """
        grandParentExpanded = self._getItemExpandState(parentPage.parent)

        if grandParentExpanded:
            for child in parentPage.children:
                if child not in self._pageCache:
                    self.insertChild(child)

        if self._getPageExpandState(parentPage):
            self.expand(parentPage)

    def insertChild(self, childPage):
        """
        Вставить одну дочерниюю страницу (childPage) в ветвь
        """
        parentItem = self.getTreeItem(childPage.parent)
        assert parentItem is not None

        childItem = self._createNotesTreeItem(childPage)
        childItem.insertChild(childPage.order, childItem)

        self._pageCache[childPage] = childItem
        self.appendChildren(childPage)

        return childItem

    def removePageItem(self, page):
        """
        Удалить элемент, соответствующий странице и все его дочерние страницы
        """
        # for child in page.children:
        #     self.removePageItem(child)

        # item = self.getTreeItem(page)
        # if item is not None:
        #     del self._pageCache[page]
        #     self.Delete(item)

    def _loadIcon(self, page):
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        icon = page.icon

        if not icon:
            return self._iconsCache.getDefaultImageId()

        icon = os.path.abspath(icon)
        page_path = os.path.abspath(page.path)

        try:
            if icon.startswith(page_path):
                imageId = self._iconsCache.replace(icon)
            else:
                imageId = self._iconsCache.add(icon)
        except Exception:
            logger.error("Invalid icon file: %s", icon)
            imageId = self._iconsCache.getDefaultImageId()
        return imageId

    def updateIcon(self, page):
        # if page not in self._pageCache:
        #     # Если нет этой страницы в дереве, то не важно,
        #     # изменилась иконка или нет
        #     return

        # icon_id = self._loadIcon(page)
        # self.SetItemImage(self._pageCache[page], icon_id)
        pass

    def _getItemExpandState(self, page):
        """
        Проверить, раскрыт ли элемент в дереве для страницы page
        """
        if page is None:
            return True

        if page.parent is None:
            return True

        return self._pageCache[page].isExpanded()

    def _getPageExpandState(self, page):
        """
        Проверить состояние "раскрытости" страницы
        """
        if page is None:
            return True

        if page.parent is None:
            return True

        page_registry = page.root.registry.get_page_registry(page)
        expanded = page_registry.getbool(self.pageOptionExpand, default=False)

        return expanded

    def getTreeItem(self, page: BasePage) -> Optional[NotesTreeItem]:
        """
        Получить элемент дерева по странице.
        Если для страницы не создан элемент дерева, возвращается None
        """
        return self._pageCache.get(page)

    def expandToPage(self, page):
        """
        Развернуть ветви до того уровня, чтобы появился элемент для page
        """
        # Список родительских страниц, которые нужно добавить в дерево
        # pages = []
        # currentPage = page.parent
        # while currentPage is not None:
        #     pages.append(currentPage)
        #     currentPage = currentPage.parent

        # pages.reverse()
        # for page in pages:
        #     self.expand(page)

    def expand(self, page):
        item = self.getTreeItem(page)
        if item is not None:
            item.expand()

    def createPage(self, newpage):
        # if newpage.parent in self._pageCache:
        #     self.insertChild(newpage)

        #     assert newpage in self._pageCache
        #     item = self._pageCache[newpage]
        #     assert item.IsOk()

        #     self.expand(newpage)
        pass

    @property
    def selectedPage(self):
        page = None

        # item = self.GetSelection()
        # if item.IsOk():
        #     page = self.GetItemData(item)

        #     # Проверка того, что выбрали не корневой элемент
        #     if page.parent is None:
        #         page = None

        return page

    @selectedPage.setter
    def selectedPage(self, newSelPage):
        # if newSelPage is None:
        #     item = self.GetRootItem()
        # else:
        #     self.expandToPage(newSelPage)
        #     item = self.getTreeItem(newSelPage)

        # if item is not None:
        #     self.SelectItem(item)
        pass
