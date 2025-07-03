import os
from typing import Dict, List

from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.system import getOS
from .spellchecker import SpellChecker
from .basespellcheckerwrapper import BaseSpellCheckerWrapper


class SpellCheckersFactory:
    def __init__(self, spell_dir_list: List[str]) -> None:
        self._CUSTOM_DICT_KEY = ""
        self._spell_dir_list = spell_dir_list
        self._spellcheckers: Dict[str, BaseSpellCheckerWrapper] = {}

    def getSpellChecker(
        self, langlist: List[str], use_custom_dict: bool = True
    ) -> SpellChecker:
        checkers = []
        for lang in langlist:
            key = self._getKey(lang)
            if key in self._spellcheckers:
                checker = self._spellcheckers[key]
            else:
                checker = getOS().getSpellChecker(self._spell_dir_list)
                checker.setLanguage(lang)
                self._spellcheckers[key] = checker

            checkers.append(checker)

        # If there is no custom dictionary, create it
        if not use_custom_dict:
            return SpellChecker(checkers)

        if self._CUSTOM_DICT_KEY in self._spellcheckers:
            custom_dict_checker = self._spellcheckers[self._CUSTOM_DICT_KEY]
        else:
            custom_dict_checker = getOS().getSpellChecker([])
            custom_dict_checker.setCustomDict(
                os.path.join(self._spell_dir_list[-1], CUSTOM_DICT_FILE_NAME)
            )
            self._spellcheckers[self._CUSTOM_DICT_KEY] = custom_dict_checker

        return SpellChecker(checkers, custom_dict_checker)

    def _getKey(self, lang: str) -> str:
        return lang.lower()

    # Used for tests only
    def isCreated(self, lang: str) -> bool:
        key = self._getKey(lang)
        return key in self._spellcheckers

    def clear(self):
        self._spellcheckers.clear()
