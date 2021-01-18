# -*- coding: utf-8 -*-

import os.path
import logging
from typing import List

import hunspell

from .dictsfinder import DictsFinder
from .spelldict import (create_new_dic_file,
                        create_new_aff_file,
                        fix_dic_file,
                        add_word_to_dic_file)

logger = logging.getLogger('outwiker.core.spellchecker.cyhunspell')


class CyHunspellWrapper (object):
    """
    Wrapper around the Cyhunspell library
    """

    def __init__(self, langlist: List[str], folders: List[str]):
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        logger.debug('Initialize HunspellWrapper spell checker')

        # Key - language (en_US, ru_RU etc),
        # value - onstance of the HunSpell class
        self._checkers = {}

        # Index - number of the dictionary,
        # value - tuple: (key for self._checkers, path to .dic file)
        self._customDicts = []

        dictsFinder = DictsFinder(folders)

        for lang in langlist:
            checker = None

            for path in dictsFinder.getFoldersForLang(lang):
                dic_file = os.path.join(path, lang + '.dic')
                aff_file = os.path.join(path, lang + '.aff')

                if (checker is None and
                        os.path.exists(dic_file) and
                        os.path.exists(aff_file)):
                    checker = hunspell.Hunspell(
                        lang, hunspell_data_dir=path, system_encoding='UTF-8')

                logger.debug('Add dictionary: {}'.format(dic_file))

            if checker is not None:
                self._checkers[lang] = checker

    def addToCustomDict(self, dictIndex: int, word: str):
        key, dic_file = self._customDicts[dictIndex]
        assert key in self._checkers

        self._checkers[key].add(word)
        add_word_to_dic_file(dic_file, word)

    def addCustomDict(self, customDictPath: str):
        logger.debug('Add custom dictionary: {}'.format(customDictPath))

        dic_folder = os.path.dirname(customDictPath)
        dic_file_name = os.path.basename(customDictPath)
        dic_name = dic_file_name[:-4]
        dic_file = customDictPath
        aff_file = customDictPath[:-4] + '.aff'

        key = (dic_name, customDictPath)
        if key in self._checkers:
            logger.debug('Dictionary already added: {}'.format(customDictPath))
            return

        try:
            create_new_dic_file(dic_file)
            create_new_aff_file(aff_file)
            fix_dic_file(dic_file)
            checker = hunspell.Hunspell(
                dic_name,
                hunspell_data_dir=dic_folder,
                system_encoding='UTF-8')
            self._checkers[key] = checker
            self._customDicts.append((key, dic_file))
        except IOError:
            logger.error(
                "Can't create custom dictionary: {}".format(customDictPath))

    def check(self, word: str):
        if not self._checkers:
            return True

        for checker in self._checkers.values():
            if checker.spell(word):
                return True

        return False

    def getSuggest(self, word: str):
        suggest_set = set()
        for checker in self._checkers.values():
            try:
                suggest_set |= set(checker.suggest(word))
            except UnicodeEncodeError:
                continue

        suggest = sorted(
            [item for item in suggest_set if len(item.strip()) > 0])

        return suggest
