# coding: utf-8

import logging
import os
from typing import Dict, Optional, List, Tuple

from outwiker.core.tree import BasePage, WikiDocument, WikiPage
import wx
import wx.lib.newevent

from outwiker.core.defines import ICON_HEIGHT
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache


NotesTreeSelChangedEvent, EVT_NOTES_TREE_SEL_CHANGED = wx.lib.newevent.NewEvent()

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
        self._iconImageId = -1
        self._extraImageIds: List[int] = []
        self._bold = False
        self._italic = False
        self._fontColor = wx.Colour(0, 0, 0)
        self._backColor = wx.Colour(0, 0, 0)
        self._expanded = False
        self._selected = False
        self._visible = False
        self._textWidth = 0

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

    def getIconImageId(self) -> int:
        return self._iconImageId

    def setIconImageId(self, imageId: int) -> "NotesTreeItem":
        self._iconImageId = imageId
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

    def getExtraImageIds(self) -> List[int]:
        return self._extraImageIds

    def isVisible(self) -> bool:
        return self._visible

    def setVisible(self, visible=True):
        self._visible = visible
        return self

    def getParent(self) -> Optional["NotesTreeItem"]:
        return self._parent

    def getTextWidth(self) -> int:
        return self._textWidth

    def setTextWidth(self, value) -> "NotesTreeItem":
        self._textWidth = value
        return self

    def getPage(self) -> BasePage:
        return self._page

    def _print_tree(self):
        expand = "[-]" if self._expanded else "[+]"
        line = f"{'   ' * self._depth}{expand} {self._title} {self._line}"
        print(line)
        for child in self._children:
            child._print_tree()

    def __repr__(self):
        return f"{self._title}"


class _NotesTreeItemPropertiesCalculator:
    def __init__(self, view_info: "_ItemsViewInfo") -> None:
        self._line = 0
        self._view_info = view_info

    def run(self, item: NotesTreeItem):
        parent = item.getParent()
        item.setLine(self._line)
        item.setVisible(parent is None or (parent.isVisible() and parent.isExpanded()))
        item.setTextWidth(self._view_info.getTextWidth(item.getTitle()))
        self._line += 1
        if item.isExpanded():
            for item in item.getChildren():
                self.run(item)

    def getLastLine(self) -> int:
        return self._line


class _ItemsViewInfo:
    def __init__(self, window: wx.Window) -> None:
        self._window = window

        # Sizes
        self.left_margin = 4
        self.top_margin = 4
        self.line_height = ICON_HEIGHT + 6
        self.icon_height = ICON_HEIGHT
        self.icon_width = ICON_HEIGHT
        self.font_size = 10
        # self.vline_left_margin = self.icon_width // 2
        self.depth_indent = self.icon_width // 2 + 16
        self.icon_left_margin = 8
        self.extra_icons_left_margin = 3
        self.title_left_margin = 8
        self.title_right_margin = 4
        self.expand_ctrl_width = 8
        self.expand_ctrl_height = 8
        # self.expand_ctrl_center_x = self.vline_left_margin

        # Colors
        self.back_color_normal = wx.WHITE
        self.back_color_selected = wx.BLUE
        self.font_color_normal = wx.BLACK
        self.font_color_selected = wx.WHITE
        self.lines_color = wx.BLACK

        self._dc = wx.ClientDC(self._window)
        self._title_font = wx.Font(wx.FontInfo(self.font_size))
        self._dc.SetFont(self._title_font)

    def getTextWidth(self, text: str) -> int:
        return self._dc.GetTextExtent(text).GetWidth()

    def getTitleLeft(self, item: NotesTreeItem) -> int:
        return self.getExtraIconsRight(item) + self.title_left_margin

    def getIconLeft(self, item: NotesTreeItem) -> int:
        return self.left_margin + item.getDepth() * self.depth_indent

    def getIconCenter(self, item: NotesTreeItem) -> int:
        return self.getIconLeft(item) + self.icon_width // 2

    def getExtraIconsLeft(self, item) -> int:
        return self.getIconLeft(item) + self.icon_width + self.extra_icons_left_margin

    def getSelectionLeft(self, item: NotesTreeItem) -> int:
        return self.getExtraIconsRight(item) + self.title_left_margin // 2

    def getSelectionWidth(self, item: NotesTreeItem):
        return (
            (self.title_left_margin // 2)
            + self.getTextWidth(item.getTitle())
            + self.title_right_margin
        )

    def getSelectionRight(self, item: NotesTreeItem) -> int:
        return self.getSelectionLeft(item) + self.getSelectionWidth(item)

    def getExtraIconsRight(self, item: NotesTreeItem) -> int:
        return (
            self.getIconLeft(item)
            + self.icon_width
            + (self.extra_icons_left_margin + self.icon_width)
            * self._getExtraIconsCount(item)
        )

    def getItemTop(self, item: NotesTreeItem) -> int:
        return item.getLine() * self.line_height + self.top_margin

    def getItemBottom(self, item: NotesTreeItem) -> int:
        return self.getItemTop(item) + self.line_height

    def getItemCenterVertical(self, item: NotesTreeItem) -> int:
        return (self.getItemTop(item) + self.getItemBottom(item)) // 2

    def isPointInItem(self, item: NotesTreeItem, x, y) -> bool:
        top = self.getItemTop(item)
        bottom = self.getItemBottom(item)
        left = self.getIconLeft(item)
        right = self.getSelectionRight(item)
        return y >= top and y <= bottom and x >= left and x <= right

    def _getExtraIconsCount(self, item: NotesTreeItem) -> int:
        return len(item.getExtraImageIds())


class _ItemsPainter:
    def __init__(
        self,
        window: wx.Window,
        dc: wx.PaintDC,
        image_list: wx.ImageList,
        view_info: _ItemsViewInfo,
    ) -> None:
        self._window = window
        self._dc = dc
        self._image_list = image_list
        self._view_info = view_info

        # Pens, brushes etc
        self._back_brush_normal = wx.NullBrush
        self._back_brush_selected = wx.NullBrush
        self._back_pen_normal = wx.NullBrush
        self._back_pen_selected = wx.NullBrush
        self._title_font_normal = wx.NullFont
        self._title_font_selected = wx.NullFont
        self._tree_line_pen = wx.NullPen
        self._text_height = None

    def __enter__(self):
        self._back_brush_normal = wx.Brush(self._view_info.back_color_normal)
        self._back_brush_selected = wx.Brush(self._view_info.back_color_selected)
        self._back_pen_normal = wx.Pen(self._view_info.back_color_normal)
        self._back_pen_selected = wx.Pen(self._view_info.back_color_selected)
        self._title_font_normal = wx.Font(wx.FontInfo(self._view_info.font_size))
        self._title_font_selected = wx.Font(wx.FontInfo(self._view_info.font_size))
        self._tree_line_pen = wx.Pen(self._view_info.lines_color, style=wx.PENSTYLE_DOT)
        self._dc.SetFont(self._title_font_normal)
        self._text_height = self._dc.GetTextExtent("W").GetHeight()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def draw(self, item: NotesTreeItem, x, y):
        if item.isVisible():
            self._drawSelection(item, x, y)
            self._drawIcon(item, x, y)
            self._drawTitle(item, x, y)

    def fillBackground(self):
        back_color = self._view_info.back_color_normal
        self._dc.SetBrush(wx.Brush(back_color))
        self._dc.SetPen(wx.Pen(back_color))
        width, height = self._window.GetClientSize()
        self._dc.DrawRectangle(0, 0, width, height)

    def drawTreeLines(self, item: NotesTreeItem, x: int, y: int):
        parentItem = item.getParent()
        if parentItem is None:
            return
        left = self._view_info.getIconCenter(parentItem) + x
        right = self._view_info.getIconLeft(item) + x
        top = self._view_info.getItemBottom(parentItem) + y
        centerV = self._view_info.getItemCenterVertical(item) + y
        points = [(left, top, left, centerV), (left, centerV, right, centerV)]
        self._dc.DrawLineList(points, pens=self._tree_line_pen)

    def _drawTitle(self, item: NotesTreeItem, x: int, y: int):
        if item.isSelected():
            self._dc.SetTextForeground(self._view_info.font_color_selected)
            self._dc.SetTextBackground(self._view_info.back_color_selected)
            self._dc.SetFont(self._title_font_selected)
        else:
            self._dc.SetTextForeground(self._view_info.font_color_normal)
            self._dc.SetTextBackground(self._view_info.back_color_normal)
            self._dc.SetFont(self._title_font_normal)

        title_x = self._view_info.getTitleLeft(item) + x
        top = self._view_info.getItemTop(item) + (self._view_info.line_height - self._text_height) // 2 + y
        self._dc.DrawText(item.getTitle(), title_x, top)

    def _drawSelection(self, item: NotesTreeItem, x: int, y: int):
        if not item.isSelected():
            return

        self._dc.SetPen(self._back_pen_selected)
        self._dc.SetBrush(self._back_brush_selected)

        left = self._view_info.getSelectionLeft(item)
        width = self._view_info.getSelectionWidth(item)
        self._dc.DrawRectangle(x + left, self._view_info.getItemTop(item) + y, width, self._view_info.line_height)

    def _drawIcon(self, item: NotesTreeItem, x: int, y: int):
        bitmap = self._image_list.GetBitmap(item.getIconImageId())
        left = self._view_info.getIconLeft(item) + x
        top = self._view_info.getItemTop(item) + (self._view_info.line_height - self._view_info.icon_height) // 2 + y
        self._dc.DrawBitmap(bitmap, left, top)


class NotesTreeCtrl2(wx.ScrolledWindow):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self._view_info = _ItemsViewInfo(parent)
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

        self.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftButtonDown)
        self.Bind(wx.EVT_LEFT_UP, handler=self._onLeftButtonUp)
        self.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightButtonDown)
        self.Bind(wx.EVT_RIGHT_UP, handler=self._onRightButtonUp)
        self.Bind(wx.EVT_LEFT_DCLICK, handler=self._onLeftDblClick)

    def _getVisibleItems(self) -> List[NotesTreeItem]:
        return [item for item in self._pageCache.values() if item.isVisible()]

    def _onLeftButtonDown(self, event):
        x = event.GetX() + self._getScrollX()
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if item is not None:
            isPointInItem = self._view_info.isPointInItem(item, x, y)
            if isPointInItem:
                oldSelectedItem = self._getSelectedItem()
                if oldSelectedItem is not None:
                    oldSelectedItem.select(False)
                item.select()
                self.Refresh()
                event = NotesTreeSelChangedEvent(page=item.getPage())
                wx.PostEvent(self.GetParent(), event)

    def _onLeftButtonUp(self, event):
        pass

    def _onRightButtonDown(self, event):
        # item = self._getItemByY(event.GetY())
        # if item is not None:
        #     isPointInItem = self._view_info.isPointInItem(
        #         item, event.GetX(), event.GetY()
        #     )
        #     if isPointInItem:
        #         print(item)
        pass

    def _onRightButtonUp(self, event):
        pass

    def _onLeftDblClick(self, event):
        pass

    def _getItemByY(self, y: int) -> Optional[NotesTreeItem]:
        for item in self._pageCache.values():
            y_min = self._view_info.getItemTop(item)
            y_max = self._view_info.getItemBottom(item)
            if y >= y_min and y <= y_max:
                return item

        return None

    def _calculateItemsProperties(self):
        calculator = _NotesTreeItemPropertiesCalculator(self._view_info)
        for root_item in self._rootItems:
            calculator.run(root_item)

        widths = [
            self._view_info.getTitleLeft(item)
            + item.getTextWidth()
            + self._view_info.title_right_margin
            for item in self._getVisibleItems()
        ]
        max_width = max(widths)
        self.SetScrollbars(
            1,
            self._view_info.line_height,
            max_width,
            calculator.getLastLine() + 1,
            0,
            0,
        )

    def _onPaint(self, event):
        with wx.PaintDC(self) as dc:
            with _ItemsPainter(
                self, dc, self._iconsCache.getImageList(), self._view_info
            ) as painter:
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
                painter.fillBackground()
                for item in self._pageCache.values():
                    x = -interval_x[0]
                    y = -interval_y[0]
                    item_top = self._view_info.getItemTop(item)
                    if item.isVisible():
                        painter.drawTreeLines(item, x, y)

                        if item_top >= interval_y[0] and item_top <= interval_y[1]:
                            painter.draw(item, x, y)

    def _getScrolledX(self) -> Tuple[int, int]:
        xmin = self._getScrollX()
        xmax = xmin + self.GetClientSize()[0]
        return (xmin, xmax)

    def _getScrolledY(self) -> Tuple[int, int]:
        ymin = self._getScrollY()
        ymax = ymin + self.GetClientSize()[1]
        return (ymin, ymax)

    def _getScrollX(self) -> int:
        return self.GetScrollPos(wx.HORIZONTAL) * self.GetScrollPixelsPerUnit()[0]

    def _getScrollY(self) -> int:
        return self.GetScrollPos(wx.VERTICAL) * self.GetScrollPixelsPerUnit()[1]

    def _onClose(self, event):
        self._iconsCache.clear()

    def _createRootNotesTreeItem(self, rootPage: WikiDocument) -> "NotesTreeItem":
        rootname = os.path.basename(rootPage.path)
        return (
            NotesTreeItem(rootname, rootPage, None)
            .setIconImageId(self._iconsCache.getDefaultImageId())
            .setVisible()
        )

    def _createNotesTreeItem(self, page: WikiPage) -> "NotesTreeItem":
        title = page.display_title
        parent_page = page.parent
        assert parent_page is not None

        parent_item = self._pageCache[parent_page]

        new_item = (
            NotesTreeItem(title, page, parent_item)
            .setIconImageId(self._loadIcon(page))
            .expand(self._getPageExpandState(page))
        )

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
            self._updateItems()

    def _updateItems(self):
        self._calculateItemsProperties()
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
        self._updateItems()

    def expand(self, page):
        item = self.getTreeItem(page)
        if item is not None:
            item.expand()
        self._updateItems()

    def createPage(self, newpage):
        # if newpage.parent in self._pageCache:
        #     self.insertChild(newpage)

        #     assert newpage in self._pageCache
        #     item = self._pageCache[newpage]
        #     assert item.IsOk()

        #     self.expand(newpage)
        self._updateItems()

    def _getSelectedItem(self) -> Optional[NotesTreeItem]:
        for item in self._pageCache.values():
            if item.isSelected():
                return item
        return None

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

        self._updateItems()
