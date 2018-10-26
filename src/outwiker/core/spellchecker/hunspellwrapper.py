# -*- coding: utf-8 -*-

import os.path
import logging

import hunspell

from .dictsfinder import DictsFinder
from .defines import CUSTOM_DICT_LANG

logger = logging.getLogger('outwiker.core.spellchecker.hunspell')


class HunspellWrapper (object):
    """
    Wrapper around hunspell (https://github.com/blatinier/pyhunspell)
    """
    def __init__(self, langlist, folders):
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
                    checker = hunspell.HunSpell(dic_file, aff_file)
                else:
                    checker.add_dic(dic_file)

                logger.debug('Add dictionary: {}'.format(dic_file))

            if checker is not None:
                self._checkers[lang] = checker

    def addToCustomDict(self, dictIndex, word):
        key, dic_file = self._customDicts[dictIndex]
        assert key in self._checkers

        self._checkers[key].add(word)

        with open(dic_file, encoding='utf8') as fp:
            lines = fp.readlines()

        lines.append(word)
        lines[0] = str(len(lines) - 1)

        with open(dic_file, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines))

    def _createCustomDictLang(self, dic_file, aff_file):
        if not os.path.exists(dic_file):
            logger.debug('Create custom .dic file: {}'.format(dic_file))
            with open(dic_file, 'w', encoding='utf8') as fp:
                fp.write('1\ntest')

        if not os.path.exists(aff_file):
            logger.debug('Create custom .aff file: {}'.format(aff_file))
            with open(aff_file, 'w') as fp:
                fp.write('SET UTF-8')

    def addCustomDict(self, customDictPath):
        logger.debug('Add custom dictionary: {}'.format(customDictPath))

        key = (CUSTOM_DICT_LANG, customDictPath)
        if key in self._checkers:
            logger.debug('Dictionary already added: {}'.format(customDictPath))
            return

        dic_file = customDictPath
        aff_file = customDictPath[:-4] + '.aff'

        try:
            self._createCustomDictLang(dic_file, aff_file)
            self._fixDicFile(dic_file)
            checker = hunspell.HunSpell(dic_file, aff_file)
            self._checkers[key] = checker
            self._customDicts.append((key, dic_file))
        except IOError as err:
            logger.error("Can't create custom dictionary: {}".format(customDictPath))

    def _fixDicFile(self, dic_file):
        with open(dic_file, encoding='utf8') as fp:
            lines = fp.readlines()

        lines = [line.strip() for line in lines if line.strip()]

        fixed = False
        try:
            int(lines[0])
        except IndexError:
            lines = ['1', 'test']
            fixed = True
        except ValueError:
            lines.insert(0, str(len(lines)))
            fixed = True

        if fixed:
            with open(dic_file, 'w', encoding='utf8') as fp:
                fp.write('\n'.join(lines))

    def check(self, word):
        if not self._checkers:
            return True

        for checker in self._checkers.values():
            encoding = checker.get_dic_encoding()

            try:
                word_encoded = word.encode(encoding)
                if checker.spell(word_encoded):
                    return True
            except UnicodeEncodeError:
                continue

        return False

    def getSuggest(self, word):
        suggest_set = set()
        for checker in self._checkers.values():
            suggest_set |= set(checker.suggest(word))

        suggest = sorted(
            [item for item in suggest_set if len(item.strip()) > 0])

        return suggest
