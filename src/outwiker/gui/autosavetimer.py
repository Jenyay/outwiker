# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.guiconfig import GeneralGuiConfig


class AutosaveTimer (wx.PyEvtHandler):
    """
    Класс для автосохранения по таймеру
    """
    def __init__ (self, application):
        wx.PyEvtHandler.__init__ (self)

        self.__application = application
        self.__guiconfig = GeneralGuiConfig (self.__application.config)

        self.__application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self.__application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        self.Bind (wx.EVT_TIMER, self.__onTick)

        self.__timer = wx.Timer (self)
        self.__setTimer()


    def __onPreferencesDialogCreate (self, dialog):
        """
        На время показа диалога с настройками отключим таймер
        """
        self.__timer.Stop()


    def __onPreferencesDialogClose (self, dialog):
        self.__setTimer()


    def __setTimer (self):
        interval = self.__guiconfig.autosaveInterval.value

        if interval > 0:
            self.__timer.Start (interval * 1000)


    def __onTick (self, event):
        """
        Этот метод вызывается, когда срабатывает таймер
        """
        # Если приложение не активно, ничего не сохраняем,
        # потому что все-равно при неактивном окне заметка
        # не может измениться средствами outwiker'а.
        # А при потере фокуса сохранение происходит и так.
        if wx.GetApp().IsActive():
            self.__application.onForceSave()


    def Destroy (self):
        self.__timer.Stop()

        self.__application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self.__application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        self.Unbind (wx.EVT_TIMER, self.__onTick)
