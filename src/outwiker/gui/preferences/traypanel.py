# -*- coding: utf-8 -*-

import wx

from . import configelements
from outwiker.core.application import Application
from outwiker.gui.guiconfig import TrayConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class TrayPanel(BasePrefPanel):
    def __init__(self, parent):
        super(TrayPanel, self).__init__(parent)

        self.trayConfig = TrayConfig(Application.config)
        self.__createTrayGui()

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX,
                  self.onMinimizeToTray,
                  self.minimizeCheckBox)

        self.LoadState()
        self.updateCheckState()
        self._setScrolling()

    def __set_properties(self):
        DEFAULT_WIDTH = 520
        DEFAULT_HEIGHT = 420

        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.SetFocus()
        self.SetScrollRate(0, 0)

    def __createTrayGui(self):
        """
        Создать элементы интерфейса, связанные с треем
        """
        self.minimizeCheckBox = wx.CheckBox(
            self,
            -1,
            _("Minimize to tray"))

        self.startIconizedCheckBox = wx.CheckBox(
            self,
            -1,
            _("Start iconized"))

        self.alwaysInTrayCheckBox = wx.CheckBox(
            self,
            -1,
            _("Always show tray icon"))

        self.minimizeOnCloseCheckBox = wx.CheckBox(
            self,
            -1,
            _("Minimize on close window"))

    def __addStaticLine(self, main_sizer):
        static_line = wx.StaticLine(self, -1)
        main_sizer.Add(static_line, 0, wx.EXPAND, 0)

    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        main_sizer.Add(self.minimizeCheckBox,
                       0,
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       2)

        main_sizer.Add(self.startIconizedCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.alwaysInTrayCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.minimizeOnCloseCheckBox, 0, wx.ALL, 2)

        self.SetSizer(main_sizer)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        # Сворачивать в трей?
        self.minimizeToTray = configelements.BooleanElement(
            self.trayConfig.minimizeToTray,
            self.minimizeCheckBox
        )

        # Всегда показывать иконку в трее
        self.alwaysInTray = configelements.BooleanElement(
            self.trayConfig.alwaysShowTrayIcon,
            self.alwaysInTrayCheckBox
        )

        # Сворачивать при закрытии
        self.minimizeOnClose = configelements.BooleanElement(
            self.trayConfig.minimizeOnClose,
            self.minimizeOnCloseCheckBox
        )

        # Запускаться свернутым?
        self.startIconized = configelements.BooleanElement(
            self.trayConfig.startIconized,
            self.startIconizedCheckBox
        )

    def Save(self):
        """
        Сохранить состояние страницы в конфиг
        """
        self.startIconized.save()
        self.minimizeToTray.save()
        self.minimizeOnClose.save()
        self.alwaysInTray.save()

    def onMinimizeToTray(self, event):
        self.updateCheckState()

    def updateCheckState(self):
        """
        Обновить стостояния чекбоксов
        """
        if not self.minimizeCheckBox.IsChecked():
            self.startIconizedCheckBox.SetValue(False)
            self.startIconizedCheckBox.Disable()
        else:
            self.startIconizedCheckBox.Enable()
