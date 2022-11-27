# -*- coding: utf-8 -*-

import wx

from . import configelements
from outwiker.gui.guiconfig import TrayConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class TrayPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super(TrayPanel, self).__init__(parent)
        self._minimize_button_actions = [_('Minimize window'), _('Hide to tray') ]
        self._close_button_actions = [_('Close window'), _('Minimize window'), _('Hide to tray') ]

        self.trayConfig = TrayConfig(application.config)
        self._createTrayGui()

        self._set_properties()
        self._layout()

        self.Bind(wx.EVT_COMBOBOX,
                  self.onMinimizeToTray,
                  self.minimizeComboBox)

        self.LoadState()
        self.updateCheckState()
        self.SetupScrolling()

    def _set_properties(self):
        DEFAULT_WIDTH = 520
        DEFAULT_HEIGHT = 420

        self.SetSize((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.SetFocus()
        self.SetScrollRate(0, 0)

    def _createMainWindowButtonsGui(self) -> None:
        self._buttons_sizer = wx.FlexGridSizer(cols=2)
        self._buttons_sizer.AddGrowableCol(1)

        # Minimize button actions
        minimizeButtonLabel = wx.StaticText(self, label=_('Minimize window button'))
        self.minimizeComboBox = wx.ComboBox(self, style=wx.CB_READONLY)

        self._buttons_sizer.Add(minimizeButtonLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        self._buttons_sizer.Add(self.minimizeComboBox, flag=wx.ALIGN_RIGHT | wx.ALL, border=2)

        # Close button actions
        closeButtonLabel = wx.StaticText(self, label=_('Close window button'))
        self.closeComboBox = wx.ComboBox(self, style=wx.CB_READONLY)

        self._buttons_sizer.Add(closeButtonLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        self._buttons_sizer.Add(self.closeComboBox, flag=wx.ALIGN_RIGHT | wx.ALL, border=2)

    def _createTrayGui(self):
        """
        Создать элементы интерфейса, связанные с треем
        """
        self._createMainWindowButtonsGui()

        self.startIconizedCheckBox = wx.CheckBox(
            self,
            -1,
            _("Start iconized"))

        self.alwaysInTrayCheckBox = wx.CheckBox(
            self,
            -1,
            _("Always show tray icon"))

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.Add(self._buttons_sizer, flag=wx.EXPAND | wx.ALL, border=2)

        main_sizer.Add(self.startIconizedCheckBox, 0, wx.ALL, 2)
        main_sizer.Add(self.alwaysInTrayCheckBox, 0, wx.ALL, 2)

        self.SetSizer(main_sizer)

    def LoadState(self):
        """
        Загрузить состояние страницы из конфига
        """
        # Action for the minimize button
        self.minimizeButtonActions = configelements.ComboBoxListElement(
                self.trayConfig.minimizeToTray,
                self.minimizeComboBox,
                self._minimize_button_actions
                )

        # Action for the close button
        self.closeButtonActions = configelements.ComboBoxListElement(
                self.trayConfig.closeButtonAction,
                self.closeComboBox,
                self._close_button_actions
                )

        # Всегда показывать иконку в трее
        self.alwaysInTray = configelements.BooleanElement(
            self.trayConfig.alwaysShowTrayIcon,
            self.alwaysInTrayCheckBox
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
        self.minimizeButtonActions.save()
        self.closeButtonActions.save()
        self.alwaysInTray.save()

    def onMinimizeToTray(self, event):
        self.updateCheckState()

    def updateCheckState(self):
        """
        Обновить состояния чекбоксов
        """
        if self.minimizeComboBox.GetSelection() == 0:
            self.startIconizedCheckBox.SetValue(False)
            self.startIconizedCheckBox.Disable()
        else:
            self.startIconizedCheckBox.Enable()
