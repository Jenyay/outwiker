# -*- coding: utf-8 -*-

import sys

import wx
import wx.lib.newevent

import outwiker.gui.controls.ultimatelistctrl as ULC

# Событие, возникающее при клике по элементу, описывающий страницу
PageClickEvent, EVT_PAGE_CLICK = wx.lib.newevent.NewEvent()


class PageData(object):
    def __init__(self, page, parent=None):
        self.page = page
        self.parent = parent


class PageList(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self._propagationLevel = 15
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self._sizer = wx.FlexGridSizer(cols=1)
        self._sizer.AddGrowableCol(0)
        self._sizer.AddGrowableRow(0)

        self._listCtrl = ULC.UltimateListCtrl(
            self,
            agwStyle=ULC.ULC_REPORT | ULC.ULC_SINGLE_SEL | ULC.ULC_VRULES | ULC.ULC_HRULES | ULC.ULC_SHOW_TOOLTIPS | ULC.ULC_NO_HIGHLIGHT
        )

        self._listCtrl.Bind(ULC.EVT_LIST_ITEM_HYPERLINK,
                            handler=self._onPageClick)
        self._listCtrl.SetHyperTextNewColour(wx.BLUE)
        self._listCtrl.SetHyperTextVisitedColour(wx.BLUE)

        self._sizer.Add(self._listCtrl, flag=wx.EXPAND)

        self.SetSizer(self._sizer)

    def _onPageClick(self, event):
        item = event.GetItem()
        pageData = item.GetPyData()
        if pageData:
            page = pageData.page
            assert page is not None
            event = PageClickEvent(page=page)
            event.ResumePropagation(self._propagationLevel)
            wx.PostEvent(self, event)

    def clear(self):
        """
        Удалить все элементы из списка
        """
        self._listCtrl.ClearAll()

        self._listCtrl.InsertColumn(0, _('Title'))
        self._listCtrl.SetColumnWidth(0, 200)

        self._listCtrl.InsertColumn(1, _('Parent'))
        self._listCtrl.SetColumnWidth(1, 200)

        self._listCtrl.InsertColumn(2, _('Tags'))
        self._listCtrl.SetColumnWidth(2, 200)

        self._listCtrl.InsertColumn(3, _('Modify date'))
        self._listCtrl.SetColumnWidth(3, 200)

    def setPageList(self, pages):
        """
        pages - список страниц, отображаемый в списке
        """
        self._listCtrl.Freeze()
        self.clear()

        for page in pages:
            data = PageData(page)
            # Title
            index = self._listCtrl.InsertStringItem(sys.maxsize,
                                                    page.display_title)

            self._listCtrl.SetItemHyperText(index, 0)

            # Parent
            parent_page = page.parent
            if parent_page.parent:
                self._listCtrl.SetStringItem(
                    index,
                    1,
                    parent_page.display_subpath + '/')
                # self._listCtrl.SetItemHyperText(index, 1)
                data.parent = parent_page

            # Tags
            self._listCtrl.SetStringItem(index, 2, ', '.join(page.tags))

            # Modify date
            date = page.datetime.strftime('%d.%m.%Y     %H:%M')
            self._listCtrl.SetStringItem(index, 3, date)

            self._listCtrl.SetItemPyData(index, data)

        self._listCtrl.Thaw()
