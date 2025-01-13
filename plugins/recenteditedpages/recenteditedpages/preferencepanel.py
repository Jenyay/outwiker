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

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        self._colorizeCheckBox = self._createCheckBox(_("Highlight pages"), mainSizer)
        self._addExtraIconCheckBox = self._createCheckBox(_("Add extra icon"), mainSizer)

        self.SetSizer(mainSizer)

    def LoadState(self):
        self._colorizeCheckBox.SetValue(self._config.colorizePage.value)
        self._addExtraIconCheckBox.SetValue(self._config.addExtraIcon.value)

    def Save(self):
        self._config.colorizePage.value = self._colorizeCheckBox.GetValue()
        self._config.addExtraIcon.value = self._addExtraIconCheckBox.GetValue()
