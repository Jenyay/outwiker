#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_
from .scrolledpanel import ScrolledPanel


class UpdateDialog(wx.Dialog):
    """Диалог для показа списка обновленных плагинов"""
    def __init__(self, parent):
        super(UpdateDialog, self).__init__(parent, 
                style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME)

        global _
        _ = get_()

        self._activeUrlColor = wx.BLUE
        self._inactiveUrlColor = wx.BLACK
        
        self.SetSize ((500, 400))
        self.SetTitle (_(u"UpdateNotifier"))
        self._createGui ()


    def _createOutWikerCurrentVersionGui (self, sizer):
        """
        Создание интерфейса для показа текущей версии OutWiker
        """
        self.outwikerCurrentLabel = wx.StaticText (self, -1, _(u"Current OutWiker version"))
        self.outwikerCurrentVersion = wx.StaticText (self, -1, u"")

        outwikerCurrentSizer = wx.FlexGridSizer (cols=2)
        outwikerCurrentSizer.AddGrowableCol (1)

        outwikerCurrentSizer.Add (self.outwikerCurrentLabel, 
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border=4)

        outwikerCurrentSizer.Add (self.outwikerCurrentVersion,
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_RIGHT, 
                border=4)

        sizer.Add (outwikerCurrentSizer, flag=wx.ALL | wx.EXPAND, border=0)


    def _createOutWikerStableVersionGui (self, sizer):
        """
        Создание интерфейса для показа последней стабильной версии OutWiker
        """
        self.outwikerStableLabel = wx.StaticText (self, -1, u"Latest stable OutWiker version")
        self.outwikerStableLink = wx.HyperlinkCtrl (self, -1, _("Update..."), url=_(u"http://jenyay.net/Outwiker/English"))

        outwikerStableSizer = wx.FlexGridSizer (cols=2)
        outwikerStableSizer.AddGrowableCol (1)

        outwikerStableSizer.Add (self.outwikerStableLabel, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL, 
                border=4)

        outwikerStableSizer.Add (self.outwikerStableLink, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_RIGHT, 
                border=4)

        sizer.Add (outwikerStableSizer, flag=wx.ALL | wx.EXPAND, border=0)


    def _createOutWikerUnstableVersionGui (self, sizer):
        """
        Создание интерфейса для показа последней нестабильной версии OutWiker
        """
        self.outwikerUnstableLabel = wx.StaticText (self, -1, u"Latest unstable OutWiker version")
        self.outwikerUnstableLink = wx.HyperlinkCtrl (self, -1, _("Update..."), url=_(u"http://jenyay.net/Outwiker/UnstableEn"))

        outwikerUnstableSizer = wx.FlexGridSizer (cols=2)
        outwikerUnstableSizer.AddGrowableCol (0)

        outwikerUnstableSizer.Add (self.outwikerUnstableLabel, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL, 
                border=4)

        outwikerUnstableSizer.Add (self.outwikerUnstableLink, 
                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_RIGHT, 
                border=4)

        sizer.Add (outwikerUnstableSizer, flag=wx.ALL | wx.EXPAND, border=0)


    def _createPluginsVersionGui (self, sizer):
        """
        Создание интерфейса для показа новых версий плагинов
        """
        pluginsLabel = wx.StaticText (self, -1, _(u"Updated plugins:"))
        self._mainSizer.Add (pluginsLabel, flag = wx.ALL | wx.EXPAND, border = 4)

        self.pluginsPanel = ScrolledPanel (self, -1, style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.pluginsPanel.SetMinSize ((-1, 200))
        self.pluginsPanel.SetupScrolling (scroll_x=False)
        
        self.pluginsSizer = wx.FlexGridSizer (cols=2)
        self.pluginsSizer.AddGrowableCol (1)
        self.pluginsPanel.SetSizer (self.pluginsSizer)

        sizer.Add (self.pluginsPanel, flag = wx.ALL | wx.EXPAND, border = 4)


    def _createGui (self):
        """
        Создание элементов управления в дилалоге
        """
        self._mainSizer = wx.FlexGridSizer (cols=1)
        self._mainSizer.AddGrowableCol (0)
        self._mainSizer.AddGrowableRow (4)

        # Строка с текущей версией OutWiker
        self._createOutWikerCurrentVersionGui (self._mainSizer)

        # Строка с последней стабильной версией OutWiker
        self._createOutWikerStableVersionGui (self._mainSizer)

        # Строка с последней нестабильной версией OutWiker
        self._createOutWikerUnstableVersionGui (self._mainSizer)

        # Панель со списком плагинов
        self._createPluginsVersionGui (self._mainSizer)

        buttonsSizer = self.CreateButtonSizer (wx.OK)
        self._mainSizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)

        self.SetSizer (self._mainSizer)
        self.Layout()


    def addPluginInfo (self, plugin, newversion, url):
        """
        Добавить информацию об обновленном плагине
        """
        newLabel = wx.StaticText (self.pluginsPanel, -1, plugin.name)

        self.pluginsSizer.Add (newLabel, 
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=4)

        newLink = wx.HyperlinkCtrl (self.pluginsPanel, -1, str(newversion), url)
        self.pluginsSizer.Add (newLink, 
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=4)

        self.Layout()


    def setCurrentOutWikerVersion (self, version):
        """
        Установить в диалоге номер текущей версии OutWiker
        """
        self.outwikerCurrentVersion.SetLabel (u"{0}".format (version) )
        self.Layout()


    def setLatestStableOutwikerVersion (self, version, isNewVersion):
        """
        Установить в диалоге номер последней стабильной версии
        """
        self.outwikerStableLink.SetLabel (u"{0}".format (version))
        
        color = self._activeUrlColor if isNewVersion else self._inactiveUrlColor
        self.outwikerStableLink.SetNormalColour (color)

        self.Layout()


    def setLatestUnstableOutwikerVersion (self, version, isNewVersion):
        """
        Установить в диалоге номер последней нестабильной версии
        """
        self.outwikerUnstableLink.SetLabel (u"{0}".format (version))
        
        color = self._activeUrlColor if isNewVersion else self._inactiveUrlColor
        self.outwikerUnstableLink.SetNormalColour (color)

        self.Layout()
