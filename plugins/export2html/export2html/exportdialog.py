#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import abstractmethod, ABCMeta

import wx

from outwiker.core.commands import MessageBox

from .exportconfig import ExportConfig


class ExportDialog (wx.Dialog):
    __metaclass__ = ABCMeta

    def __init__ (self, parent, config):
        from .i18n import _
        global _

        self._config = ExportConfig (config)

        wx.Dialog.__init__ (self, parent, title=_(u"Export"), style=wx.DEFAULT_DIALOG_STYLE)

        self.__SEL_FOLDER = wx.NewId()

        self.__folderLabel = wx.StaticText (self, -1, _(u"Folder for Export:"))
        self.__folderTextCtrl = wx.TextCtrl (self)

        textBoxWidth = 350
        self.__folderTextCtrl.SetMinSize ((textBoxWidth, -1))

        self.__selFolderButton = wx.Button (self, 
                self.__SEL_FOLDER,
                label=u"...",
                style=wx.BU_EXACTFIT)

        self.__overwriteCheckBox = wx.CheckBox (self, -1, _(u"Overwrite Existing Files"))
        self.__imagesOnlyCheckBox = wx.CheckBox (self, -1, _(u"Attaches. Save Only Images"))
        self.__buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)

        self.__layout()
        self.__centerWindow()

        self.Bind (wx.EVT_BUTTON, self.__onSelFolder, self.__selFolderButton)
        self.Bind (wx.EVT_BUTTON, self.__onOkPressed, id=wx.ID_OK)

        self.__loadParams ()
        self._setFocusDefault()

    
    def __loadParams (self):
        self.overwrite = self._config.overwrite
        self.imagesOnly = self._config.imagesOnly


    def _setFocusDefault (self):
        self.__folderTextCtrl.SetFocus()

    
    def __centerWindow (self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self.GetSize()

        parentWidth, parentHeight = self.GetParent().GetSize()
        parentX, parentY = self.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self.SetPosition ((posX, posY))
    


    @property
    def path (self):
        return self.__folderTextCtrl.GetValue().strip()


    @path.setter
    def path (self, value):
        self.__folderTextCtrl.SetValue (value)


    @property
    def overwrite (self):
        return self.__overwriteCheckBox.GetValue()


    @overwrite.setter
    def overwrite (self, value):
        self.__overwriteCheckBox.SetValue (value)


    @property
    def imagesOnly (self):
        return self.__imagesOnlyCheckBox.GetValue()


    @imagesOnly.setter
    def imagesOnly (self, value):
        self.__imagesOnlyCheckBox.SetValue (value)


    def __onOkPressed (self, event):
        if len (self.path) == 0:
            MessageBox (_(u"Please, select folder for export"), 
                    _(u"Error"),
                    wx.OK | wx.ICON_ERROR )
            self._setFocusDefault()
            return

        self._onOk()


    @abstractmethod
    def _onOk(self):
        pass


    def __onSelFolder (self, event):
        dlg = wx.DirDialog (self)
        if dlg.ShowModal() == wx.ID_OK:
            self.__folderTextCtrl.SetValue (dlg.GetPath())


    def __layout (self):
        folderSizer = wx.FlexGridSizer (rows=1, cols=2)
        folderSizer.AddGrowableCol (0)
        folderSizer.Add (self.__folderTextCtrl, flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        folderSizer.Add (self.__selFolderButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)


        self._mainSizer = wx.FlexGridSizer (rows=0, cols=1)
        self._mainSizer.AddGrowableCol (0)
        self._mainSizer.Add (self.__folderLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add (folderSizer, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=2)
        self._mainSizer.Add (self.__overwriteCheckBox, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add (self.__imagesOnlyCheckBox, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add (self.__buttonsSizer, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)

        self.SetSizer (self._mainSizer)
        self.Fit()
        self.Layout()

