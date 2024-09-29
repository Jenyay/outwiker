# coding: utf-8

import logging
import os
from typing import Dict, Optional, List, Tuple

from outwiker.core.tree import BasePage, WikiDocument, WikiPage
import wx

from outwiker.core.defines import ICON_HEIGHT
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache

logger = logging.getLogger("outwiker.gui.controls.notestreectrl2")


class NotesTreeItem:
    def __init__(
        self, title: str, page: BasePage, parent: Optional["NotesTreeItem"]
    ) -> None:
        self._title = title
        self._page = page
        self._depth = parent.getDepth() + 1 if parent is not None else 0
        self._line = 0
        self._parent: Optional["NotesTreeItem"] = parent
        self._children: List["NotesTreeItem"] = []
        self._imageId = -1
        self._bold = False
        self._italic = False
        self._fontColor = wx.Colour(0, 0, 0)
        self._backColor = wx.Colour(0, 0, 0)
        self._expanded = False
        self._selected = False

    def getTitle(self) -> str:
        return self._title

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

    def isSelected(self) -> bool:
        return self._selected

    def select(self, selected=True):
        self._selected = selected
        return self

    def insertChild(self, index: int, child: "NotesTreeItem") -> "NotesTreeItem":
        if index < 0:
            index = 0
        if index > len(self._children):
            index = len(self._children)

        self._children.insert(index, child)
        return self

    def getChildren(self) -> List["NotesTreeItem"]:
        return self._children

    def _print(self):
        expand = "[-]" if self._expanded else "[+]"
        line = f"{'   ' * self._depth}{expand} {self._title} {self._line}"
        print(line)
        for child in self._children:
            child._print()


class _NotesTreeItemPositionCalculator:
    def __init__(self) -> None:
        self._line = 0

    def run(self, root_item: NotesTreeItem):
        root_item.setLine(self._line)
        self._line += 1
        if root_item.isExpanded():
            for item in root_item.getChildren():
                self.run(item)

    def getLastLine(self) -> int:
        return self._line


class _ItemsPainter:
    def __init__(self, window: wx.Window, dc: wx.PaintDC, lineHeight: int) -> None:
        self._window = window
        self._dc = dc

        # Sizes
        self._lineHeight = lineHeight
        self._iconHeight = ICON_HEIGHT
        self._indent = 16
        self._fontSize = 12
        self._linesGap = 3
        self._expandCtrlWidth = 8
        self._expandCtrlHeight = 8
        self._expandCtrlLeftGap = 3
        self._expandCtrlRightGap = 3

        # Colors
        self._back_color_normal = wx.WHITE
        self._back_color_selected = wx.BLUE
        self._font_color_normal = wx.BLACK
        self._font_color_selected = wx.WHITE

        # Pens, brushes etc
        self._back_brush_normal = wx.NullBrush
        self._back_brush_selected = wx.NullBrush
        self._back_pen_normal = wx.NullBrush
        self._back_pen_selected = wx.NullBrush
        self._title_font_normal = wx.NullFont
        self._title_font_selected = wx.NullFont

    def draw(self, item: NotesTreeItem, x, y):
        self._drawBackground(item, x, y)
        self._drawTitle(item, x, y)

    def _drawTitle(self, item: NotesTreeItem, x: int, y: int):
        if item.isSelected():
            self._dc.SetTextForeground(self._font_color_selected)
            self._dc.SetTextBackground(self._back_color_selected)
        else:
            self._dc.SetTextForeground(self._font_color_normal)
            self._dc.SetTextBackground(self._back_color_normal)

        self._dc.DrawText(item.getTitle(), x + self._indent * item.getDepth(), y)

    def _drawBackground(self, item: NotesTreeItem, x: int, y: int):
        width = self._window.GetClientSize()[0]
        if item.isSelected():
            self._dc.SetPen(self._back_pen_selected)
            self._dc.SetBrush(self._back_brush_selected)
        else:
            self._dc.SetPen(self._back_pen_normal)
            self._dc.SetBrush(self._back_brush_normal)

        self._dc.SetPen(wx.WHITE_PEN)
        self._dc.DrawRectangle(x, y, width, self._lineHeight)

    def __enter__(self):
        self._back_brush_normal = wx.Brush(self._back_color_normal)
        self._back_brush_selected = wx.Brush(self._back_color_selected)
        self._back_pen_normal = wx.Pen(self._back_color_normal)
        self._back_pen_selected = wx.Pen(self._back_color_selected)
        return self

    def __exit__(self, type, value, traceback):
        pass


class NotesTreeCtrl2(wx.ScrolledWindow):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self._lineHeight = ICON_HEIGHT + 6
        self.SetScrollRate(0, 0)

        self.defaultIcon = getBuiltinImagePath("page.svg")

        # Картинки для дерева
        self._iconsCache = ImageListCache(self.defaultIcon)

        # Кеш для страниц, чтобы было проще искать элемент дерева по странице
        # Словарь. Ключ - страница, значение - элемент дерева NotesTreeItem
        self._pageCache: Dict[BasePage, NotesTreeItem] = {}

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = "Expand"

        self._rootItems: List[NotesTreeItem] = []
        self._lineCount = 0

        self.Bind(wx.EVT_CLOSE, self._onClose)
        self.Bind(wx.EVT_PAINT, handler=self._onPaint)

    def _calculateItemsPositions(self):
        calculator = _NotesTreeItemPositionCalculator()
        for root_item in self._rootItems:
            calculator.run(root_item)

        self._updateScrollBars(calculator.getLastLine() + 1)

    def _updateScrollBars(self, linesCount):
        self.SetScrollbars(5, self._lineHeight, 0, linesCount, 0, 0)

    def _onPaint(self, event):
        with wx.PaintDC(self) as dc:
            with _ItemsPainter(self, dc, self._lineHeight) as painter:
                # back_color = self.GetBackgroundColour()
                # dc.SetBrush(wx.Brush(back_color))
                # dc.SetPen(wx.Pen(back_color))
                # width, height = self.GetClientSize()
                # dc.DrawRectangle(0, 0, width, height)

                # vbX, vbY = self.GetViewStart()
                # print(vbX, vbY)
                # upd = wx.RegionIterator(self.GetUpdateRegion())
                # while upd.HaveRects():
                #     rect = upd.GetRect()
                #     print(rect)
                #     # Repaint this rectangle
                #     # PaintRectangle(rect, dc)
                #     upd.Next()

                interval_x = self._getScrolledX()
                interval_y = self._getScrolledY()
                for root_item in self._rootItems:
                    self._paintTree(root_item, painter, interval_x, interval_y)
                    # root_item._print()

    def _getScrolledX(self) -> Tuple[int, int]:
        xmin = self.GetScrollPos(wx.HORIZONTAL) * self.GetScrollPixelsPerUnit()[0]
        xmax = xmin + self.GetClientSize()[0]
        return (xmin, xmax)

    def _getScrolledY(self) -> Tuple[int, int]:
        ymin = self.GetScrollPos(wx.VERTICAL) * self.GetScrollPixelsPerUnit()[1]
        ymax = ymin + self.GetClientSize()[1]
        return (ymin, ymax)

    def _paintTree(
        self,
        root_item: NotesTreeItem,
        painter: _ItemsPainter,
        interval_x: Tuple[int, int],
        interval_y: Tuple[int, int],
    ):
        x = 0
        y = root_item.getLine() * self._lineHeight
        if y >= interval_y[0] and y <= interval_y[1]:
            painter.draw(root_item, x, y - interval_y[0])

        if root_item.isExpanded():
            for item in root_item._children:
                self._paintTree(item, painter, interval_x, interval_y)

    def _onClose(self, event):
        self._iconsCache.clear()

    def _createRootNotesTreeItem(self, rootPage: WikiDocument) -> "NotesTreeItem":
        rootname = os.path.basename(rootPage.path)
        return NotesTreeItem(rootname, rootPage, None).setImageId(
            self._iconsCache.getDefaultImageId()
        )

    def _createNotesTreeItem(self, page: WikiPage) -> "NotesTreeItem":
        title = page.display_title
        parent_page = page.parent
        assert parent_page is not None

        parent_item = self._pageCache[parent_page]

        new_item = NotesTreeItem(title, page, parent_item).setImageId(self._loadIcon(page)).expand(self._getPageExpandState(page))

        return new_item

    def treeUpdate(self, rootPage):
        """
        Обновить дерево
        """
        self._iconsCache.clear()
        self._pageCache.clear()
        self._rootItems.clear()

        if rootPage is not None:
            root_item = self._createRootNotesTreeItem(rootPage)
            self._rootItems.append(root_item)
            self._pageCache[rootPage] = root_item
            self._appendChildren(rootPage)

            self.selectedPage = rootPage.selectedPage
            self.expand(rootPage)
            self._calculateItemsPositions()
            self.Update()

    def _appendChildren(self, parentPage):
        """
        Добавить детей в дерево
        parentPage - родительская страница, куда добавляем дочерние страницы
        """
        grandParentExpanded = self._getItemExpandState(parentPage.parent)

        if grandParentExpanded:
            for child in parentPage.children:
                if child not in self._pageCache:
                    self._insertChild(child)

        if self._getPageExpandState(parentPage):
            self.expand(parentPage)

    def _insertChild(self, childPage):
        """
        Вставить одну дочерниюю страницу (childPage) в ветвь
        """
        parentItem = self.getTreeItem(childPage.parent)
        assert parentItem is not None

        childItem = self._createNotesTreeItem(childPage)
        parentItem.insertChild(childPage.order, childItem)

        self._pageCache[childPage] = childItem
        self._appendChildren(childPage)

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
        pages = []
        currentPage = page.parent
        while currentPage is not None:
            pages.append(currentPage)
            currentPage = currentPage.parent

        pages.reverse()
        for page in pages:
            self.expand(page)
        self._calculateItemsPositions()
        self.Update()

    def expand(self, page):
        item = self.getTreeItem(page)
        if item is not None:
            item.expand()
        # self._calculateItemsPositions()
        # self.Update()

    def createPage(self, newpage):
        # if newpage.parent in self._pageCache:
        #     self.insertChild(newpage)

        #     assert newpage in self._pageCache
        #     item = self._pageCache[newpage]
        #     assert item.IsOk()

        #     self.expand(newpage)
        self._calculateItemsPositions()
        self.Update()

    @property
    def selectedPage(self) -> Optional[BasePage]:
        for page, item in self._pageCache.items():
            if item.isSelected():
                return page
        return None

    @selectedPage.setter
    def selectedPage(self, newSelectedPage: Optional[BasePage]):
        for page, item in self._pageCache.items():
            item.select(page is newSelectedPage)

        self._calculateItemsPositions()
        self.Update()
