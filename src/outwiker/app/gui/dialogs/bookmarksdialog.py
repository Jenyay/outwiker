import wx

from outwiker.core.application import Application
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.pagelist_columns import ColumnsFactory
from outwiker.gui.guiconfig import BookmarksDialogConfig
from outwiker.gui.images import readImage
from outwiker.gui.theme import Theme
from outwiker.gui.controls.pagelist import PageList


class BookmarksDialog(wx.Frame):
    def __init__(self, parent: wx.Window, theme: Theme):
        super().__init__(
            parent,
            style=wx.CAPTION
            | wx.RESIZE_BORDER
            | wx.CLOSE_BOX
            | wx.FRAME_FLOAT_ON_PARENT
            | wx.FRAME_TOOL_WINDOW
        )
        self._theme = theme

        self.Hide()
        self.SetTitle(_("Bookmark management"))
        self._create_gui()

    def applyTheme(self):
        self.SetBackgroundColour(self._theme.colorBackground)
        self.bookmark_list.SetBackgroundColour(self._theme.colorBackground)

    def Destroy(self) -> bool:
        self.Hide()
        self.bookmark_list.Destroy()
        return super().Destroy()

    def _create_gui(self):
        button_height = wx.Button.GetDefaultSize().height
        button_width = button_height
        icon_size = (
            button_height
            - self._theme.get(Theme.SECTION_GENERAL, Theme.BITMAP_BUTTON_PADDING) * 2
        )

        # Bookmarks list
        self.bookmark_list = PageList(self, sortable=False, selectable=True)
        columns = ColumnsFactory().createDefaultColumns()
        self.bookmark_list.setColumns(columns)

        # Move up button
        self.move_up_btn = wx.BitmapButton(
            self,
            bitmap=readImage(getBuiltinImagePath("arrow_up.svg"), icon_size, icon_size),
        )
        self.move_up_btn.SetMinSize(wx.Size(button_width, button_height))
        self.move_up_btn.SetToolTip(_("Move bookmark up"))

        # Move down button
        self.move_down_btn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("arrow_down.svg"), icon_size, icon_size
            ),
        )
        self.move_down_btn.SetMinSize(wx.Size(button_width, button_height))
        self.move_down_btn.SetToolTip(_("Move bookmark down"))

        # Remove button
        self.remove_btn = wx.BitmapButton(
            self,
            bitmap=readImage(getBuiltinImagePath("remove.svg"), icon_size, icon_size),
        )
        self.remove_btn.SetMinSize(wx.Size(button_width, button_height))
        self.remove_btn.SetToolTip(_("Remove bookmark"))
        self._layout()

        self.applyTheme()

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)
        self.SetSizer(main_sizer)

        # Buttons
        buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer.Add(self.move_up_btn, flag=wx.ALL, border=2)
        buttons_sizer.Add(self.move_down_btn, flag=wx.ALL, border=2)
        buttons_sizer.Add(self.remove_btn, flag=wx.ALL, border=2)

        # List layout
        list_sizer = wx.FlexGridSizer(cols=2)
        list_sizer.AddGrowableCol(0)
        list_sizer.AddGrowableRow(0)
        list_sizer.Add(self.bookmark_list, flag=wx.EXPAND)
        list_sizer.Add(buttons_sizer, flag=wx.ALL, border=2)

        main_sizer.Add(list_sizer, flag=wx.EXPAND)

        self.Layout()


class BookmarksDialogController:
    def __init__(self, dialog: BookmarksDialog, application: Application) -> None:
        self._dlg = dialog
        self._application = application
        self._config = BookmarksDialogConfig(self._application.config)

        self._dlg.move_up_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveUp)
        self._dlg.move_down_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveDown)
        self._dlg.remove_btn.Bind(wx.EVT_BUTTON, handler=self._onRemoveBookmark)
        self._dlg.Bind(wx.EVT_CLOSE, handler=self._onClose)

    def show(self):
        if not self._dlg.IsShown():
            self._load_dialog_rect()
            self._update_bookmark_list()
            self._dlg.Show()
            self._dlg.SetFocus()

    def destroy(self):
        self._dlg.Unbind(wx.EVT_CLOSE, handler=self._onClose)
        self._dlg.Destroy()
        wx.SafeYield()

    def _update_bookmark_list(self):
        pages = [page for page in self._application.bookmarks if page is not None]
        self._dlg.bookmark_list.setPageList(pages)
        self._dlg.bookmark_list.setSelected(0)

    def _onMoveUp(self, event):
        self._dlg.bookmark_list.moveSelectedItemUp()
        self._save_bookmarks()

    def _onMoveDown(self, event):
        self._dlg.bookmark_list.moveSelectedItemDown()
        self._save_bookmarks()

    def _onRemoveBookmark(self, event):
        sel_index = self._dlg.bookmark_list.getSelectedIndex()
        if sel_index is not None:
            self._dlg.bookmark_list.removeItem(sel_index)
            self._save_bookmarks()

    def _save_bookmarks(self):
        pages = self._dlg.bookmark_list.getPageList()

    def _onClose(self, event):
        self._save_dialog_rect()
        self._dlg.Hide()

    def _save_dialog_rect(self):
        rect = self._dlg.GetRect()

        if rect.width > 0 and rect.height > 0:
            self._config.width.value = rect.width
            self._config.height.value = rect.height
            self._config.x.value = rect.x
            self._config.y.value = rect.y

    def _load_dialog_rect(self):
        width = self._config.width.value
        height = self._config.height.value
        x = self._config.x.value
        y = self._config.y.value

        assert width is not None
        assert height is not None
        assert x is not None
        assert y is not None

        if x < 0 or y < 0:
            parent_wnd_rect = self._dlg.GetParent().GetRect()
            x = parent_wnd_rect.x + (parent_wnd_rect.width - width) // 2
            y = parent_wnd_rect.y + (parent_wnd_rect.height - height) // 2

        self._dlg.SetSize(x, y, width, height, sizeFlags=wx.SIZE_FORCE)
