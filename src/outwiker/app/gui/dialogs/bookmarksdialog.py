import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.images import readImage
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.theme import Theme


class BookmarksDialog(TestedDialog):
    def __init__(self, parent: wx.Window, theme: Theme):
        super().__init__(parent, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetTitle(_("Bookmark management"))
        self._theme = theme
        self._create_gui()

    def _create_gui(self):
        button_height = wx.Button.GetDefaultSize().height
        button_width = button_height
        icon_size = (
            button_height
            - self._theme.get(Theme.SECTION_GENERAL, Theme.BITMAP_BUTTON_PADDING) * 2
        )

        # Bookmarks list
        self.bookmarks_list = wx.ListBox(self)

        # Move up button
        self.move_up_btn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("arrow_up.svg"), icon_size, icon_size
            ),
        )
        self.move_up_btn.SetMinSize(wx.Size(button_width, button_height))
        self.move_up_btn.SetToolTip(_("Move bookmark up"))
        self.move_up_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveUp)

        # Move down button
        self.move_down_btn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("arrow_down.svg"), icon_size, icon_size
            ),
        )
        self.move_down_btn.SetMinSize(wx.Size(button_width, button_height))
        self.move_down_btn.SetToolTip(_("Move bookmark down"))
        self.move_down_btn.Bind(wx.EVT_BUTTON, handler=self._onMoveDown)

        # Remove button
        self.remove_btn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("remove.svg"), icon_size, icon_size
            ),
        )
        self.remove_btn.SetMinSize(wx.Size(button_width, button_height))
        self.remove_btn.SetToolTip(_("Remove bookmark"))
        self.remove_btn.Bind(wx.EVT_BUTTON, handler=self._onRemove)

        # OK / Cancel buttons
        self._ok_cancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
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
        list_sizer.Add(self.bookmarks_list, flag=wx.EXPAND)
        list_sizer.Add(buttons_sizer, flag=wx.ALL, border=2)

        main_sizer.Add(list_sizer, flag=wx.EXPAND)
        main_sizer.Add(self._ok_cancel, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)

        self.SetSize(wx.Size(500, 400))
        self.Layout()

    def _onMoveUp(self, event):
        print("Move up")

    def _onMoveDown(self, event):
        print("Move down")

    def _onRemove(self, event):
        print("Remove")
