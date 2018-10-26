# -*- coding: utf-8 -*-

import os.path
import logging

from enchant import Dict, DictWithPWL, Broker
import enchant.errors

from .dictsfinder import DictsFinder
from .defines import CUSTOM_DICT_LANG

logger = logging.getLogger('outwiker.core.spellchecker.enchant')


class EnchantWrapper (object):
    """
    Wrapper around pyenchant (http://pythonhosted.org/pyenchant/)
    """
    # Key - tuple (lang, path), value - Dict instance
    _dictCache = {}

    def __init__(self, langlist, folders):
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        logger.debug('Initialize Enchant spell checker')
        self._folders = folders
        self._checkers = []
        self._customCheckers = []

        dictsFinder = DictsFinder(self._folders)

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang(lang):
                try:
                    logger.debug('Add dictionary. path={}; lang={}'.format(path, lang))
                    self._checkers.append(self._getDict(lang, path))
                except enchant.errors.Error as err:
                    logger.error('Spellchecker append error. path={}; lang={}'.format(path, lang))
                    logger.error(err)

    def addToCustomDict(self, dictIndex, word):
        if dictIndex < len(self._customCheckers):
            self._customCheckers[dictIndex].add(word)

    def _createCustomDictLang(self, pathToDict):
        # Create fake language for custom dictionary
        dicFile = os.path.join(pathToDict,
                               CUSTOM_DICT_LANG + u'.dic')

        affFile = os.path.join(pathToDict,
                               CUSTOM_DICT_LANG + u'.aff')

        if not os.path.exists(dicFile):
            with open(dicFile, 'w') as fp:
                fp.write(u'1\ntest')

        if not os.path.exists(affFile):
            with open(affFile, 'w'):
                pass

    def addCustomDict(self, customDictPath):
        try:
            self._createCustomDictLang(self._folders[-1])
        except IOError as err:
            logger.error("Can't create custom dictionary")

        key = (CUSTOM_DICT_LANG, customDictPath)

        if key not in self._dictCache:
            broker = Broker()
            broker.set_param('enchant.myspell.dictionary.path',
                             self._folders[-1])

            try:
                currentDict = DictWithPWL(CUSTOM_DICT_LANG,
                                          customDictPath,
                                          broker=broker)
            except enchant.errors.Error as err:
                logger.error('Custom dictionary error. path={}; lang={}'.format(customDictPath, key))
                logger.error(err)
                return

            self._dictCache[key] = currentDict
        else:
            currentDict = self._dictCache[key]

        self._customCheckers.append(currentDict)

    def _getDict(self, lang, path):
        key = (lang, path)
        if key not in self._dictCache:
            broker = Broker()
            broker.set_param('enchant.myspell.dictionary.path', path)
            broker.set_ordering('*', 'myspell')
            currentDict = Dict(lang, broker)
            self._dictCache[key] = currentDict
        else:
            currentDict = self._dictCache[key]

        return currentDict

    def check(self, word):
        if not self._checkers:
            return True

        for checker in self._checkers + self._customCheckers:
            if checker.check(word):
                return True

        return False

    def getSuggest(self, word):
        suggest_set = set()
        for checker in self._checkers + self._customCheckers:
            suggest_set |= set(checker.suggest(word))

        suggest = sorted(
            [item for item in suggest_set if len(item.strip()) > 0])

        return suggest
