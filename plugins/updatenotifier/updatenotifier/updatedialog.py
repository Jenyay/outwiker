#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class UpdateDialog(wx.Dialog):
    """Диалог для показа списка обновленных плагинов"""
    def __init__(self, parent):
        super(UpdateDialog, self).__init__(parent)

        global _
        _ = get_()
        
        self._createGui ()


    def _createGui (self):
        self._mainSizer = wx.FlexGridSizer (cols=1)
        self._mainSizer.AddGrowableCol (0)

        outwikerCurrentLabel = wx.StaticText (self, -1, _(u"Current OutWiker Version"))

        self.SetSizer (self._mainSizer)
        self.Fit()


    def addPluginInfo (self, plugin, newversion):
        """
        Добавить информацию об обновленном плагине
        """
        print u"{0}. Current version: {1}. New version: {2}".format (plugin.name, plugin.version, newversion)


    def setCurrentOutWikerVersion (self, version):
        """
        Установить в диалоге номер текущей версии OutWiker
        """
        print u"Current OutWiker version: {0}".format (version)


    def setLatestStableOutwikerVersion (self, version):
        """
        Установить в диалоге номер последней стабильной версии
        """
        print u"Latest stable OutWiker version: {0}".format (version)


    def setLatestUnstableOutwikerVersion (self, version):
        """
        Установить в диалоге номер последней нестабильной версии
        """
        print u"Latest unstable OutWiker version: {0}".format (version)

