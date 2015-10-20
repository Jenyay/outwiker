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

        self.notebook = wx.Notebook (self, -1)
        self._createPanels (self.notebook)

        self.__do_layout()

        self.SetSize((self._config.width.value, self._config.height.value))
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


    def _createPanels (self, notebook):
        self._generalPanel = GeneralPanel (notebook, self._application)
        self._iconsPanel = IconsPanel (notebook, self._application)
        self._appearancePanel = AppearancePanel (notebook, self._application)

        self._panels = [self._generalPanel,
                        self._iconsPanel,
                        self._appearancePanel,
                        ]

        for panel in self._panels:
            self.notebook.AddPage (panel, panel.title)


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add (self.notebook, 0, wx.EXPAND, 0)
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


    @property
    def tags (self):
        return self._generalPanel.tagsSelector.tags


    @property
    def icon (self):
        selection = self._iconsPanel.iconsList.getSelection()
        assert len (selection) != 0

        return selection[0]


    @property
    def style (self):
        return self._appearancePanel.style
