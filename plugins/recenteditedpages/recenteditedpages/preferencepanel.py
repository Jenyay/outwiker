import wx

from outwiker.api.core.config import Config
from outwiker.api.gui.preferences import BasePrefPanel

from .i18n import get_
from .config import RecentPagesConfig


class PreferencePanel(BasePrefPanel):
    def __init__(self, parent: wx.Treebook, config: Config):
        """
        parent - panel's parent
        config - Config from plugin._application.config
        """
        super().__init__(parent)
        self._config = RecentPagesConfig(config)

        global _
        _ = get_()

        self._createGui()
        self.Layout()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        # Hightlight
        self._colorizeCheckBox = self._createCheckBox(_("Highlight pages"), mainSizer)

        # Hightlight color picker
        colorPickerSizer = wx.FlexGridSizer(cols=2)
        colorPickerSizer.AddGrowableCol(0)
        colorPickerSizer.AddGrowableCol(1)
        self._highlightColor = self._createLabelAndColorPicker(_("Highlight color"), colorPickerSizer)[1]
        mainSizer.Add(colorPickerSizer, flag=wx.EXPAND | wx.ALL, border=2)

        # Extra icon
        self._addExtraIconCheckBox = self._createCheckBox(_("Add extra icon"), mainSizer)
        self.SetSizer(mainSizer)

    def LoadState(self):
        self._colorizeCheckBox.SetValue(self._config.colorizePage.value)
        self._addExtraIconCheckBox.SetValue(self._config.addExtraIcon.value)
        self._highlightColor.SetColour(wx.Colour(self._config.highlightColor.value))

    def Save(self):
        self._config.colorizePage.value = self._colorizeCheckBox.GetValue()
        self._config.addExtraIcon.value = self._addExtraIconCheckBox.GetValue()
        self._config.highlightColor.value = self._highlightColor.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
