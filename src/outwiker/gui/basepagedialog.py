# -*- coding: UTF-8 -*-

import os
import os.path

import wx
import wx.combo

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PageDialogConfig
from outwiker.gui.pagedialogpanels.iconspanel import IconsPanel
from outwiker.gui.pagedialogpanels.appearancepanel import AppearancePanel
from outwiker.gui.pagedialogpanels.generalpanel import GeneralPanel


class BasePageDialog (wx.Dialog):
    def __init__(self, parentPage = None, *args, **kwds):
        """
        parentPage - родительская страница (используется, если страницу нужно создавать, а не изменять)
        """
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        super (BasePageDialog, self).__init__(*args, **kwds)

        self._application = Application
        self._panels = []

        # Используется для редактирования существующей страницы
        self.currentPage = None
        self.parentPage = parentPage

        self.config = PageDialogConfig (Application.config)

        self.notebook = wx.Notebook (self, -1)
        self._createPanels (self.notebook)

        self.__do_layout()

        self.SetTitle(_(u"Create Page"))
        self.SetSize((self.config.width.value, self.config.height.value))
        self.Center(wx.CENTRE_ON_SCREEN)
        self.generalPanel.titleTextCtrl.SetFocus()


    def _createPanels (self, notebook):
        self._panels = [GeneralPanel (notebook, self._application),
                        IconsPanel (notebook, self._application),
                        AppearancePanel (notebook, self._application),
                        ]

        self.generalPanel = self._panels[0]
        self.iconsPanel = self._panels[1]
        self.appearancePanel = self._panels[2]

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
        self.config.width.value = width
        self.config.height.value = height

        styleName = self.appearancePanel.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае,
        # если изменяется существующая страница
        if (self.currentPage is None):
            self.config.recentStyle.value = styleName


    def _fillStyleCombo (self, styleslist, page=None):
        """
        Заполняет self.appearancePanel.styleCombo списком стилей
        styleslist - список путей до загруженных стилей
        page - страница, для которой вызывается диалог. Если page is not None, то первый стиль в списке - это стиль данной страницы
        """
        names = []
        if page is not None:
            names.append (_(u"Do not change"))

        names.append (_(u"Default"))
        style_names = [os.path.basename (style) for style in styleslist]
        style_names.sort()

        names += style_names

        self.appearancePanel.styleCombo.Clear()
        self.appearancePanel.styleCombo.AppendItems (names)

        # Определение последнего используемого стиля
        recentStyle = self.config.recentStyle.value
        names_lower = [name.lower() for name in names]
        try:
            currentStyleIndex = names_lower.index (recentStyle.lower())
        except ValueError:
            currentStyleIndex = 0

        if page is not None:
            # Для уже существующих страниц по умолчанию использовать уже установленный стиль
            currentStyleIndex = 0

        self.appearancePanel.styleCombo.SetSelection (currentStyleIndex)


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)


    @property
    def selectedFactory (self):
        index = self.generalPanel.typeCombo.GetSelection()
        return self.generalPanel.typeCombo.GetClientData (index)


    @property
    def pageTitle (self):
        return self.generalPanel.titleTextCtrl.GetValue().strip()


    @property
    def tags (self):
        return self.generalPanel.tagsSelector.tags


    @property
    def icon (self):
        selection = self.iconsPanel.iconsList.getSelection()
        assert len (selection) != 0

        return selection[0]
