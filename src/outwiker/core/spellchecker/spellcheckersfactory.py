import logging
import os
from typing import Dict, List, Optional

from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.system import getOS
from .spellchecker import SpellChecker

logger = logging.getLogger("spellcheckers")


class SpellCheckersFactory:
    def __init__(self, spell_dir_list: List[str]) -> None:
        self._CUSTOM_DICT_KEY = ""
        self._spell_dir_list = spell_dir_list
        self._spellcheckers = {}
        self._lang_list: Optional[List[str]] = None
        self._default_checkers = None

    def setLangList(self, langlist: List[str]):
        self._lang_list = langlist[:]
        self._default_checkers = None
        if self._CUSTOM_DICT_KEY in self._spellcheckers:
            del self._spellcheckers[self._CUSTOM_DICT_KEY]
        logger.debug("Use dictionaries: %s", ", ".join(langlist))

    def _getCheckers(self, langlist: List[str]):
        checkers = []
        for lang in langlist:
            key = self._getKey(lang)
            if key in self._spellcheckers:
                checker = self._spellcheckers[key]
            else:
                checker = getOS().getSpellChecker(self._spell_dir_list)
                checker.setLanguage(lang)
                # self._spellcheckers[key] = checker

            checkers.append(checker)

        return checkers

    def getSpellChecker(
        self, extra_lang_list: Optional[List[str]] = None, use_custom_dict: bool = True
    ) -> SpellChecker:
        if self._lang_list is None:
            checkers = []
        elif self._default_checkers is None:
            checkers = self._getCheckers(self._lang_list)
            # self._default_checkers = checkers[:]
        else:
            checkers = self._default_checkers[:]

        # if extra_lang_list is not None:
        #     checkers += self._getCheckers(extra_lang_list)

        # # If there is no custom dictionary, create it
        # if not use_custom_dict:
        #     return SpellChecker(checkers)

        # if self._CUSTOM_DICT_KEY in self._spellcheckers:
        #     custom_dict_checker = self._spellcheckers[self._CUSTOM_DICT_KEY]
        # else:
        #     custom_dict_checker = getOS().getSpellChecker([])
        #     custom_dict_checker.setCustomDict(
        #         os.path.join(self._spell_dir_list[-1], CUSTOM_DICT_FILE_NAME)
        #     )
        #     self._spellcheckers[self._CUSTOM_DICT_KEY] = custom_dict_checker

        # return SpellChecker(checkers, custom_dict_checker)
        return SpellChecker([])

    def _getKey(self, lang: str) -> str:
        return lang.lower()

    # Used for tests only
    def isCreated(self, lang: str) -> bool:
        key = self._getKey(lang)
        return key in self._spellcheckers

    def clear(self):
        self._spellcheckers.clear()
        if self._default_checkers is not None:
            self._default_checkers.clear()
