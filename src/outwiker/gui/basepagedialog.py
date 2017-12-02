# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx
#import wx.combo

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.pagedialogpanels.generalpanel import (GeneralPanel,
                                                        GeneralController)
from outwiker.gui.pagedialogpanels.iconspanel import (IconsPanel,
                                                      IconsController)
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.events import (PageDialogInitParams,
                                  PageDialogDestroyParams)


class BasePageDialog (TestedDialog):
    #__metaclass__ = ABCMeta

    def __init__(self, parentWnd, currentPage, parentPage):
        super (BasePageDialog, self).__init__(parent=parentWnd)

        self._parentPage = parentPage
        self._currentPage = currentPage

        self._application = Application
        self._panels = []
        self._controllers = []

        self._config = PageDialogConfig (Application.config)

        self._notebook = wx.Notebook (self, -1)
        self._createPanels ()

        self.__do_layout()

        self._application.onPageDialogInit (self._application.selectedPage,
                                            PageDialogInitParams (self))

        self.SetClientSize ((self._config.width.value, self._config.height.value))

        self.Center(wx.BOTH)
        self._generalPanel.titleTextCtrl.SetFocus()


    #@abstractmethod
    def _validate (self):
        pass

    #@abstractmethod
    def _initController (self, controller):
        pass


    def _onOk (self, event):
        if not self._validate():
            return

        self.saveParams()
        map (lambda controller: controller.saveParams(), self._controllers)
        event.Skip()


    def Destroy (self):
        map (lambda controller: controller.clear(), self._controllers)

        self._application.onPageDialogDestroy (self._application.selectedPage,
                                               PageDialogDestroyParams (self))
        super (BasePageDialog, self).Destroy()


    def getPanelsParent (self):
        return self._notebook


    def addPanel (self, panel, title):
        self._panels.append (panel)
        self.getPanelsParent().AddPage (panel, title)


    def removePanel (self, panel):
        if panel in self._panels:
            index = self._panels.index (panel)
            self._notebook.DeletePage (index)
            self._panels.remove (panel)


    def addController (self, controller):
        self._controllers.append (controller)
        self._initController (controller)


    def removeController (self, controller):
        if controller in self._controllers:
            controller.clear()
            self._controllers.remove (controller)


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

        self._generalPanel = GeneralPanel (parent)
        self.addPanel (self._generalPanel, _(u'General'))

        self._iconsPanel = IconsPanel (parent)
        self.addPanel (self._iconsPanel, _(u'Icon'))

        self._generalController = GeneralController (self._generalPanel,
                                                     self._application,
                                                     self)
        self.addController (self._generalController)

        self._iconsController = IconsController (self._iconsPanel,
                                                 self._application,
                                                 self)
        self.addController (self._iconsController)


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add (self._notebook, 0, wx.EXPAND, 0)
        self._createOkCancelButtons (mainSizer)
        self.SetSizer(mainSizer)
        self.Layout()


    def saveParams (self):
        width, height = self.GetClientSize()
        self._config.width.value = width
        self._config.height.value = height


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)


    @property
    def selectedFactory (self):
        return self._generalController.selectedFactory


    @property
    def pageTitle (self):
        return self._generalController.pageTitle


    def setPageProperties (self, page):
        for controller in self._controllers:
            if not controller.setPageProperties (page):
                return False

        return True
