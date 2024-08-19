# -*- coding=utf-8 -*-

import wx

from outwiker.gui.preferences import configelements
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.datetimeformatctrl import DateTimeFormatCtrl
from outwiker.gui.controls.treebook2 import BasePrefPanel
from outwiker.gui.guiconfig import GeneralGuiConfig


class FormatsPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self.generalConfig = GeneralGuiConfig(application.config)
        self._createGui()

    def _createGui(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createTemplatesGui(main_sizer, self.generalConfig)

        self.SetSizer(main_sizer)

    def _createTemplatesGui(self, main_sizer, generalConfig):
        """
        Create GUI for selection date and time format
        and new page title template
        """
        # Config values
        initial_date_format = generalConfig.dateTimeFormat.value
        initial_page_title = generalConfig.pageTitleTemplate.value

        # Create labels
        dateTimeLabel = wx.StaticText(self, label=_("Date and time format"))
        pageTitleTemplateLabel = wx.StaticText(self, label=_("New page title template"))

        hintBitmap = wx.Bitmap(getBuiltinImagePath("wand.png"))

        # Create main controls
        self.dateTimeFormatCtrl = DateTimeFormatCtrl(
            self, hintBitmap, initial_date_format
        )

        self.pageTitleTemplateCtrl = DateTimeFormatCtrl(
            self, hintBitmap, initial_page_title
        )

        # Create common sizer
        templateSizer = wx.FlexGridSizer(cols=2)
        templateSizer.AddGrowableCol(1)

        templateSizer.Add(
            dateTimeLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        templateSizer.Add(
            self.dateTimeFormatCtrl, flag=wx.TOP | wx.BOTTOM | wx.EXPAND, border=2
        )

        templateSizer.Add(
            pageTitleTemplateLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        templateSizer.Add(
            self.pageTitleTemplateCtrl, flag=wx.TOP | wx.BOTTOM | wx.EXPAND, border=2
        )

        main_sizer.Add(templateSizer, flag=wx.EXPAND)

    def LoadState(self):
        self.dateTimeFormat = configelements.StringElement(
            self.generalConfig.dateTimeFormat, self.dateTimeFormatCtrl
        )

        self.pageTitleTemplate = configelements.StringElement(
            self.generalConfig.pageTitleTemplate, self.pageTitleTemplateCtrl
        )

    def Save(self):
        self.dateTimeFormat.save()
        self.pageTitleTemplate.save()
