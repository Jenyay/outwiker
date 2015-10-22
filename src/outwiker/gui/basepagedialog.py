# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx
import wx.combo

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.pagedialogpanels.iconspanel import IconsPanel
from outwiker.gui.pagedialogpanels.appearancepanel import AppearancePanel
from outwiker.gui.pagedialogpanels.generalpanel import GeneralPanel
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.events import PageDialogInitParams


class BasePageDialog (TestedDialog):
    __metaclass__ = ABCMeta

    def __init__(self, parentWnd, currentPage, parentPage):
        super (BasePageDialog, self).__init__(parent=parentWnd)

        self._parentPage = parentPage
        self._currentPage = currentPage

        self._application = Application
        self._panels = []

        self._config = PageDialogConfig (Application.config)

        self._notebook = wx.Notebook (self, -1)
        self._createPanels ()

        self.__do_layout()

        self._application.onPageDialogInit (self._application.selectedPage,
                                            PageDialogInitParams (self))

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


    def addPanel (self, panel, title):
        self._panels.append (panel)
        self.getPanelsParent().AddPage (panel, title)


    @property
    def currentPage (self):
        return self._currentPage


    @property
    def parentPage (self):
        return self._parentPage


    @property
    def generalPanel (self):
        return self._generalPanel


    @property
    def iconsPanel (self):
        return self._iconsPanel


    @property
    def appearancePanel (self):
        return self._appearancePanel


    def _createPanels (self):
        parent = self.getPanelsParent ()

        self._generalPanel = GeneralPanel (parent, self._application, self)
        self._iconsPanel = IconsPanel (parent, self._application, self)
        self._appearancePanel = AppearancePanel (parent, self._application, self)

        self.addPanel (self._generalPanel, _(u'General'))
        self.addPanel (self._iconsPanel, _(u'Icon'))
        self.addPanel (self._appearancePanel, _(u'Appearance'))


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
            if panel.IsShown ():
                if not panel.setPageProperties (page):
                    return False

        return True
