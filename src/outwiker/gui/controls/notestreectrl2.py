# coding: utf-8

import logging
import os
from typing import Dict, Optional, List, Tuple

from outwiker.core.tree import BasePage, WikiPage
import wx
import wx.lib.newevent

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.imagelistcache import ImageListCache
from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT


NotesTreeSelChangedEvent, EVT_NOTES_TREE_SEL_CHANGED = wx.lib.newevent.NewEvent()
NotesTreeItemExpandChangedEvent, EVT_NOTES_TREE_EXPAND_CHANGED = (
    wx.lib.newevent.NewEvent()
)
NotesTreeRightButtonUpEvent, EVT_NOTES_TREE_RIGHT_BUTTON_UP = wx.lib.newevent.NewEvent()
NotesTreeMiddleButtonUpEvent, EVT_NOTES_TREE_MIDDLE_BUTTON_UP = (
    wx.lib.newevent.NewEvent()
)
NotesTreeItemActivateEvent, EVT_NOTES_TREE_ITEM_ACTIVATE = wx.lib.newevent.NewEvent()
NotesTreeEndItemEditEvent, EVT_NOTES_TREE_END_ITEM_EDIT = wx.lib.newevent.NewEvent()
NotesTreeDropItemEvent, EVT_NOTES_TREE_DROP_ITEM = wx.lib.newevent.NewEvent()

logger = logging.getLogger("outwiker.gui.controls.notestreectrl2")


class NotesTreeItem:
    def __init__(self, page: BasePage) -> None:
        self._title = ""
        self._page = page
        self._parent: Optional["NotesTreeItem"] = None
        self._depth = 0
        self._line = 0
        self._children: List["NotesTreeItem"] = []
        self._iconImageId = -1
        self._extraImageIds: List[int] = []
        self._bold = False
        self._italic = False
        self._fontColor = None
        self._backColor = None
        self._italic = False
        self._bold = False
        self._expanded = False
        self._selected = False
        self._visible = False
        self._textWidth = 0
        self._dropHovered = False
        self._hovered = False

    def getTitle(self) -> str:
        return self._title

    def setTitle(self, value) -> "NotesTreeItem":
        self._title = value
        return self

    def getDepth(self) -> int:
        return self._depth

    def getLine(self) -> int:
        return self._line

    def setLine(self, line: int) -> "NotesTreeItem":
        self._line = line
        return self

    def addChild(self, child: "NotesTreeItem") -> "NotesTreeItem":
        self._children.append(child)
        child.setParent(self)
        return self

    def getChildren(self) -> List["NotesTreeItem"]:
        return sorted(self._children, key=lambda item: item.getPage().order)

    def getChildrenCount(self) -> int:
        return len(self._children)

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

    def getExtraImageIds(self) -> List[int]:
        return self._extraImageIds

    def isVisible(self) -> bool:
        return self._visible

    def setVisible(self, visible=True):
        self._visible = visible
        return self

    def getParent(self) -> Optional["NotesTreeItem"]:
        return self._parent

    def setParent(self, parent: Optional["NotesTreeItem"]) -> "NotesTreeItem":
        self._parent = parent
        self._depth = parent.getDepth() + 1 if parent is not None else 0
        return self

    def getTextWidth(self) -> int:
        return self._textWidth

    def setTextWidth(self, value) -> "NotesTreeItem":
        self._textWidth = value
        return self

    def getPage(self) -> BasePage:
        return self._page

    def hasChildren(self):
        return bool(self._children)

    def isItalic(self):
        return self._italic

    def setItalic(self, italic=True) -> "NotesTreeItem":
        self._italic = italic
        return self

    def isBold(self):
        return self._bold

    def setBold(self, bold=True) -> "NotesTreeItem":
        self._bold = bold
        return self

    def isDropHovered(self) -> bool:
        return self._dropHovered

    def setDropHovered(self, hovered: bool) -> "NotesTreeItem":
        self._dropHovered = hovered
        return self

    def isHovered(self) -> bool:
        return self._hovered

    def setHovered(self, hovered: bool) -> "NotesTreeItem":
        self._hovered = hovered
        return self

    def _print_tree(self):
        expand = "[-]" if self._expanded else "[+]"
        line = f"{'   ' * self._depth}{expand} {self._title} {self._line} {self._visible=} {self._parent=}"
        if self.isVisible():
            print(line)
            for child in self._children:
                child._print_tree()

    def __repr__(self):
        return f"{self._title}"


class _NotesTreeItemPropertiesCalculator:
    def __init__(self, view_info: "_ItemsViewInfo") -> None:
        self._line = 0
        self._view_info = view_info
        self._visibleItems: List[NotesTreeItem] = []

    def run(self, item: NotesTreeItem):
        parent = item.getParent()
        visible = parent is None or (parent.isVisible() and parent.isExpanded())
        item.setVisible(visible)

        if visible:
            item.setLine(self._line)
            item.setTextWidth(self._view_info.getTextWidth(item.getTitle()))
            self._line += 1
            self._visibleItems.append(item)
        for item in item.getChildren():
            self.run(item)

    def getLastLine(self) -> int:
        return self._line

    def getVisibleItems(self) -> List[NotesTreeItem]:
        return self._visibleItems


class _ItemsViewInfo:
    def __init__(self, window: wx.Window) -> None:
        self._window = window

        # Sizes
        self.left_margin = 4
        self.top_margin = 4
        self.icon_height = ICONS_HEIGHT
        self.line_height = self.icon_height + 10
        self.icon_width = ICONS_WIDTH
        self.font_size = wx.SystemSettings.GetFont(
            wx.SYS_DEFAULT_GUI_FONT
        ).GetPointSize()
        self.depth_indent = self.icon_width // 2 + 16
        self.icon_left_margin = 8
        self.extra_icons_left_margin = 3
        self.title_left_margin = 8
        self.title_right_margin = 4
        self.expand_ctrl_width = 11
        self.expand_ctrl_height = 11
        self.selection_margin_vertical = 2

        # Colors
        self.back_color = window.GetBackgroundColour()
        self.fore_color = window.GetForegroundColour()

        self.back_color_normal = self.back_color
        self.back_color_selected = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        # self.back_color_hovered = wx.Colour(230, 243, 255)
        self.back_color_hovered = wx.Colour(self.back_color_selected.GetRed(),
                                            self.back_color_selected.GetGreen(),
                                            self.back_color_selected.GetBlue(), 30)

        self.font_color_normal = self.fore_color
        self.font_color_selected = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.lines_color = self.fore_color
        # self.drop_hover_color = wx.Colour(128, 193, 255)
        self.drop_hover_color = wx.Colour(self.back_color_selected.GetRed(),
                                          self.back_color_selected.GetGreen(),
                                          self.back_color_selected.GetBlue(), 100)

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

    def getSelectionWidth(self, item: NotesTreeItem) -> int:
        return (
            (self.title_left_margin // 2)
            + self.getTextWidth(item.getTitle())
            + self.title_right_margin
        )

    def getSelectionHeight(self, item: NotesTreeItem) -> int:
        return self.getSelectionBottom(item) - self.getSelectionTop(item)

    def getSelectionRight(self, item: NotesTreeItem) -> int:
        return self.getSelectionLeft(item) + self.getSelectionWidth(item)

    def getSelectionTop(self, item: NotesTreeItem) -> int:
        return self.getItemTop(item) + self.selection_margin_vertical

    def getSelectionBottom(self, item: NotesTreeItem) -> int:
        return self.getItemBottom(item) - self.selection_margin_vertical

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

    def isPointInSelection(self, item: NotesTreeItem, x, y) -> bool:
        top = self.getSelectionTop(item)
        bottom = self.getSelectionBottom(item)
        left = self.getSelectionLeft(item)
        right = self.getSelectionRight(item)
        return y >= top and y <= bottom and x >= left and x <= right

    def isPointInItem(self, item: NotesTreeItem, x, y) -> bool:
        top = self.getItemTop(item)
        bottom = self.getItemBottom(item)
        left = self.getIconLeft(item)
        right = self.getSelectionRight(item)
        return y >= top and y <= bottom and x >= left and x <= right

    def isPointInExpandCtrl(self, item: NotesTreeItem, x, y) -> bool:
        top = self.getExpandCtrlTop(item)
        bottom = self.getExpandCtrlBottom(item)
        left = self.getExpandCtrlLeft(item)
        right = self.getExpandCtrlRight(item)
        return y >= top and y <= bottom and x >= left and x <= right

    def _getExtraIconsCount(self, item: NotesTreeItem) -> int:
        return len(item.getExtraImageIds())

    def getTreeGridLeft(self, item: NotesTreeItem) -> int:
        return self.getIconLeft(item) - self.depth_indent + self.icon_width // 2

    def getExpandCtrlLeft(self, item: NotesTreeItem) -> int:
        return self.getTreeGridLeft(item) - self.expand_ctrl_width // 2

    def getExpandCtrlRight(self, item: NotesTreeItem) -> int:
        return self.getTreeGridLeft(item) + self.expand_ctrl_width // 2

    def getExpandCtrlTop(self, item: NotesTreeItem) -> int:
        return self.getItemCenterVertical(item) - self.expand_ctrl_height // 2

    def getExpandCtrlBottom(self, item: NotesTreeItem) -> int:
        return self.getItemCenterVertical(item) + self.expand_ctrl_height // 2


class _ItemsPainter:
    def __init__(
        self,
        window: wx.Window,
        dc: wx.DC,
        image_list: wx.ImageList,
        view_info: _ItemsViewInfo,
    ) -> None:
        self._window = window
        self._dc = dc
        self._image_list = image_list
        self._view_info = view_info
        self._gc = wx.GraphicsContext.Create(dc)

        self._expand_ctrl_images = SafeImageList(
            self._view_info.expand_ctrl_width, self._view_info.expand_ctrl_height
        )
        self._expanded_img = self._expand_ctrl_images.AddFromFile(
            getBuiltinImagePath("expanded.svg")
        )
        self._collapsed_img = self._expand_ctrl_images.AddFromFile(
            getBuiltinImagePath("collapsed.svg")
        )

        # Pens, brushes etc
        self._back_brush_normal = wx.NullBrush
        self._back_brush_selected = wx.NullBrush
        self._back_brush_hovered = wx.NullBrush

        self._back_pen_normal = wx.NullBrush
        self._back_pen_selected = wx.NullBrush
        self._back_pen_hovered = wx.NullBrush

        self._title_font_normal = wx.NullFont
        self._title_font_selected = wx.NullFont

        self._tree_line_pen = wx.NullPen
        self._drop_hover_pen = wx.NullPen
        self._drop_hover_brush = wx.NullBrush
        self._text_height = None

    def __enter__(self):
        self._back_brush_normal = wx.Brush(self._view_info.back_color_normal)
        self._back_brush_selected = wx.Brush(self._view_info.back_color_selected)
        self._back_brush_hovered = wx.Brush(self._view_info.back_color_hovered)

        self._back_pen_normal = wx.Pen(self._view_info.back_color_normal)
        self._back_pen_selected = wx.Pen(self._view_info.back_color_selected)
        self._back_pen_hovered = wx.Pen(self._view_info.back_color_hovered)

        self._drop_hover_pen = wx.Pen(self._view_info.drop_hover_color, style=wx.PENSTYLE_SOLID)
        self._drop_hover_brush = wx.Brush(self._view_info.drop_hover_color)

        self._title_font_normal = wx.Font(wx.FontInfo(self._view_info.font_size))
        self._title_font_selected = wx.Font(wx.FontInfo(self._view_info.font_size))

        self._tree_line_pen = wx.Pen(self._view_info.lines_color, style=wx.PENSTYLE_DOT)

        self._dc.SetFont(self._title_font_normal)
        self._text_height = self._dc.GetTextExtent("W").GetHeight()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def draw(self, item: NotesTreeItem, dx, dy):
        if item.isVisible():
            self._drawBackground(item, dx, dy)
            self._drawSelection(item, dx, dy)
            self._drawIcon(item, dx, dy)
            self._drawTitle(item, dx, dy)
            # self._drawDropHover(item, dx, dy)
            self._drawExpandCtrl(item, dx, dy)

    def fillBackground(self):
        back_color = self._view_info.back_color_normal
        self._dc.SetBrush(wx.Brush(back_color))
        self._dc.SetPen(wx.Pen(back_color))
        width, height = self._window.GetClientSize()
        self._dc.DrawRectangle(0, 0, width, height)

    def drawTreeLines(self, item: NotesTreeItem, dx: int, dy: int):
        parentItem = item.getParent()
        if parentItem is None:
            return

        left = self._view_info.getTreeGridLeft(item) + dx
        right = self._view_info.getIconLeft(item) + dx
        top = self._view_info.getItemBottom(parentItem) + dy
        if top < 0:
            top = 0
        centerV = self._view_info.getItemCenterVertical(item) + dy
        points = [(left, top, left, centerV), (left, centerV, right, centerV)]
        self._dc.DrawLineList(points, pens=self._tree_line_pen)

    def _drawExpandCtrl(self, item: NotesTreeItem, dx, dy):
        if item.getChildren():
            left = self._view_info.getExpandCtrlLeft(item) + dx
            top = self._view_info.getExpandCtrlTop(item) + dy
            bitmap = self._expand_ctrl_images.GetBitmap(
                self._expanded_img if item.isExpanded() else self._collapsed_img
            )
            self._dc.DrawBitmap(bitmap, left, top)

    def _drawTitle(self, item: NotesTreeItem, dx: int, dy: int):
        current_font = (
            self._title_font_selected if item.isSelected() else self._title_font_normal
        )
        current_font.SetStyle(
            wx.FONTSTYLE_ITALIC if item.isItalic() else wx.FONTSTYLE_NORMAL
        )
        current_font.SetWeight(
            wx.FONTWEIGHT_BOLD if item.isBold() else wx.FONTWEIGHT_NORMAL
        )

        if item.isSelected():
            self._dc.SetTextForeground(self._view_info.font_color_selected)
            self._dc.SetTextBackground(self._view_info.back_color_selected)
        else:
            self._dc.SetTextForeground(self._view_info.font_color_normal)
            self._dc.SetTextBackground(self._view_info.back_color_normal)

        self._dc.SetFont(current_font)

        title_x = self._view_info.getTitleLeft(item) + dx
        top = (
            self._view_info.getItemTop(item)
            + (self._view_info.line_height - self._text_height) // 2
            + dy
        )
        self._dc.DrawText(item.getTitle(), title_x, top)

    # def _drawDropHover(self, item: NotesTreeItem, dx: int, dy: int):
    #     if item.isDropHovered():
    #         left = self._view_info.getIconLeft(item) + dx
    #         right = self._view_info.getSelectionRight(item) + dx
    #         top = self._view_info.getSelectionTop(item) + dy
    #         bottom = self._view_info.getSelectionBottom(item) + dy
    #         self._gc.SetBrush(self._drop_hover_brush)
    #         self._gc.SetPen(self._drop_hover_pen)
    #         self._gc.DrawRectangle(left, top, right - left, bottom - top)

    def _drawBackground(self, item: NotesTreeItem, dx: int, dy: int):
        left = self._view_info.getIconLeft(item) + dx
        right = self._view_info.getSelectionRight(item) + dx
        top = self._view_info.getSelectionTop(item) + dy
        bottom = self._view_info.getSelectionBottom(item) + dy

        if item.isHovered():
            self._gc.SetBrush(self._back_brush_hovered)
            self._gc.SetPen(self._back_pen_hovered)
        elif item.isDropHovered():
            self._gc.SetBrush(self._drop_hover_brush)
            self._gc.SetPen(self._drop_hover_pen)
        else:
            self._gc.SetBrush(self._back_brush_normal)
            self._gc.SetPen(self._back_pen_normal)

        self._gc.DrawRectangle(left, top, right - left, bottom - top)

    def _drawSelection(self, item: NotesTreeItem, dx: int, dy: int):
        if not item.isSelected():
            return

        self._dc.SetPen(self._back_pen_selected)
        self._dc.SetBrush(self._back_brush_selected)

        left = self._view_info.getSelectionLeft(item)
        width = self._view_info.getSelectionWidth(item)
        height = self._view_info.getSelectionHeight(item)
        self._dc.DrawRectangle(
            dx + left,
            self._view_info.getSelectionTop(item) + dy,
            width,
            height,
        )

    def _drawIcon(self, item: NotesTreeItem, dx: int, dy: int):
        bitmap = self._image_list.GetBitmap(item.getIconImageId())
        left = self._view_info.getIconLeft(item) + dx
        top = (
            self._view_info.getItemTop(item)
            + (self._view_info.line_height - self._view_info.icon_height) // 2
            + dy
        )
        self._dc.DrawBitmap(bitmap, left, top)


class NotesTreeCtrl2(wx.ScrolledWindow):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)
        self._view_info = _ItemsViewInfo(self)

        self.defaultIcon = getBuiltinImagePath("page.svg")

        # Картинки для дерева
        self._iconsCache = ImageListCache(self.defaultIcon,
                                          self._view_info.icon_width,
                                          self._view_info.icon_height)

        # Кеш для страниц, чтобы было проще искать элемент дерева по странице
        # Словарь. Ключ - страница, значение - элемент дерева NotesTreeItem
        self._pageCache: Dict[BasePage, NotesTreeItem] = {}
        self._visibleItems: List[NotesTreeItem] = []

        self._dropHoveredItem: Optional[NotesTreeItem] = None
        self._hoveredItem: Optional[NotesTreeItem] = None

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = "Expand"

        self._rootItems: List[NotesTreeItem] = []
        self._lineCount = 0

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # Scroll speed
        self._mouseWheelDeltaX = 3
        self._mouseWheelDeltaY = 3

        # Rename items
        self._editItemFont = wx.Font()
        self._editItemFont.SetPointSize(self._view_info.font_size)

        self._editItemTextCtrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self._editItemTextCtrl.Hide()
        self._editItemTextCtrl.SetFont(self._editItemFont)
        self._currentEditItem: Optional[NotesTreeItem] = None
        self._editClickDelay_ms = 300
        self._editItemCencelled = False
        self._editItemTimer = wx.Timer()

        # Rename items event handlers
        self._editItemTextCtrl.Bind(wx.EVT_TEXT_ENTER, handler=self._onEditItemEnter)
        self._editItemTextCtrl.Bind(wx.EVT_CHAR, handler=self._onEditItemChar)
        self._editItemTextCtrl.Bind(wx.EVT_KILL_FOCUS, handler=self._onEditItemComplete)
        self._editItemTimer.Bind(wx.EVT_TIMER, handler=self._onEditTimer)

        # Drag items
        self._dragItem: Optional[NotesTreeItem] = None
        self._dragMode = False
        self._mouseLeftDownXY: Optional[Tuple[int, int]] = None

        # Misc event handlers
        self.Bind(wx.EVT_CLOSE, self._onClose)
        self.Bind(wx.EVT_PAINT, handler=self._onPaint)

        # Items mouse events
        self.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftButtonDown)
        self.Bind(wx.EVT_LEFT_UP, handler=self._onLeftButtonUp)
        self.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightButtonDown)
        self.Bind(wx.EVT_RIGHT_UP, handler=self._onRightButtonUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleButtonDown)
        self.Bind(wx.EVT_MIDDLE_UP, handler=self._onMiddleButtonUp)
        self.Bind(wx.EVT_LEFT_DCLICK, handler=self._onLeftDblClick)
        self.Bind(wx.EVT_MOTION, handler=self._onMouseMove)
        self.Bind(wx.EVT_MOUSEWHEEL, handler=self._onMouseWheel)

    def _updateViewInfo(self):
        self._view_info = _ItemsViewInfo(self)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self._updateViewInfo()

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self._updateViewInfo()

    # Used in tests only
    def getRootItem(self, n: int) -> NotesTreeItem:
        return self._rootItems[n]

    # Used in tests only
    def getTreeItem(self, page: WikiPage) -> Optional[NotesTreeItem]:
        return self._pageCache.get(page)

    def pageInTree(self, page: Optional[WikiPage]) -> bool:
        return page in self._pageCache

    def isExpanded(self, page: Optional[BasePage]) -> bool:
        if page is None:
            return True

        item = self._pageCache.get(page)
        return item is not None and item.isExpanded()

    def _onMouseWheel(self, event):
        event.StopPropagation()
        scroll_x_src, scroll_y_src = self.GetViewStart()

        delta_x = 0
        delta_y = 0

        if event.GetModifiers() & wx.MOD_SHIFT:
            delta_x = self._mouseWheelDeltaX
            if event.GetWheelRotation() > 0:
                delta_x *= -1
        else:
            delta_y = self._mouseWheelDeltaY
            if event.GetWheelRotation() > 0:
                delta_y *= -1

        scroll_x = scroll_x_src + delta_x
        scroll_y = scroll_y_src + delta_y
        if scroll_x < 0:
            scroll_x = 0

        if scroll_y < 0:
            scroll_y = 0

        self.Scroll(scroll_x, scroll_y)

    def _onEditTimer(self, event):
        self._editItemTimer.Stop()
        if not self._editItemCencelled:
            item = self._getSelectedItem()
            if item is not None:
                self._beginItemEdit(item)

    def _onExpandCollapseItem(self, item):
        page = item.getPage()
        expanded = not item.isExpanded()
        self.expand(page, expanded, True)

    def _onSelectItem(
        self, item: NotesTreeItem, oldSelectedItem: Optional[NotesTreeItem]
    ):
        if oldSelectedItem is not None:
            oldSelectedItem.select(False)
        item.select()
        self.Refresh()
        event = NotesTreeSelChangedEvent(page=item.getPage())
        wx.PostEvent(self, event)

    def _onEditItemEnter(self, event):
        self._completeItemEdit()

    def _onEditItemComplete(self, event):
        self._completeItemEdit()

    def _onEditItemChar(self, event):
        keycode = event.GetUnicodeKey()
        if keycode == wx.WXK_ESCAPE:
            self._cancelItemEdit()

        event.Skip()

    def _resetDragMode(self):
        if self._dropHoveredItem is not None:
            self._dropHoveredItem.setDropHovered(False)
            self._refreshItem(self._dropHoveredItem)

        self._dragMode = False
        self._mouseLeftDownXY = None
        self._dragItem = None
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def _dropItem(self, srcItem: NotesTreeItem, destItem: NotesTreeItem):
        order: Optional[int] = None
        event = NotesTreeDropItemEvent(
            srcPage=srcItem.getPage(), destPage=destItem.getPage(), order=order
        )
        wx.PostEvent(self, event)
        self._resetDragMode()

    def _onMouseMove(self, event):
        event.Skip()
        if self._processMoveDragMode(event):
            return

        self._processMove(event)

    def _processMove(self, event):
        x = event.GetX() + self._getScrollX()
        y = event.GetY() + self._getScrollY()
        oldHoveredItem = self._hoveredItem
        self._hoveredItem = self._getItemByXY(x, y)
        if oldHoveredItem is not self._hoveredItem:
            if oldHoveredItem is not None:
                oldHoveredItem.setHovered(False)
                self._refreshItem(oldHoveredItem)
            if self._hoveredItem is not None:
                self._hoveredItem.setHovered(True)
                self._refreshItem(self._hoveredItem)

    def _processMoveDragMode(self, event):
        if self._dragItem is not None and event.LeftIsDown():
            self._dragMode = True
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            if not self.HasCapture():
                self.CaptureMouse()

        if self._dragMode:
            y = event.GetY() + self._getScrollY()
            oldHoveredItem = self._dropHoveredItem
            self._dropHoveredItem = self._getItemByY(y)

            if oldHoveredItem is not self._dropHoveredItem:
                if oldHoveredItem is not None:
                    oldHoveredItem.setDropHovered(False)
                    self._refreshItem(oldHoveredItem)
                if self._dropHoveredItem is not None and self._dragItem is not self._dropHoveredItem:
                    self._dropHoveredItem.setDropHovered(True)
                    self._refreshItem(self._dropHoveredItem)
        return self._dragMode

    def _onLeftButtonDown(self, event):
        self._completeItemEdit()
        x = event.GetX() + self._getScrollX()
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if item is None:
            return

        if item.hasChildren() and self._view_info.isPointInExpandCtrl(item, x, y):
            self._onExpandCollapseItem(item)
            return

        if self._view_info.isPointInItem(item, x, y):
            self._mouseLeftDownXY = (x, y)
            self._dragItem = item
            self._dragMode = False

    def _onLeftButtonUp(self, event):
        self._completeItemEdit()
        x = event.GetX() + self._getScrollX()
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if self.HasCapture():
            self.ReleaseMouse()

        if item is None:
            self._resetDragMode()
            return

        if self._dragMode:
            assert self._dragItem is not None
            self._dropItem(self._dragItem, item)
            self._resetDragMode()
            return

        self._resetDragMode()

        if self._view_info.isPointInItem(item, x, y):
            oldSelectedItem = self._getSelectedItem()
            if oldSelectedItem != item:
                self._onSelectItem(item, oldSelectedItem)
            elif self._view_info.isPointInSelection(item, x, y):
                self._editItemCencelled = False
                self._editItemTimer.StartOnce(self._editClickDelay_ms)
            return

    def _onRightButtonDown(self, event):
        self._completeItemEdit()

    def _onRightButtonUp(self, event):
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if item is None:
            return

        event = NotesTreeRightButtonUpEvent(page=item.getPage())
        wx.PostEvent(self, event)

    def _onMiddleButtonDown(self, event):
        self._completeItemEdit()

    def _onMiddleButtonUp(self, event):
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if item is None:
            return

        event = NotesTreeMiddleButtonUpEvent(page=item.getPage())
        wx.PostEvent(self, event)

    def _onLeftDblClick(self, event):
        self._editItemCencelled = True
        self._completeItemEdit()
        y = event.GetY() + self._getScrollY()
        item = self._getItemByY(y)
        if item is None:
            return

        event = NotesTreeItemActivateEvent(page=item.getPage())
        wx.PostEvent(self, event)

    def _getItemByY(self, y: int) -> Optional[NotesTreeItem]:
        for item in self._visibleItems:
            y_min = self._view_info.getItemTop(item)
            y_max = self._view_info.getItemBottom(item)
            if y >= y_min and y <= y_max:
                return item
            if y_min > y:
                break
        return None

    def _getItemByXY(self, x: int, y: int) -> Optional[NotesTreeItem]:
        item = self._getItemByY(y)
        if item is None:
            return None

        x_min = self._view_info.getIconLeft(item)
        x_max = self._view_info.getSelectionRight(item)
        return item if x >= x_min and x <= x_max else None

    def HitTest(self, point: Tuple[int, int]) -> Optional[BasePage]:
        x = point[0] + self._getScrollX()
        y = point[1] + self._getScrollY()
        item = self._getItemByY(y)
        if item is None:
            return None

        if (x >= self._view_info.getIconLeft(item)
                and x <= self._view_info.getSelectionRight(item)):
            return item.getPage()

    def _calculateItemsProperties(self):
        calculator = _NotesTreeItemPropertiesCalculator(self._view_info)
        for root_item in self._rootItems:
            calculator.run(root_item)
            self._visibleItems = calculator.getVisibleItems()

        widths = [
            self._view_info.getTitleLeft(item)
            + item.getTextWidth()
            + self._view_info.title_right_margin
            for item in self._visibleItems
        ]
        hor_step = 10
        max_scroll_x = (max(widths) if widths else 0) // hor_step
        max_scroll_y = calculator.getLastLine() + 1

        old_scroll_pos_x = self.GetScrollPos(wx.HORIZONTAL)
        old_scroll_pos_y = self.GetScrollPos(wx.VERTICAL)

        self.SetScrollbars(
            hor_step,
            self._view_info.line_height,
            max_scroll_x,
            max_scroll_y,
            old_scroll_pos_x,
            old_scroll_pos_y,
            noRefresh=True
        )

    def _refreshItem(self, item: NotesTreeItem):
        with wx.ClientDC(self) as dc:
            with _ItemsPainter(
                self, dc, self._iconsCache.getImageList(), self._view_info
            ) as painter:
                interval_x = self._getScrolledX()
                interval_y = self._getScrolledY()
                dx = -interval_x[0]
                dy = -interval_y[0]
                painter.draw(item, dx, dy)

    def _onPaint(self, event):
        with wx.BufferedPaintDC(self) as dc:
            with _ItemsPainter(
                self, dc, self._iconsCache.getImageList(), self._view_info
            ) as painter:
                interval_x = self._getScrolledX()
                interval_y = self._getScrolledY()
                painter.fillBackground()
                for item in self._visibleItems:
                    dx = -interval_x[0]
                    dy = -interval_y[0]
                    item_top = self._view_info.getItemTop(item)
                    if item_top >= interval_y[0]:
                        painter.drawTreeLines(item, dx, dy)

                    if item_top >= interval_y[0] and item_top <= interval_y[1]:
                        painter.draw(item, dx, dy)

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

    def _createRootNotesTreeItem(self, rootPage: BasePage) -> "NotesTreeItem":
        rootname = os.path.basename(rootPage.path)
        item = NotesTreeItem(rootPage)

        return (
            item.setTitle(rootname)
            .setIconImageId(self._iconsCache.getDefaultImageId())
            .setVisible()
        )

    def _createNotesTreeItem(self, page: WikiPage) -> "NotesTreeItem":
        new_item = NotesTreeItem(page)
        return self._updateItemProperties(new_item)

    def _updateItemProperties(self, item: "NotesTreeItem"):
        page = item.getPage()

        assert page is not None
        parent_page = page.parent
        if parent_page is not None:
            title = page.display_title
            parent_item = self._pageCache.get(parent_page)
            item.setParent(parent_item)
            item.setTitle(title)
            item.expand(self._getPageExpandState(page))
            item.setIconImageId(self._loadIcon(page))
            item.setItalic(page.readonly)
        return item

    def updateItem(self, page: WikiPage, update=True):
        item = self._pageCache.get(page)
        assert item is not None
        self._updateItemProperties(item)
        if update:
            self.updateTree()

    def clear(self, update=True):
        self._iconsCache.clear()
        self._pageCache.clear()
        self._rootItems.clear()
        self._visibleItems.clear()
        if update:
            self.updateTree()

    def addRoot(self, rootPage: BasePage, update=True):
        assert rootPage is not None
        root_item = self._createRootNotesTreeItem(rootPage)
        root_item.expand(True)
        self._rootItems.append(root_item)
        self._pageCache[rootPage] = root_item
        if update:
            self.updateTree()

    def updateTree(self):
        self._calculateItemsProperties()
        self.Refresh()

    def addPage(self, page: WikiPage, update=True):
        """
        Вставить одну дочерниюю страницу (page) в ветвь
        """
        if page not in self._pageCache:
            parentItem = self._getTreeItem(page.parent)
            assert parentItem is not None

            item = self._createNotesTreeItem(page)
            parentItem.addChild(item)
            self._pageCache[page] = item

        if update:
            self.updateTree()

    def scrollToPage(self, page: Optional[BasePage]):
        if page is None:
            return

        item = self._pageCache.get(page)
        if item is not None:
            scroll_x = 0
            scroll_y = item.getLine() - 1
            if scroll_y < 0:
                scroll_y = 0

            self.SetScrollPos(wx.HORIZONTAL, scroll_x, refresh=False)
            self.SetScrollPos(wx.VERTICAL, scroll_y)

    def _beginItemEdit(self, item: NotesTreeItem):
        self._currentEditItem = item

        scroll_x = self._getScrollX()
        scroll_y = self._getScrollY()
        x_min = self._view_info.getSelectionLeft(item)
        y_min = self._view_info.getSelectionTop(item)
        y_max = self._view_info.getSelectionBottom(item)

        width = self.GetClientSize().GetWidth() - x_min - 2
        textCtrlHeight = self._editItemTextCtrl.GetSize().GetHeight()
        y = y_min + abs(y_max - y_min - textCtrlHeight) // 2

        self._editItemTextCtrl.SetSize(
            x_min - scroll_x, y - scroll_y, width, -1
        )
        title = item.getTitle()
        self._editItemTextCtrl.SetValue(title)
        self._editItemTextCtrl.SetSelection(0, len(title))
        self._editItemTextCtrl.Show()
        self._editItemTextCtrl.SetFocus()

    def _cancelItemEdit(self):
        self._currentEditItem = None
        self._editItemTextCtrl.Hide()

    def _completeItemEdit(self):
        if self._currentEditItem is not None:
            event = NotesTreeEndItemEditEvent(
                page=self._currentEditItem.getPage(),
                new_title=self._editItemTextCtrl.GetValue(),
            )
            wx.PostEvent(self, event)
            self._cancelItemEdit()

    def editItem(self, page: WikiPage):
        item = self._pageCache.get(page)
        if item is not None:
            self._beginItemEdit(item)

    def _getAllPageChildren(self, parent_item: NotesTreeItem, children: List[BasePage]):
        children_items = parent_item._children
        children += [item.getPage() for item in children_items]
        for child_item in children_items:
            self._getAllPageChildren(child_item, children)

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

    def _getPageExpandState(self, page: Optional[BasePage]):
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

    def _getTreeItem(self, page: Optional[BasePage]) -> Optional[NotesTreeItem]:
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
            self.expand(page, True)

    def expand(self, page, expanded=True, update=True):
        item = self._getTreeItem(page)
        if item is not None:
            item.expand(expanded)
            event = NotesTreeItemExpandChangedEvent(page=page, expanded=expanded)
            wx.PostEvent(self, event)
            if update:
                self.updateTree()

    def _getSelectedItem(self) -> Optional[NotesTreeItem]:
        for item in self._pageCache.values():
            if item.isSelected():
                return item
        return None

    def getSelectedPage(self) -> Optional[BasePage]:
        for page, item in self._pageCache.items():
            if item.isSelected():
                return page
        return None

    def setSelectedPage(self, newSelectedPage: Optional[BasePage]):
        for page, item in self._pageCache.items():
            item.select(page is newSelectedPage)

        self.updateTree()
        self.scrollToPage(newSelectedPage)
