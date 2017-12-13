# -*- coding: UTF-8 -*-

# This file was copied from outwiker/gui/dialogs to
# maintain backward compatibility with OutWiker 1.9

import wx

from outwiker.gui.testeddialog import TestedDialog


class ButtonsDialog(TestedDialog):
    """
    Added in outwiker.gui 1.5

    The dialog with the custom buttons.
    The ShowModal method return number of the button (begins with 0).

    Version 1.1
    """
    def __init__(self, parent, message, caption, buttons,
                 default=0, cancel=-1):
        """
        parent - parent window
        message - text message to show in the dialog.
        caption - dialog title.
        buttons - list of the strings for buttons.
        default - default button number.
        cancel - button number which is triggered by pressing the Esc
        """
        assert len(buttons) > 0
        assert default < len(buttons)
        assert cancel < len(buttons)

        self.ID_MIN = wx.ID_HIGHEST + 1

        super(ButtonsDialog, self).__init__(parent)

        self.__default = default
        self.__cancel = cancel

        self.SetTitle(caption)
        self.__textLabel = wx.StaticText(self,
                                         -1,
                                         message,
                                         style=wx.ALIGN_CENTRE)

        self.__createButtons(buttons, default, cancel)
        self.__do_layout()
        self.Center(wx.BOTH)

    def __createButtons(self, buttons, default, cancel):
        self.__buttons = [wx.Button(self, self.ID_MIN + index, text)
                          for text, index
                          in zip(buttons, list(range(len(buttons))))]

        if default >= 0:
            default_id = self.__buttons[default].GetId() + self.ID_MIN
            self.SetAffirmativeId(default_id)
            self.__buttons[default].SetFocus()

        if cancel >= 0:
            cancel_id = self.__buttons[cancel].GetId() + self.ID_MIN
            self.SetEscapeId(cancel_id)

        self.__assignHotKeys()
        self.Bind(wx.EVT_BUTTON, self.__onButton)
        self.Bind(wx.EVT_MENU, self.__onButton)

    def __assignHotKeys(self):
        count = min(9, len(self.__buttons))
        entries = [wx.AcceleratorEntry() for n in range(count + 1)]

        for n in range(count):
            if n <= 9:
                entries[n].Set(0, ord('1') + n, self.ID_MIN + n)
                text = u'{n}. {title}'.format(
                    n=n + 1,
                    title=self.__buttons[n].GetLabel())
                self.__buttons[n].SetLabel(text)

        entries[count].Set(0, wx.WXK_ESCAPE, wx.ID_CANCEL)

        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)

    def __onButton(self, event):
        self.EndModal(event.GetId() - self.ID_MIN)

    def __do_layout(self):
        sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_1.AddGrowableCol(0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(
            self.__textLabel,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            border=8)

        for button in self.__buttons:
            sizer_2.Add(button, 0, wx.ALL, border=4)

        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=2)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
