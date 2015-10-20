# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx
import wx.combo

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.pagedialogpanels.iconspanel import IconsPanel
from outwiker.gui.pagedialogpanels.appearancepanel import AppearancePanel
from outwiker.gui.pagedialogpanels.generalpanel import GeneralPanel


class BasePageDialog (wx.Dialog):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        super (BasePageDialog, self).__init__(*args, **kwds)

        self._application = Application
        self._panels = []

        self._config = PageDialogConfig (Application.config)

        self._notebook = wx.Notebook (self, -1)
        self._createPanels ()

        self.__do_layout()

        self.SetSizeWH (self._config.width.value, self._config.height.value)
        self.Center(wx.CENTRE_ON_SCREEN)


    @abstractmethod
    def _validate (self):
        pass


    def _onOk (self, event):
        if not self._validate():
            return

        self.saveParams()
        map (lambda panel: panel.saveParams(), self._panels)
        map (lambda panel: panel.clear(), self._panels)
        event.Skip()


    def _onCancel (self, event):
        map (lambda panel: panel.clear(), self._panels)
        event.Skip()


    def getPanelsParent (self):
        return self._notebook


    def addPanel (self, panel):
        self._panels.append (panel)
        self.getPanelsParent().AddPage (panel, panel.title)


    def _createPanels (self):
        parent = self.getPanelsParent ()

        self._generalPanel = GeneralPanel (parent, self._application)
        iconsPanel = IconsPanel (parent, self._application)
        appearancePanel = AppearancePanel (parent, self._application)

        self.addPanel (self._generalPanel)
        self.addPanel (iconsPanel)
        self.addPanel (appearancePanel)


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(rows=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add (self._notebook, 0, wx.EXPAND, 0)
        self._createOkCancelButtons (mainSizer)
        self.SetSizer(mainSizer)

        self.Layout()


    def saveParams (self):
        width, height = self.GetSizeTuple()
        self._config.width.value = width
        self._config.height.value = height


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
        self.Bind (wx.EVT_BUTTON, self._onCancel, id=wx.ID_CANCEL)


    @property
    def selectedFactory (self):
        return self._generalPanel.selectedFactory


    @property
    def pageTitle (self):
        return self._generalPanel.pageTitle


    def setPageProperties (self, page):
        for panel in self._panels:
            if not panel.setPageProperties (page):
                return False

        return True
