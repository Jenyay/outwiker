# -*- coding: utf-8 -*-

import os.path
import logging
from typing import Dict, List, Optional, Tuple

import hunspell

from .basespellcheckerwrapper import BaseSpellCheckerWrapper
from .dictsfinder import DictsFinder
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
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        self._dict_folers = dict_folders

        # Key - language (en_US, ru_RU etc),
        # value - instance of the HunSpell class
        self._checkers: Dict[str, hunspell.Hunspell] = {}

        # tuple: (key for self._checkers, path to .dic file)
        self._customDict: Optional[Tuple[str, str]] = None

    def addLanguage(self, lang: str):
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
            self._checkers[lang] = checker

    def addToCustomDict(self, word: str):
        if self._customDict is None:
            logger.warn("Custom dictionary is not set")
            return

        key, dic_file = self._customDict
        assert key in self._checkers

        self._checkers[key].add(word)
        add_word_to_dic_file(dic_file, word)

    def setCustomDict(self, customDictPath: str):
        logger.debug("Add custom dictionary: %s", customDictPath)

        dic_folder = os.path.dirname(customDictPath)
        dic_file_name = os.path.basename(customDictPath)
        dic_name = dic_file_name[:-4]
        dic_file = customDictPath
        aff_file = customDictPath[:-4] + ".aff"

        key = "{}:{}".format(dic_name, customDictPath)
        if key in self._checkers:
            logger.debug("Dictionary already added: %s", customDictPath)
            return

        try:
            create_new_dic_file(dic_file)
            create_new_aff_file(aff_file)
            fix_dic_file(dic_file)
            checker = hunspell.Hunspell(
                dic_name, hunspell_data_dir=dic_folder, system_encoding="UTF-8"
            )
            self._checkers[key] = checker
            self._customDict = (key, dic_file)
        except IOError:
            logger.error("Can't create custom dictionary: %s", customDictPath)
            return

    def check(self, word: str) -> bool:
        if not self._checkers:
            return True

        for checker in self._checkers.values():
            if checker.spell(word):
                return True

        return False

    def getSuggest(self, word: str) -> List[str]:
        suggest_set = set()
        for checker in self._checkers.values():
            try:
                suggest_set |= set(checker.suggest(word))
            except UnicodeEncodeError:
                continue

        suggest = sorted([item for item in suggest_set if len(item.strip()) > 0])

        return suggest
