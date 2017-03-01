# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class ButtonsDialog(TestedDialog):
    """
    Added in outwiker.gui 1.5

    The dialog with the custom buttons.
    The ShowModal method return number of the button (begins with 0).
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
        self.Center(wx.CENTRE_ON_SCREEN)

    def __createButtons(self, buttons, default, cancel):
        self.__buttons = [wx.Button(self, index, text)
                          for text, index
                          in zip(buttons, range(len(buttons)))]

        if default >= 0:
            self.SetAffirmativeId(self.__buttons[default].GetId())
            self.__buttons[default].SetFocus()

        if cancel >= 0:
            self.SetEscapeId(self.__buttons[cancel].GetId())

        self.Bind(wx.EVT_BUTTON, self.__onButton)

    def __onButton(self, event):
        self.EndModal(event.GetId())

    def __do_layout(self):
        sizer_1 = wx.FlexGridSizer(2, 1)
        sizer_1.AddGrowableCol(0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(
            self.__textLabel,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            4)

        for button in self.__buttons:
            sizer_2.Add(button, 0, wx.ALL, 2)

        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
