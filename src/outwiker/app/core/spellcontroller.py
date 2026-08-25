from typing import List

from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.core.application import Application
from outwiker.gui.guiconfig import EditorConfig


class SpellCheckersController:
    def __init__(self, application: Application) -> None:
        self._application = application
        self._config = EditorConfig(self._application.config)
        self.updateSpellCheckers()

        self._application.onPreferencesDialogClose.bind(
            self._onPreferences, EVENT_PRIORITY_MAX_CORE
        )

    def updateSpellCheckers(self):
        langlist = self._getDictsFromConfig()
        spell_checkers = self._application.spellCheckers
        if spell_checkers is not None:
            spell_checkers.setLangList(langlist)

    def _getDictsFromConfig(self) -> List[str]:
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip() for item in dictsStr.split(",") if item.strip()]

    def _onPreferences(self, dialog):
        self.updateSpellCheckers()

    def clear(self):
        self._application.onPreferencesDialogClose.unbind(self._onPreferences)
        spell_checkers = self._application.spellCheckers
        if spell_checkers is not None:
            spell_checkers.clear()
