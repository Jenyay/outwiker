import wx

from outwiker.core.application import Application
from outwiker.core.tree import WikiPage
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.pagelist_columns import ColumnsFactory
from outwiker.gui.images import readImage
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.theme import Theme
from outwiker.gui.controls.pagelist import PageList


class BookmarksDialog(TestedDialog):
    def __init__(self, parent: wx.Window, theme: Theme):
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetTitle(_("Bookmark management"))
        self._theme = theme
        self._create_gui()
        columns = ColumnsFactory().createDefaultColumns()
        self.bookmark_list.setColumns(columns)

    def _create_gui(self):
        button_height = wx.Button.GetDefaultSize().height
        button_width = button_height
        icon_size = (
            button_height
            - self._theme.get(Theme.SECTION_GENERAL, Theme.BITMAP_BUTTON_PADDING) * 2
        )

        # Bookmarks list
        self.bookmark_list = PageList(self, sortable=False, selectable=True)

        # Move up button
        self.move_up_btn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("arrow_up.svg"), icon_size, icon_size
            ),
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
            bitmap=readImage(
                getBuiltinImagePath("remove.svg"), icon_size, icon_size
            ),
        )
        self.remove_btn.SetMinSize(wx.Size(button_width, button_height))
        self.remove_btn.SetToolTip(_("Remove bookmark"))

        # Close button
        self._ok_cancel = self.CreateButtonSizer(wx.CLOSE)
        self._layout()

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
        main_sizer.Add(self._ok_cancel, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)

        self.SetSize(wx.Size(800, 400))
        self.Layout()


class BookmarksDialogController:
    def __init__(self, dialog: BookmarksDialog, application: Application) -> None:
        self._dlg = dialog
        self._application = application
        self._dlg.move_up_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveUp)
        self._dlg.move_down_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveDown)
        self._dlg.remove_btn.Bind(wx.EVT_BUTTON, handler=self._onRemoveBookmark)

    def show(self):
        if not self._dlg.IsShown():
            self._update_bookmark_list()
            self._dlg.Show()

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
