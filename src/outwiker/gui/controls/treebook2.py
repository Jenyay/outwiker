import os.path
from typing import List, Optional, Tuple, Dict

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from outwiker.gui.imagelistcache import ImageListCache
from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT


class Treebook2(wx.SplitterWindow):
    def __init__(self, parent: wx.Window, defaultIcon: str):
        super().__init__(parent)
        self._default_icon = defaultIcon
        self._current_page: Optional[wx.Panel] = None
        self._default_leftSize = 300
        self._create_gui()
        self._pages: List[BasePrefPanel] = []
        self._tagged_pages: Dict[str, Tuple[wx.TreeItemId, BasePrefPanel]] = {}

        self._tree.Bind(wx.EVT_TREE_SEL_CHANGED, handler=self._onSelected)

    def Clear(self):
        self._tree.Unbind(wx.EVT_TREE_SEL_CHANGED, handler=self._onSelected)

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
        self._iconsCache = ImageListCache(self._default_icon, ICONS_WIDTH, ICONS_HEIGHT)

        self._tree = wx.TreeCtrl(
            self,
            style=wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_HAS_BUTTONS | wx.TR_NO_LINES,
        )
        self._tree.AssignImageList(self._iconsCache.getImageList())
        self._root_item_id = self._tree.AddRoot(
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

    def AddPage(
        self,
        page: "BasePrefPanel",
        label: str,
        parent_page_tag: Optional[str] = None,
        icon_fname=None,
        tag: Optional[str] = None,
    ):
        page.Hide()
        if parent_page_tag is not None and parent_page_tag in self._tagged_pages:
            parent = self._tagged_pages[parent_page_tag][0]
        else:
            parent = self._root_item_id

        item_id = self._tree.AppendItem(
            parent, text=label, data=page, image=self._loadIcon(icon_fname)
        )

        self._pages.append(page)
        if tag:
            self._tagged_pages[tag] = (item_id, page)

    def GetPages(self) -> List["BasePrefPanel"]:
        return self._pages

    def SetSelection(self, tag: str):
        if tag in self._tagged_pages:
            item_id = self._tagged_pages[tag][0]
            self._tree.SelectItem(item_id)

    def ExpandNode(self, tag: str):
        if tag in self._tagged_pages:
            item_id = self._tagged_pages[tag][0]
            self._tree.Expand(item_id)

    def ExpandAll(self):
        self._tree.ExpandAll()

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
