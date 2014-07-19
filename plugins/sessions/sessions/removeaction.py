# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from .i18n import get_
from .sessionstorage import SessionStorage


class RemoveSessionAction (BaseAction):
    """
    Действие для удаления сессии
    """
    def __init__ (self, application, guicreator):
        self._application = application
        self._guicreator = guicreator

        global _
        _ = get_()

    stringId = u"Sessions_RemoveSession"


    @property
    def title (self):
        return _(u"Remove session...")


    @property
    def description (self):
        return _(u"Remove session")


    def run (self, params):
        storage = SessionStorage (self._application.config)
        names = sorted (storage.getSessions().keys())

        if len (names) == 0:
            MessageBox (_(u"Not created any session"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        with RemoveSessionDialog (self._application.mainWindow, self._application, names) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                storage.remove (dlg.sessionName)
                self._guicreator.updateMenu()


class RemoveSessionDialog (TestedDialog):
    def __init__ (self, parent, application, names):
        """
        parent - родительское окно
        application - экземпляр класса Application
        names - список имен существующих сессий
        """
        super (RemoveSessionDialog, self).__init__(parent)
        assert len (names) != 0

        self._application = application
        self._names = names

        self.SetTitle (_(u"Remove Session"))
        self.__createGui ()
        self._sessionComboBox.SetFocus()

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)


    def __onOk (self, event):
        assert self.sessionName in self._names

        name = self.sessionName

        if len (name.strip()) == 0:
            MessageBox (_(u"The session name must not be empty"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        if (MessageBox (_(u'Remove session "{}"?').format (name),
                        _(u"Remove session?"),
                        wx.ICON_QUESTION | wx.YES | wx.NO) != wx.YES):
            return

        event.Skip()


    def __createGui (self):
        sessionNameLabel = wx.StaticText (self, label = _(u"Select session name"))
        self._sessionComboBox = wx.ComboBox (self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self._sessionComboBox.SetMinSize ((200, -1))
        self._sessionComboBox.Clear()
        self._sessionComboBox.AppendItems (self._names)
        self._sessionComboBox.SetSelection (0)

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
