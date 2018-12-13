# -*- coding: utf-8 -*-

from typing import Tuple

import wx


class PopupMixin:
    def getBestPosition(self, mainWindow) -> Tuple[int, int]:
        """
        Рассчитывает координаты окна таким образом, чтобы оно было около
        курсора, но не вылезало за пределы окна
        """
        mousePosition = wx.GetMousePosition()

        width, height = self.GetSize()
        parent_window_rect = mainWindow.GetScreenRect()

        if mousePosition.x < parent_window_rect.x + parent_window_rect.width / 2:
            popup_x = mousePosition.x
        else:
            popup_x = mousePosition.x - width

        if mousePosition.y < parent_window_rect.y + parent_window_rect.height / 2:
            popup_y = mousePosition.y
        else:
            popup_y = mousePosition.y - height

        return (popup_x, popup_y)


class PopupWindow(PopupMixin, wx.PopupTransientWindow):
    '''
    Popup window with accurate position
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.createGUI()

    def createGUI(self):
        pass

    def Popup(self, mainWindow):
        self.Dismiss()
        self.Layout()
        self.SetPosition(self.getBestPosition(mainWindow))
        super().Popup()


class ResizablePopupWindow(PopupMixin, wx.MiniFrame):
    '''
    Popup window with accurate position
    '''
    def __init__(self, parent):
        super().__init__(
            parent,
            style=wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT)

        # To skip closing after deactivate
        self._skipDeactivateCount = 0

        self.createGUI()
        self.Bind(wx.EVT_CLOSE, handler=self._onClose)
        self.Bind(wx.EVT_ACTIVATE, handler=self._onActivate)

    def setDeactivateCount(self, value: int):
        '''
        value - How many times to skip deactivate
        '''
        self._skipDeactivateCount = value

    def _onActivate(self, event: wx.ActivateEvent):
        if not event.GetActive():
            if self._skipDeactivateCount > 0:
                self._skipDeactivateCount -= 1
            else:
                self.Close()

    def _onClose(self, event):
        self.Hide()

    def createGUI(self):
        pass

    def Popup(self, mainWindow):
        self.SetPosition(self.getBestPosition(mainWindow))
        self.Show()
        self.Raise()
