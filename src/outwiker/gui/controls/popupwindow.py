# -*- coding: utf-8 -*-

import wx


class PopupWindow(wx.PopupTransientWindow):
    '''
    Popup window with accurate position
    '''
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self._mainWindow = mainWindow
        self.createGUI()

    def createGUI(self):
        pass

    def Popup(self):
        self.Dismiss()
        self.Layout()
        self.SetPosition(self._getBestPosition())
        super().Popup()

    def _getBestPosition(self):
        """
        Рассчитывает координаты окна таким образом, чтобы оно было около
        курсора, но не вылезало за пределы окна
        """
        mousePosition = wx.GetMousePosition()

        width, height = self.GetSize()
        parent_window_rect = self._mainWindow.GetScreenRect()

        if mousePosition.x < parent_window_rect.x + parent_window_rect.width / 2:
            popup_x = mousePosition.x
        else:
            popup_x = mousePosition.x - width

        if mousePosition.y < parent_window_rect.y + parent_window_rect.height / 2:
            popup_y = mousePosition.y
        else:
            popup_y = mousePosition.y - height

        return (popup_x, popup_y)
