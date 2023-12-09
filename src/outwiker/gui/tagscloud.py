# -*- coding: utf-8 -*-

import os
from typing import Collection, Dict, List, Optional, Tuple
from collections.abc import Iterable
from datetime import datetime

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.core.tagslist import TagsList
from outwiker.gui.controls.taglabel2 import TagLabel2
from outwiker.gui.defines import TAGS_CLOUD_MODE_CONTINUOUS, TAGS_CLOUD_MODE_LIST


class TagsCloud(wx.Panel):
    def __init__(
        self,
        parent,
        use_buttons: bool = True,
        min_font_size: int = 8,
        max_font_size: int = 16,
        mode: str = TAGS_CLOUD_MODE_CONTINUOUS,
        enable_tooltips: bool = True,
        enable_active_tags_filter: bool = True
    ):
        super().__init__(parent)
        self._use_buttons = use_buttons
        self._min_font_size = min_font_size
        self._max_font_size = max_font_size
        self._mode = mode
        self._enable_tooltips = enable_tooltips
        self._enable_active_tags_filter = enable_active_tags_filter

        self._scroll_start_time = None
        self._scroll_timeout_musec = 200e3

        # Отступ от края окна
        self._margin = 4

        # Зазор между тегами по горизонтали
        self._gapx = 10

        # Зазор между метками по вертикали
        self._gapy = 4

        # Size of the control before tags layout
        self._oldSize = (-1, -1)

        self._filter = ""
        self._tags: Optional[TagsList] = None
        self._filtered_tags: List[str] = []

        # Ключ - имя метки, значение - контрол, отображающий эту метку
        self._labels: Dict[str, TagLabel2] = {}

        self._prevLabelHovered: Optional[TagLabel2] = None

        self._create_gui()

        self._tags_panel.Bind(wx.EVT_SIZE, self.__onSize)
        self._tags_panel.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self._tags_panel.Bind(wx.EVT_MOTION, handler=self._onMouseMove)
        self._tags_panel.Bind(wx.EVT_LEFT_DOWN, handler=self._onLeftMouseClick)
        self._tags_panel.Bind(wx.EVT_RIGHT_DOWN, handler=self._onRightMouseClick)
        self._tags_panel.Bind(wx.EVT_MIDDLE_DOWN, handler=self._onMiddleMouseClick)
        self._tags_panel.Bind(wx.EVT_SCROLLWIN, handler=self._onScroll)
        self._search_ctrl.Bind(wx.EVT_TEXT, handler=self._onSearch)
        self._search_ctrl.Bind(wx.EVT_KEY_DOWN, self._onKeyPressed)
        self._active_tags_flag.Bind(wx.EVT_TOGGLEBUTTON, self._onActiveTagsToggle)

    def _findLabel(self, x, y) -> Optional[TagLabel2]:
        result = None

        for label in self._labels.values():
            if not label.isVisible():
                continue

            label_x_min, label_y_min = label.getPosition()
            label_x_max, label_y_max = label.getPositionMax()
            if (y >= label_y_min and y <= label_y_max and
                    x >= label_x_min and x <= label_x_max):
                result = label
                break

            if y < label_y_min:
                break

        return result

    def _getMouseCoord(self, event) -> Tuple[int, int]:
        return (event.GetX(), event.GetY() + self._getScrolledY()[0])

    def _onScroll(self, event):
        event.Skip()
        # Don't repaint labels during scroll
        self._scroll_start_time = datetime.now()
        if self._prevLabelHovered is not None:
            self._prevLabelHovered.setHover(False)
            self._tags_panel.UnsetToolTip()
            self._prevLabelHovered = None

    def _onMouseMove(self, event):
        # Don't repaint labels during scroll
        if self._scroll_start_time is not None:
            delta = datetime.now() - self._scroll_start_time
            if delta.microseconds >= self._scroll_timeout_musec:
                self._scroll_start_time = None
            else:
                return

        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)

        if (self._prevLabelHovered is not None and 
                label is not self._prevLabelHovered):
            self._tags_panel.UnsetToolTip()
            self._prevLabelHovered.setHover(False)

        if label is not None and label is not self._prevLabelHovered:
            label.setHover(True)
            if self._enable_tooltips:
                assert self._tags is not None
                tooltip = _("Number of notes: {}").format(len(self._tags[label.getLabel()]))
                self._tags_panel.SetToolTip(tooltip)

        self._prevLabelHovered = label

        if label is not None:
            label_x, label_y = label.getPosition()
            label.onMouseMove(x - label_x, y - label_y)

    def _onLeftMouseClick(self, event):
        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)
        if label is not None:
            label_x, label_y = label.getPosition()
            label.onLeftMouseClick(x - label_x, y - label_y)

    def _onRightMouseClick(self, event):
        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)
        if label is not None:
            label_x, label_y = label.getPosition()
            label.onRightMouseClick(x - label_x, y - label_y)

    def _onMiddleMouseClick(self, event):
        x, y = self._getMouseCoord(event)
        label = self._findLabel(x, y)
        if label is not None:
            label_x, label_y = label.getPosition()
            label.onMiddleMouseClick(x - label_x, y - label_y)

    def _getScrolledY(self) -> Tuple[int, int]:
        ymin = self._tags_panel.GetScrollPos(wx.VERTICAL) * self._tags_panel.GetScrollPixelsPerUnit()[1]
        ymax = ymin + self._tags_panel.GetClientSize()[1]
        return (ymin, ymax)

    def _repaintLabels(self, label_names: Iterable, dc: wx.DC):
        y_min, y_max = self._getScrolledY()

        for label_name in label_names:
            label = self._labels[label_name]
            label_x_min, label_y_min = label.getPosition()
            label_y_max = label.getPositionMax()[1]
            if label_y_min <= y_max and label_y_max >= y_min:
                label.onPaint(dc, label_x_min, label_y_min - y_min)

            if label_y_min > y_max:
                break

    def _onPaint(self, event):
        with wx.PaintDC(self._tags_panel) as dc:
            back_color = self.GetBackgroundColour()
            dc.SetBrush(wx.Brush(back_color))
            dc.SetPen(wx.Pen(back_color))
            width, height = self._tags_panel.GetClientSize()
            dc.DrawRectangle(0, 0, width, height)
            self._repaintLabels(self._filtered_tags, dc)

    def setFontSize(self, min_font_size: int, max_font_size: int):
        self._min_font_size = min_font_size
        self._max_font_size = max_font_size

        for tag_label in self._labels.values():
            tag_label.setFontSize(min_font_size, max_font_size)

        self._layoutTags()

    def setMode(self, mode):
        self._mode = mode
        self._layoutTags()

    def _create_gui(self):
        self.SetMinSize((150, 150))
        self._main_sizer = wx.FlexGridSizer(cols=1)
        self._main_sizer.AddGrowableCol(0)
        self._main_sizer.AddGrowableRow(1)

        self._tags_panel = wx.ScrolledCanvas(self)
        self._tags_panel.SetScrollRate(0, 0)

        self._search_ctrl = wx.SearchCtrl(self)
        self._active_tags_flag = wx.BitmapToggleButton(self, label=wx.Bitmap(getBuiltinImagePath("tag_active.png")))
        self._active_tags_flag.SetToolTip(_("Applied tags only"))
        self._active_tags_flag.Show(self._enable_active_tags_filter)

        filter_sizer = wx.FlexGridSizer(cols=2)
        filter_sizer.AddGrowableCol(0)
        filter_sizer.AddGrowableRow(0)

        filter_sizer.Add(self._search_ctrl, flag=wx.EXPAND)
        filter_sizer.Add(self._active_tags_flag, flag=wx.ALIGN_RIGHT | wx.EXPAND)

        self._main_sizer.Add(filter_sizer, flag=wx.EXPAND)
        self._main_sizer.Add(self._tags_panel, flag=wx.EXPAND)

        self.SetSizer(self._main_sizer)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        for label in self._labels.values():
            label.setBackColor(colour)
        self._tags_panel.SetBackgroundColour(colour)
        self._search_ctrl.SetBackgroundColour(colour)

    def __onSize(self, event):
        newSize = self.GetSize()
        if self._oldSize != newSize:
            self.__moveLabels()
            self._oldSize = newSize

    def _onSearch(self, event):
        self._updateFilter()

    def _onKeyPressed(self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self._search_ctrl.SetValue("")

        event.Skip()

    def _is_active_only(self):
        return self._active_tags_flag.GetValue()

    def _onActiveTagsToggle(self, event):
        self._updateFilter()

    def _updateFilter(self):
        self.setFilter(self._search_ctrl.GetValue(), self._is_active_only())

    def setTags(self, taglist: TagsList):
        """
        Добавить теги в облако
        """
        self.Freeze()
        oldy = self._tags_panel.GetScrollPos(wx.VERTICAL)
        self.clear()

        self._tags = taglist
        self._create_tag_labels()

        active_only = self._active_tags_flag.GetValue()
        self._filtered_tags = (
            self._filter_tags(self._tags.tags, active_only) if self._tags is not None else []
        )
        self._filter_tag_labels()
        self._tags_panel.Scroll(-1, oldy)
        self._prevLabelHover = None
        self.Thaw()
        self.Update()

    def setFilter(self, tags_filter: str, active_only: bool = False):
        self._filter = tags_filter

        if self._tags is None:
            return

        self._filtered_tags = (
            self._filter_tags(self._tags.tags, active_only) if self._tags is not None else []
        )
        self._filter_tag_labels()

    def enableTooltips(self, enable: bool = True):
        if enable != self._enable_tooltips:
            self._enable_tooltips = enable
            if not enable:
                self._tags_panel.UnsetToolTip()

    def _create_tag_labels(self):
        if self._tags is None:
            return

        back_color = self.GetBackgroundColour()
        for tag in self._tags:
            newlabel = TagLabel2(
                self._tags_panel,
                tag,
                self._use_buttons,
                self._min_font_size,
                self._max_font_size,
                back_color=back_color
            )

            self._labels[tag] = newlabel

    def _filter_tag_labels(self):
        if self._tags is None:
            return

        for tag_name in self._tags:
            label = self._labels[tag_name]
            label.Show(tag_name in self._filtered_tags)

        self._layoutTags()

    def _filter_tags(self, tags: List[str], active_only: bool) -> List[str]:
        return list(
            filter(lambda tag_name: self._filter.lower() in tag_name.lower() and (not active_only or self.isMarked(tag_name)), tags)
        )

    def mark(self, tag: str, marked: bool = True):
        """
        Выделить метку
        """
        if tag.lower().strip() in self._labels.keys():
            self._labels[tag.lower().strip()].mark(marked)
            if self._is_active_only():
                self._updateFilter()

    def mark_list(self, tags: Collection[str], marked: bool = True):
        for tag in tags:
            if tag.lower().strip() in self._labels.keys():
                self._labels[tag.lower().strip()].mark(marked)

        if self._is_active_only():
            self._updateFilter()

        self.Update()

    def clearMarks(self):
        """
        Убрать все выделения с меток
        """
        for label in self._labels.values():
            label.mark(False)

        if self._is_active_only():
            self._updateFilter()

    def isMarked(self, tag):
        return self._labels[tag].isMarked

    def clear(self):
        self._labels = {}
        self._tags = None
        self._filtered_tags = []

    def __getMaxCount(self) -> int:
        count = 0
        if self._tags is None:
            return count

        for tag in self._tags:
            if len(self._tags[tag]) > count:
                count = len(self._tags[tag])

        return count

    def __calcSizeRatio(self, count):
        assert self._tags is not None

        maxcount = self.__getMaxCount()
        ratio = 1

        if maxcount != 0:
            ratio = float(count) / maxcount

        return ratio

    def __setSizeLabels(self):
        if self._tags is None:
            return

        for tagname in self._filtered_tags:
            count = len(self._tags[tagname])
            ratio = self.__calcSizeRatio(count)

            label = self._labels[tagname]
            label.setRatio(ratio)

    def _layoutTags(self):
        """
        Расположение тегов в окне
        """
        if self._tags is None:
            return

        self.__setSizeLabels()
        self.__moveLabels()

    def __moveLabels(self):
        if self._tags is None or len(self._tags) == 0:
            return

        assert len(self._labels) != 0

        # Хак из-за разного поведения полос прокрутки в винде и линуксе
        if os.name != "nt":
            self._tags_panel.SetScrollbars(0, 0, 0, 0)

        if self._mode == TAGS_CLOUD_MODE_LIST:
            self.__moveLabelsAsList()
        else:
            self.__moveLabelsContinuous()

        self._tags_panel.Update()

    def _getScrollStepY(self) -> int:
        return list(self._labels.values())[0].getSize()[1] + self._gapy

    def __moveLabelsAsList(self):
        stepy = self._getScrollStepY()

        for line, tagname in enumerate(self._filtered_tags):
            label = self._labels[tagname]
            label.Move(self._margin, self._margin + line * stepy)

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, len(self._filtered_tags))

    def __moveLabelsContinuous(self):
        stepy = list(self._labels.values())[0].getSize()[1] + self._gapy

        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self._margin
        currenty = self._margin

        linesCount = 1

        maxwidth = self._tags_panel.GetClientSize()[0] - self._margin * 2

        for tagname in self._filtered_tags:
            label = self._labels[tagname]

            newRightBorder = currentx + label.getSize()[0]

            if newRightBorder > maxwidth and len(currentLine) != 0:
                currentx = self._margin
                currenty += stepy

                currentLine = []
                linesCount += 1

            label.Move(currentx, currenty)

            currentLine.append(label)
            currentx += label.getSize()[0] + self._gapx

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, linesCount)
