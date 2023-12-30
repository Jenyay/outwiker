import os.path
from typing import List, Optional, Tuple

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from outwiker.gui.imagelistcache import ImageListCache


class Treebook2(wx.SplitterWindow):
    def __init__(self, parent: wx.Window, defaultIcon: str):
        super().__init__(parent)
        self._default_icon = defaultIcon
        self._current_page: Optional[wx.Panel] = None
        self._default_leftSize = 300
        self._last_added_section: Optional[wx.TreeItemId] = None
        self._create_gui()
        self._pages: List[BasePrefPanel] = []

        self._tree.Bind(wx.EVT_TREE_SEL_CHANGED, handler=self._onSelected)

    def _onSelected(self, event):
        if self._current_page is not None:
            self._container_sizer.Clear()
            self._current_page.Hide()

        page = self._tree.GetItemData(event.GetItem())
        if page is not None:
            page.Show()
            self._container_sizer.Add(page, flag=wx.EXPAND | wx.ALL, border=4)
            self._container.Layout()

        self._current_page = page

    def _create_gui(self):
        self._iconsCache = ImageListCache(self._default_icon)
        self._tree = wx.TreeCtrl(
            self, style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS | wx.TR_NO_LINES
        )
        self._tree.AssignImageList(self._iconsCache.getImageList())
        self._root = self._tree.AddRoot(
            _("Preferences"), image=self._iconsCache.getDefaultImageId()
        )

        self._container = wx.Panel(self)
        self.SplitVertically(
            self._tree, self._container, sashPosition=self._default_leftSize
        )

        self._container_sizer = wx.FlexGridSizer(cols=1)
        self._container_sizer.AddGrowableCol(0)
        self._container_sizer.AddGrowableRow(0)
        self._container.SetSizer(self._container_sizer)

    def GetParentPanel(self) -> wx.Panel:
        return self.GetWindow2()

    def GetCurrentPage(self) -> Optional[wx.Panel]:
        return self._current_page

    def AddPage(self, page: "BasePrefPanel", label: str, icon_fname=None):
        self._pages.append(page)
        page.Hide()
        self._last_added_section = self._tree.AppendItem(
            self._root, text=label, data=page, image=self._loadIcon(icon_fname)
        )

    def AddSubPage(self, page: "BasePrefPanel", label: str, icon_fname=None):
        self._pages.append(page)
        page.Hide()
        parent = (
            self._last_added_section
            if self._last_added_section is not None
            else self._root
        )
        self._tree.AppendItem(
            parent, text=label, data=page, image=self._loadIcon(icon_fname)
        )

    def GetPages(self) -> List["BasePrefPanel"]:
        return self._pages

    def SetSelection(self, index: int):
        pass

    def ExpandNode(self, index: int):
        pass

    def _loadIcon(self, icon_fname: Optional[str]):
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        if icon_fname is None:
            return self._iconsCache.getDefaultImageId()

        icon_fname = os.path.abspath(icon_fname)
        imageId = self._iconsCache.add(icon_fname)

        if imageId is None:
            imageId = self._iconsCache.getDefaultImageId()

        return imageId


class BasePrefPanel(ScrolledPanel):
    def __init__(self, treeBook: Treebook2):
        style = wx.TAB_TRAVERSAL | wx.HSCROLL | wx.VSCROLL
        super().__init__(treeBook.GetParentPanel(), style=style)

    def LoadState(self):
        pass

    def Save(self):
        pass

    def Cancel(self):
        pass

    def _addLabelAndControlToSizer(
        self, sizer: wx.Sizer, label: wx.StaticText, control: wx.Control
    ):
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, 0, wx.ALL | wx.ALIGN_RIGHT, border=2)

    def _createLabelAndComboBox(
        self, title: str, sizer: wx.Sizer
    ) -> Tuple[wx.StaticText, wx.ComboBox]:
        label = wx.StaticText(self, label=title)
        combobox = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self._addLabelAndControlToSizer(sizer, label, combobox)
        return (label, combobox)

    def _createLabelAndColorPicker(
        self, title: str, sizer: wx.Sizer
    ) -> Tuple[wx.StaticText, wx.ColourPickerCtrl]:
        label = wx.StaticText(self, label=title)
        colorPicker = wx.ColourPickerCtrl(self)

        self._addLabelAndControlToSizer(sizer, label, colorPicker)
        return (label, colorPicker)

    def _createCheckBox(self, title: str, sizer: wx.Sizer) -> wx.CheckBox:
        checkBox = wx.CheckBox(self, label=title)
        sizer.Add(checkBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        return checkBox

    def _createSection(
        self, main_sizer: wx.Sizer, title: str
    ) -> Tuple[wx.StaticBox, wx.Sizer]:
        """
        Create StaticBox for options
        """
        staticBox = wx.StaticBox(self, label=title)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)

        colorsSizer = wx.FlexGridSizer(cols=2)
        colorsSizer.AddGrowableCol(0)
        colorsSizer.AddGrowableCol(1)

        staticBoxSizer.Add(colorsSizer, flag=wx.EXPAND)
        main_sizer.Add(staticBoxSizer, flag=wx.EXPAND | wx.ALL, border=2)
        return (staticBox, colorsSizer)
