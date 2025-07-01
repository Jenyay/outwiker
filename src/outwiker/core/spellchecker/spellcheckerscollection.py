import os
from typing import Any, Dict, List

from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from .spellchecker import SpellChecker


class SpellCheckersCollection:
    def __init__(self, spell_dir_list: List[str]) -> None:
        self._spell_dir_list = spell_dir_list
        self._spellcheckers: Dict[str, Any] = {}

    def getSpellChecker(self, langlist: List[str]):
        key = self._getKey(langlist)
        if key in self._spellcheckers:
            return self._spellcheckers[key]

        spellChecker = SpellChecker(langlist, self._spell_dir_list)
        spellChecker.addCustomDict(
            os.path.join(self._spell_dir_list[-1], CUSTOM_DICT_FILE_NAME)
        )
        self._spellcheckers[key] = spellChecker
        return spellChecker

    def _getKey(self, langlist: List[str]):
        return ";".join(sorted([lang.lower() for lang in langlist]))

    def isCreated(self, langlist: List[str]):
        key = self._getKey(langlist)
        return key in self._spellcheckers

    def clear(self):
        self._spellcheckers.clear()
