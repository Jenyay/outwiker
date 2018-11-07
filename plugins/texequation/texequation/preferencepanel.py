# -*- coding: utf-8 -*-

import wx

from outwiker.core.config import Config
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel

from .i18n import get_
from .texconfig import TeXConfig


class PreferencePanel(BasePrefPanel):
    def __init__(self, parent: wx.Treebook, config: Config):
        """
        parent - panel's parent
        config - Config from plugin._application.config
        """
        super().__init__(parent)
        self.config = TeXConfig(config)

        global _
        _ = get_()

        self._createGui()
        self.SetupScrolling()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        # Scale of inline equation
        scale_inline_label = wx.StaticText(self,
                                           label=_('Inline equations scale'))
        self.scale_inline_spin = wx.SpinCtrl(
            self,
            style=wx.SP_ARROW_KEYS,
            min=1,
            max=10000,
            initial=100
        )
        self.scale_inline_spin.SetMinSize((150, -1))

        # Scale of block equation
        scale_block_label = wx.StaticText(self,
                                          label=_('Block equations scale'))
        self.scale_block_spin = wx.SpinCtrl(
            self,
            style=wx.SP_ARROW_KEYS,
            min=1,
            max=10000,
            initial=100
        )
        self.scale_block_spin.SetMinSize((150, -1))

        # Layout GUI elements
        mainSizer.Add(
            scale_inline_label,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
            border=2)

        mainSizer.Add(
            self.scale_inline_spin,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2)

        mainSizer.Add(
            scale_block_label,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
            border=2)

        mainSizer.Add(
            self.scale_block_spin,
            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2)

        self.SetSizer(mainSizer)

    def LoadState(self):
        self.scale_inline_spin.SetValue(self.config.scaleInline.value)
        self.scale_block_spin.SetValue(self.config.scaleBlock.value)

    def Save(self):
        self.config.scaleInline.value = self.scale_inline_spin.GetValue()
        self.config.scaleBlock.value = self.scale_block_spin.GetValue()
