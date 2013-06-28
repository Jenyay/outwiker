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
        
        self.SetMinSize ((500, 500))
        self._createGui ()


    def _getOutWikerVersionString (self, version):
        """
        Установить строку для показа номера текущей версии OutWiker
        """
        return _(u"Current OutWiker version is ").format (version)


    def _createGui (self):
        self._mainSizer = wx.FlexGridSizer (cols=1)
        self._mainSizer.AddGrowableCol (0)

        # Строка с текущей версией OutWiker
        self.outwikerCurrentLabel = wx.StaticText (self, -1, u"")
        self._mainSizer.Add (self.outwikerCurrentLabel, 1, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

        # Строка с последней стабильной версией OutWiker
        self.outwikerStableLabel = wx.StaticText (self, -1, u"")
        self.outwikerStableLink = wx.HyperlinkCtrl (self, -1, _("Update..."), url=_(u"http://jenyay.net/Outwiker/English"))
        self.outwikerStableLink.Show (False)

        outwikerStableSizer = wx.FlexGridSizer (cols=2)
        outwikerStableSizer.AddGrowableCol (0)
        outwikerStableSizer.AddGrowableCol (1)

        outwikerStableSizer.Add (self.outwikerStableLabel, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, border=4)
        outwikerStableSizer.Add (self.outwikerStableLink, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, border=4)

        self._mainSizer.Add (outwikerStableSizer, flag=wx.ALL | wx.EXPAND, border=0)

        # Строка с последней нестабильной версией OutWiker
        self.outwikerUnstableLabel = wx.StaticText (self, -1, u"")
        self.outwikerUnstableLink = wx.HyperlinkCtrl (self, -1, _("Update..."), url=_(u"http://jenyay.net/Outwiker/UnstableEn"))
        self.outwikerUnstableLink.Show (False)

        outwikerUnstableSizer = wx.FlexGridSizer (cols=2)
        outwikerUnstableSizer.AddGrowableCol (0)
        outwikerUnstableSizer.AddGrowableCol (1)

        outwikerUnstableSizer.Add (self.outwikerUnstableLabel, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, border=4)
        outwikerUnstableSizer.Add (self.outwikerUnstableLink, 1, flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, border=4)

        self._mainSizer.Add (outwikerUnstableSizer, flag=wx.ALL | wx.EXPAND, border=0)

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
        self.outwikerCurrentLabel.SetLabel (_(u"Current OutWiker version is {0}").format (version) )
        self.Fit()
        self.Layout()


    def setLatestStableOutwikerVersion (self, version):
        """
        Установить в диалоге номер последней стабильной версии
        """
        self.outwikerStableLabel.SetLabel (u"Latest stable OutWiker version: {0}".format (version))
        self.Fit()
        self.Layout()


    def showUpdateStableOutWiker (self, show=True):
        self.outwikerStableLink.Show (show)
        self.Layout()


    def setLatestUnstableOutwikerVersion (self, version):
        """
        Установить в диалоге номер последней нестабильной версии
        """
        self.outwikerUnstableLabel.SetLabel (u"Latest unstable OutWiker version: {0}".format (version))
        self.Fit()
        self.Layout()


    def showUpdateUnstableOutWiker (self, show=True):
        self.outwikerUnstableLink.Show (show)
        self.Fit()
        self.Layout()

