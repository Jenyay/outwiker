from typing import Tuple

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from outwiker.gui.controls.treebook2 import Treebook2
from outwiker.gui.controls.colorcombobox import ColorComboBox


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
        sizer.Add(label, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        sizer.Add(control, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)

    def _createLabelAndSpin(
        self, title: str, minVal: int, maxVal: int, sizer: wx.Sizer
    ) -> Tuple[wx.StaticText, wx.SpinCtrl]:
        label = wx.StaticText(self, label=title)
        spin = wx.SpinCtrl(self, min=minVal, max=maxVal)
        spin.SetMinSize((150, -1))
        self._addLabelAndControlToSizer(sizer, label, spin)
        return (label, spin)

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

    def _createLabelAndColorComboBox(
        self, title: str, sizer: wx.Sizer
    ) -> Tuple[wx.StaticText, ColorComboBox]:
        label = wx.StaticText(self, label=title)
        colorComboBox = ColorComboBox(self)
        colorComboBox.SetMinSize((200, -1))

        self._addLabelAndControlToSizer(sizer, label, colorComboBox)
        return (label, colorComboBox)

    def _createCheckBox(self, title: str, sizer: wx.Sizer) -> wx.CheckBox:
        checkBox = wx.CheckBox(self, label=title)
        sizer.Add(checkBox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        return checkBox

    def _createSection(
        self,
        main_sizer: wx.Sizer,
        title: str,
        cols: int = 2,
    ) -> Tuple[wx.StaticBox, wx.Sizer]:
        """
        Create StaticBox for options
        """
        staticBox = wx.StaticBox(self, label=title)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)

        sizer = wx.FlexGridSizer(cols=cols)
        for n in range(cols):
            sizer.AddGrowableCol(n)

        staticBoxSizer.Add(sizer, flag=wx.EXPAND)
        main_sizer.Add(staticBoxSizer, flag=wx.EXPAND | wx.ALL, border=2)
        return (staticBox, sizer)
