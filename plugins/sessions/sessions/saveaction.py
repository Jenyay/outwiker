# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from .i18n import get_
from .sessionstorage import SessionStorage
from .sessioncontroller import SessionController


class SaveSessionAction (BaseAction):
    """
    Действие для сохранения сессии
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Sessions_SaveSession"


    @property
    def title (self):
        return _(u"Save session...")


    @property
    def description (self):
        return _(u"Save currently opened tabs")


    def run (self, params):
        storage = SessionStorage (self._application.config)
        names = sorted (storage.getSessions().keys())

        with SaveSessionDialog (self._application.mainWindow, self._application, names) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                session = SessionController(self._application).getCurrentSession()
                storage.save (session, dlg.sessionName)


class SaveSessionDialog (TestedDialog):
    def __init__ (self, parent, application, names):
        """
        parent - родительское окно
        application - экземпляр класса Application
        names - список имен существующих сессий
        """
        super (SaveSessionDialog, self).__init__(parent)

        self._application = application
        self._names = names

        self.SetTitle (_(u"Save Session"))
        self.__createGui ()
        self._sessionComboBox.SetFocus()

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)


    def __onOk (self, event):
        name = self.sessionName
        if len (name.strip()) == 0:
            MessageBox (_(u"The session name must not be empty"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        if (name in self._names and
            MessageBox (_(u'Session with name "{}" exists. Overwrite?').format (name),
                        _(u"Overwrite session?"),
                        wx.ICON_QUESTION | wx.YES | wx.NO) != wx.YES):
            return

        event.Skip()


    def __createGui (self):
        sessionNameLabel = wx.StaticText (self, label = _(u"Enter session name"))
        self._sessionComboBox = wx.ComboBox (self, style=wx.CB_DROPDOWN)
        self._sessionComboBox.SetMinSize ((200, -1))
        self._sessionComboBox.Clear()
        self._sessionComboBox.AppendItems (self._names)

        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)

        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (1)
        mainSizer.Add (sessionNameLabel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        mainSizer.Add (self._sessionComboBox, 1, wx.EXPAND | wx.ALL, border=2)
        mainSizer.AddSpacer (1)
        mainSizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)

        self.SetSizer (mainSizer)
        self.Fit()


    @property
    def sessionName (self):
        return self._sessionComboBox.GetValue()
