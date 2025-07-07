# -*- coding: utf-8 -*-

import os.path
import logging
from typing import List, Optional

import hunspell

from .dictsfinder import DictsFinder
from .basespellcheckerwrapper import BaseSpellCheckerWrapper
from .spelldict import (
    create_new_dic_file,
    create_new_aff_file,
    fix_dic_file,
    add_word_to_dic_file,
)

logger = logging.getLogger("outwiker.core.spellchecker.cyhunspell")


class CyHunspellWrapper(BaseSpellCheckerWrapper):
    """
    Wrapper around the Cyhunspell library
    """

    def __init__(self, dict_folders: List[str]):
        self._dict_folers = dict_folders
        self._checker: Optional[hunspell.Hunspell] = None
        self._customDictChecker: Optional[hunspell.Hunspell] = None
        self._customDictPath: Optional[str] = None

    def setLanguage(self, lang: str):
        logger.debug("Add dictionary to HunspellWrapper spell checker")
        dictsFinder = DictsFinder(self._dict_folers)

        checker = None

        for path in dictsFinder.getFoldersForLang(lang):
            dic_file = os.path.join(path, lang + ".dic")
            aff_file = os.path.join(path, lang + ".aff")

            if (
                checker is None
                and os.path.exists(dic_file)
                and os.path.exists(aff_file)
            ):
                checker = hunspell.Hunspell(
                    lang, hunspell_data_dir=path, system_encoding="UTF-8"
                )

            logger.debug("Add dictionary: %s", dic_file)

        if checker is not None:
            self._checker = checker

    def addToCustomDict(self, word: str):
        if self._customDictChecker is None:
            logger.warn("Custom dictionary is not set")
            return

        assert self._customDictPath is not None, "Custom dictionary path is not set"

        self._customDictChecker.add(word)
        add_word_to_dic_file(self._customDictPath, word)

    def setCustomDict(self, customDictPath: str):
        logger.debug("Add custom dictionary: %s", customDictPath)

        dic_folder = os.path.dirname(customDictPath)
        dic_file_name = os.path.basename(customDictPath)
        dic_name = dic_file_name[:-4]
        dic_file = customDictPath
        aff_file = customDictPath[:-4] + ".aff"

        try:
            create_new_dic_file(dic_file)
            create_new_aff_file(aff_file)
            fix_dic_file(dic_file)
            checker = hunspell.Hunspell(
                dic_name, hunspell_data_dir=dic_folder, system_encoding="UTF-8"
            )
            self._customDictChecker = checker
            self._customDictPath = customDictPath
        except IOError:
            logger.error("Can't create custom dictionary: %s", customDictPath)
            return

    def check(self, word: str) -> bool:
        checkers = self._getCheckers()
        if not checkers:
            return True

        for checker in checkers:
            if checker.spell(word):
                return True

        return False

    def _getCheckers(self) -> List[hunspell.Hunspell]:
        checkers = []
        if self._checker is not None:
            checkers.append(self._checker)

        if self._customDictChecker is not None:
            checkers.append(self._customDictChecker)

        return checkers

    def getSuggest(self, word: str) -> List[str]:
        suggest_set = set()
        checkers = self._getCheckers()
        for checker in checkers:
            try:
                suggest_set |= set(checker.suggest(word))
            except UnicodeEncodeError:
                continue

        suggest = sorted([item for item in suggest_set if len(item.strip()) > 0])

        return suggest
