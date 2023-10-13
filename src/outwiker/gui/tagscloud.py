# -*- coding: utf-8 -*-

import os
from typing import Dict, List, Optional

import wx

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
    ):
        super().__init__(parent)
        self._use_buttons = use_buttons
        self._min_font_size = min_font_size
        self._max_font_size = max_font_size
        self._mode = mode
        self._enable_tooltips = enable_tooltips

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

        self._create_gui()

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self._tags_panel.Bind(wx.EVT_SIZE, self.__onSize)
        self._tags_panel.Bind(wx.EVT_PAINT, handler=self._onPaint)
        self._search_ctrl.Bind(wx.EVT_TEXT, handler=self._onSearch)
        self._search_ctrl.Bind(wx.EVT_KEY_DOWN, self._onKeyPressed)

    def _onPaint(self, event):
        # dc = wx.PaintDC(self._tags_panel)
        with wx.PaintDC(self._tags_panel) as dc:
            for label in self._labels.values():
                label.onPaint(dc)

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

        self._tags_panel = wx.ScrolledWindow(self)
        self._tags_panel.SetScrollRate(0, 0)

        self._search_ctrl = wx.SearchCtrl(self)

        self._main_sizer.Add(self._search_ctrl, flag=wx.EXPAND | wx.ALL, border=4)
        self._main_sizer.Add(self._tags_panel, flag=wx.EXPAND | wx.ALL, border=4)

        self.SetSizer(self._main_sizer)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)

    def __onSize(self, event):
        newSize = self.GetSize()
        if self._oldSize != newSize:
            self.__moveLabels()
            self._oldSize = newSize

    def _onSearch(self, event):
        self.setFilter(event.GetString())

    def _onKeyPressed(self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self._search_ctrl.SetValue("")

        event.Skip()

    def setTags(self, taglist: TagsList):
        """
        Добавить теги в облако
        """
        self.Freeze()
        oldy = self._tags_panel.GetScrollPos(wx.VERTICAL)
        self.clear()

        self._tags = taglist
        self._filtered_tags = (
            self._filter_tags(self._tags.tags) if self._tags is not None else []
        )

        self._create_tag_labels()
        self._filter_tag_labels()
        self._tags_panel.Scroll(-1, oldy)
        self.Thaw()

    def setFilter(self, tags_filter: str):
        self._filter = tags_filter

        if self._tags is None:
            return

        self.Freeze()
        self._filtered_tags = (
            self._filter_tags(self._tags.tags) if self._tags is not None else []
        )
        self._filter_tag_labels()
        self.Thaw()

    def enableTooltips(self, enable: bool = True):
        if enable != self._enable_tooltips:
            self._enable_tooltips = enable
            self._update_tooltips()

    def _create_tag_labels(self):
        if self._tags is None:
            return

        for tag in self._tags:
            newlabel = TagLabel2(
                self._tags_panel,
                tag,
                self._use_buttons,
                self._min_font_size,
                self._max_font_size,
            )

            self._labels[tag] = newlabel

        self._update_tooltips()

    def _update_tooltips(self):
        if self._tags is None:
            return

        for tag in self._tags:
            label = self._labels[tag]

            # if self._enable_tooltips:
            #     tooltip = _("Number of notes: {}").format(len(self._tags[tag]))
            #     label.SetToolTip(tooltip)
            # else:
            #     label.UnsetToolTip()


    def _filter_tag_labels(self):
        if self._tags is None:
            return

        for tag_name in self._tags:
            tag_ctrl = self._labels[tag_name]
            tag_ctrl.Show(tag_name in self._filtered_tags)

        self._layoutTags()

    def _filter_tags(self, tags: List[str]) -> List[str]:
        if not self._filter:
            return tags

        return list(
            filter(lambda tag_name: self._filter.lower() in tag_name.lower(), tags)
        )

    def mark(self, tag: str, marked: bool = True):
        """
        Выделить метку
        """
        if tag.lower().strip() in self._labels.keys():
            self._labels[tag.lower().strip()].mark(marked)

    def clearMarks(self):
        """
        Убрать все выделения с меток
        """
        for label in self._labels.values():
            label.mark(False)

    def isMarked(self, tag):
        return self._labels[tag].isMarked

    def clear(self):
        # for label in self._labels.values():
        #     label.Destroy()

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

        # Дважды перемещаем метки, чтобы учесть,
        # что может появиться полоса прокрутки
        self.__moveLabels()
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

        self.Refresh()

    def __moveLabelsAsList(self):
        stepy = list(self._labels.values())[0].GetSize()[1] + self._gapy

        for line, tagname in enumerate(self._filtered_tags):
            label = self._labels[tagname]
            label.Move(self._margin, self._margin + line * stepy)
            label.Refresh()

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, len(self._filtered_tags))

    def __moveLabelsContinuous(self):
        stepy = list(self._labels.values())[0].GetSize()[1] + self._gapy

        # Метки, расположенные на текущей строке
        currentLine = []

        currentx = self._margin
        currenty = self._margin

        linesCount = 1

        maxwidth = self._tags_panel.GetClientSize()[0] - self._margin * 2

        for tagname in self._filtered_tags:
            label = self._labels[tagname]

            newRightBorder = currentx + label.GetSize()[0]

            if newRightBorder > maxwidth and len(currentLine) != 0:
                currentx = self._margin
                currenty += stepy

                currentLine = []
                linesCount += 1

            label.Move(currentx, currenty)
            label.Refresh()

            currentLine.append(label)
            currentx += label.GetSize()[0] + self._gapx

        lineheight = stepy
        self._tags_panel.SetScrollbars(0, lineheight, 0, linesCount)
