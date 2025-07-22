# -*- coding: utf-8 -*-

import wx

from outwiker.app.gui.pagedialogpanels.generalpanel import (
    GeneralPanel,
    GeneralController,
)
from outwiker.app.gui.pagedialogpanels.appearancepanel import (
    AppearancePanel,
    AppearanceController,
)
from outwiker.core.events import PageDialogInitParams, PageDialogDestroyParams
from outwiker.gui.defines import CONTROLS_MARGIN
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.testeddialog import TestedDialog


class BasePageDialog(TestedDialog):
    def __init__(self, parentWnd, currentPage, parentPage, application):
        super().__init__(
            parent=parentWnd, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        self._parentPage = parentPage
        self._currentPage = currentPage

        self._application = application
        self._panels = []
        self._controllers = []

        self._config = PageDialogConfig(self._application.config)

        self._notebook = wx.Notebook(self, -1)
        self._appearancePanel = None
        self._appearanceController = None
        self._createPanels()

        self._do_layout()

        self._application.onPageDialogInit(
            self._application.selectedPage, PageDialogInitParams(self)
        )

        self._setDialogSize()
        self._generalPanel.titleTextCtrl.SetFocus()

    def _setDialogSize(self):
        self.Fit()
        default_width, default_height = self.GetClientSize()

        width = self._config.width.value
        height = self._config.height.value

        if default_width > self._config.width.value:
            width = default_width

        if default_height > self._config.height.value:
            height = default_height

        self.SetClientSize((width, height))

    def _validate(self):
        pass

    def _initController(self, controller):
        pass

    def _onOk(self, event):
        if not self._validate():
            return

        self.saveParams()
        list(map(lambda controller: controller.saveParams(), self._controllers))
        event.Skip()

    def Destroy(self):
        list(map(lambda controller: controller.clear(), self._controllers))

        self._application.onPageDialogDestroy(
            self._application.selectedPage, PageDialogDestroyParams(self)
        )
        super(BasePageDialog, self).Destroy()

    def getPanelsParent(self):
        return self._notebook

    def addPanel(self, panel, title):
        self._panels.append(panel)
        self.getPanelsParent().AddPage(panel, title)

    def getPanel(self, index):
        return self._panels[index]

    def removePanel(self, panel):
        if panel in self._panels:
            index = self._panels.index(panel)
            self._notebook.DeletePage(index)
            self._panels.remove(panel)

    def addController(self, controller):
        self._controllers.append(controller)
        self._initController(controller)

    def removeController(self, controller):
        if controller in self._controllers:
            controller.clear()
            self._controllers.remove(controller)

    def getController(self, index):
        return self._controllers[index]

    @property
    def currentPage(self):
        return self._currentPage

    @property
    def parentPage(self):
        return self._parentPage

    @property
    def generalPanel(self):
        return self._generalPanel

    def _createPanels(self):
        # Add general panel
        parent = self.getPanelsParent()

        self._generalPanel = GeneralPanel(parent, self._application.theme)
        self.addPanel(self._generalPanel, _("General"))

        self._generalController = GeneralController(
            self._generalPanel, self._application, self
        )
        self.addController(self._generalController)

    def showAppearancePanel(self):
        if self._appearancePanel is None:
            parent = self.getPanelsParent()
            self._appearancePanel = AppearancePanel(parent)
            self.addPanel(self._appearancePanel, _("Appearance"))

            self._appearanceController = AppearanceController(
                self._appearancePanel, self._application, self
            )
            self.addController(self._appearanceController)

    def hideAppearancePanel(self):
        if self._appearancePanel is not None:
            self.removeController(self._appearanceController)
            self.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def _do_layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(self._notebook, 0, wx.EXPAND, 0)
        self._createOkCancelButtons(mainSizer)
        self.SetSizerAndFit(mainSizer)

    def saveParams(self):
        width, height = self.GetClientSize()
        self._config.width.value = width
        self._config.height.value = height

    def _createOkCancelButtons(self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(buttonsSizer, flag=wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM, border=CONTROLS_MARGIN)
        self.Bind(wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)

    @property
    def selectedFactory(self):
        return self._generalController.selectedFactory

    @property
    def pageTitle(self):
        return self._generalController.pageTitle

    @property
    def orderCalculator(self):
        return self._generalController.orderCalculator

    def setPageProperties(self, page):
        for controller in self._controllers:
            if not controller.setPageProperties(page):
                return False

        return True
