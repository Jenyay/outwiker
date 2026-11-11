import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import BookmarksPaneConfig
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.pagelist_columns import ColumnsFactory
from outwiker.gui.images import readImage
from outwiker.gui.theme import Theme
from outwiker.gui.controls.pagelist import PageList


class BookmarksPanel(wx.Panel):
    def __init__(self, parent: wx.Window, application: Application):
        super().__init__(parent)
        self._application = application
        self._attach_config = BookmarksPaneConfig(self._application.config)
        self._theme = self._application.theme
        self.bookmark_list = None
        self._create_gui_part_1()

    def applyTheme(self):
        self.SetBackgroundColour(self._theme.colorBackground)
        self.bookmark_list.SetBackgroundColour(self._theme.colorBackground)

    def _create_buttons(self):
        button_height = wx.Button.GetDefaultSize().height
        button_width = button_height
        icon_size = (
            button_height
            - self._theme.get(Theme.SECTION_GENERAL, Theme.BITMAP_BUTTON_PADDING) * 2
        )

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

    def _create_bookmark_list(self):
        self.bookmark_list = PageList(self, sortable=False, selectable=True)
        columns = ColumnsFactory().createDefaultColumns()
        self.bookmark_list.setColumns(columns)

    def _create_gui_part_1(self):
        self._create_buttons()

    def create_gui_part_2(self):
        if self.bookmark_list is None:
            self._create_bookmark_list()
            self._layout()
            self.applyTheme()

    def _layout(self):
        assert self.bookmark_list is not None

        main_sizer = wx.FlexGridSizer(cols=2)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(0)
        self.SetSizer(main_sizer)

        # Buttons
        buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer.Add(self.move_up_btn, flag=wx.ALL, border=2)
        buttons_sizer.Add(self.move_down_btn, flag=wx.ALL, border=2)
        buttons_sizer.Add(self.remove_btn, flag=wx.ALL, border=2)

        main_sizer.Add(self.bookmark_list, flag=wx.EXPAND)
        main_sizer.Add(buttons_sizer, flag=wx.ALL, border=2)

        self.Layout()
