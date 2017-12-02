# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from .i18n import get_
from .sessionstorage import SessionStorage
from .misc import getImagePath


class EditSessionsAction (BaseAction):
    """
    Действие для вызова диалога редактирования сессий
    """
    def __init__ (self, application, guicreator):
        self._application = application
        self._guicreator = guicreator

        global _
        _ = get_()

    stringId = u"Sessions_EditSession"


    @property
    def title (self):
        return _(u"Edit sessions...")


    @property
    def description (self):
        return _(u"Edit (rename or delete) sessions")


    def run (self, params):
        storage = SessionStorage (self._application.config)
        names = sorted (storage.getSessions().keys())

        if len (names) == 0:
            MessageBox (_(u"Not created any session"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        with EditSessionsDialog (self._application.mainWindow,
                                 self._application,
                                 self._guicreator) as dlg:
            dlg.ShowModal()


class EditSessionsDialog (TestedDialog):
    def __init__ (self, parent, application, guicreator):
        """
        parent - родительское окно
        application - экземпляр класса Application
        guicreator - экземпляр класса GuiCreator
        """
        super (EditSessionsDialog, self).__init__(parent,
                                                  style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self._application = application
        self._guicreator = guicreator

        self._storage = SessionStorage (self._application.config)

        self.RENAME_ID = wx.NewId()
        self.REMOVE_ID = wx.NewId()

        self.SetTitle (_(u"Edit Sessions"))
        self.__createGui ()

        self._updateSessionsList ()
        self.Center(wx.BOTH)
        self.SetSize ((350, 250))

        self.Bind (wx.EVT_BUTTON, handler=self._onRemove, id=self.REMOVE_ID)
        self.Bind (wx.EVT_BUTTON, handler=self._onRename, id=self.RENAME_ID)


    def _updateSessionsList (self):
        names = sorted (self._storage.getSessions().keys())
        self._actionsList.Clear()
        self._actionsList.AppendItems (names)


    def _onRemove (self, event):
        name = self._actionsList.GetStringSelection()
        if len (name) == 0:
            return

        if (MessageBox (_(u'Remove session "{}"?').format (name),
                        _(u"Remove session?"),
                        wx.ICON_QUESTION | wx.YES | wx.NO) == wx.YES):
            self._storage.remove (name)
            self._updateSessionsList()
            self._guicreator.updateMenu()


    def _onRename (self, event):
        name = self._actionsList.GetStringSelection()
        if len (name) == 0:
            return

        with wx.TextEntryDialog (self,
                                 _(u"Enter new session name"),
                                 _(u"Rename session"),
                                 name) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                newname = dlg.GetValue().strip()

                if len (newname) == 0:
                    MessageBox (_(u'Session name is empty').format (newname),
                                _(u"Invalid session name"),
                                wx.ICON_ERROR | wx.OK)
                    return

                # Проверим, что не ввели имя сессии, совпадающее с существующей
                # сессией (кроме случая, что не изменили имя)
                if (newname != name and
                        newname in self._storage.getSessions()):
                    MessageBox (_(u'Session "{}" already exists').format (newname),
                                _(u"Invalid session name"),
                                wx.ICON_ERROR | wx.OK)
                    return

                self._storage.rename (name, newname)
                self._updateSessionsList()
                self._guicreator.updateMenu()


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (rows=2)
        mainSizer.AddGrowableRow (0)
        mainSizer.AddGrowableCol (0)

        actionsSizer = wx.FlexGridSizer (cols=2)
        actionsSizer.AddGrowableCol (0)
        actionsSizer.AddGrowableRow (0)

        self._actionsList = wx.ListBox (self)
        self._actionsList.SetMinSize ((250, 150))

        mainButtonsSizer = wx.BoxSizer (wx.VERTICAL)

        self._renameButton = wx.BitmapButton (self,
                                              self.RENAME_ID,
                                              wx.Bitmap (getImagePath (u"rename.png")))

        self._renameButton.SetToolTip (_(u"Rename session..."))

        self._removeButton = wx.BitmapButton (self,
                                              self.REMOVE_ID,
                                              wx.Bitmap (getImagePath (u"remove.png")))

        self._removeButton.SetToolTip (_(u"Remove session..."))

        mainButtonsSizer.Add (self._renameButton, 0, wx.ALL, border=2)
        mainButtonsSizer.Add (self._removeButton, 0, wx.ALL, border=2)

        actionsSizer.Add (self._actionsList, 1, wx.EXPAND | wx.ALL, border = 2)
        actionsSizer.Add (mainButtonsSizer, 1, wx.ALL, border = 2)

        buttonsSizer = self.CreateButtonSizer (wx.OK)
        mainSizer.Add (actionsSizer, 1, wx.EXPAND | wx.ALL, border = 2)
        mainSizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)

        self.SetSizer (mainSizer)
        self.Fit()


    @property
    def sessionName (self):
        return self._sessionComboBox.GetValue()
