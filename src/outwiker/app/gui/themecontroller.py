from typing import Optional

from outwiker.core.application import Application
from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.gui.theme import Theme


class ThemeController:
    def __init__(self, application: Application) -> None:
        self._application = application
        self._theme: Optional[Theme] = None
        self._application.onPreferencesDialogClose.bind(self._onPreferences, EVENT_PRIORITY_MAX_CORE)

    def setTheme(self, theme: Theme):
        self.clear()
        self._theme = theme
        
    def loadParams(self):
        if self._theme is not None:
            self._theme.loadSystemParams()
            self._theme.loadFromConfig(self._application.config)
            self._theme.sendEvent()

    def clear(self):
        if self._theme is not None:
            self._theme.clear()
            self._theme = None

    def _onPreferences(self, dialog):
        if self._theme is not None:
            self._theme.loadFromConfig(self._application.config)
            self._theme.sendEvent()
