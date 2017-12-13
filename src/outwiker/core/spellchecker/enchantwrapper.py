# -*- coding: UTF-8 -*-

import os.path

from enchant import Dict, DictWithPWL, Broker
import enchant.errors

from .dictsfinder import DictsFinder
from .defines import CUSTOM_DICT_LANG


class EnchantWrapper (object):
    """
    Wrapper around pyenchant (http://pythonhosted.org/pyenchant/)
    """
    # Key - tuple (lang, path), value - Dict instance
    _dictCache = {}

    def __init__ (self, langlist, folders):
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        self._folders = folders
        self._checkers = []
        self._customCheckers = []

        dictsFinder = DictsFinder (self._folders)

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                try:
                    self._checkers.append (self._getDict (lang, path))
                except enchant.errors.Error:
                    pass


    def addToCustomDict (self, dictIndex, word):
        if dictIndex < len (self._customCheckers):
            self._customCheckers[dictIndex].add_to_pwl (word)


    def _createCustomDictLang (self, pathToDict):
        # Create fake language for custom dictionary
        dicFile = os.path.join (pathToDict,
                                CUSTOM_DICT_LANG + u'.dic')

        affFile = os.path.join (pathToDict,
                                CUSTOM_DICT_LANG + u'.aff')

        if not os.path.exists (dicFile):
            with open (dicFile, 'w') as fp:
                fp.write (u'1\ntest')

        if not os.path.exists (affFile):
            with open (affFile, 'w'):
                pass


    def addCustomDict (self, customDictPath):
        try:
            self._createCustomDictLang (self._folders[-1])
        except IOError:
            pass

        key = (CUSTOM_DICT_LANG, customDictPath)

        if key not in self._dictCache:
            broker = Broker ()
            broker.set_param ('enchant.myspell.dictionary.path',
                              self._folders[-1])

            try:
                currentDict = DictWithPWL (CUSTOM_DICT_LANG,
                                           customDictPath,
                                           broker=broker)
            except enchant.errors.Error:
                return

            self._dictCache[key] = currentDict
        else:
            currentDict = self._dictCache[key]

        self._customCheckers.append (currentDict)


    def _getDict (self, lang, path):
        key = (lang, path)
        if key not in self._dictCache:
            broker = Broker ()
            broker.set_param ('enchant.myspell.dictionary.path', path)
            currentDict = Dict (lang, broker)
            self._dictCache[key] = currentDict
        else:
            currentDict = self._dictCache[key]

        return currentDict


    def check (self, word):
        if not self._checkers:
            return True

        for checker in self._checkers + self._customCheckers:
            if checker.check (word):
                return True

        return False


    def getSuggest (self, word):
        suggest_set = set()
        for checker in self._checkers + self._customCheckers:
            suggest_set |= set (checker.suggest (word))

        suggest = [item for item in suggest_set if len (item.strip()) > 0]
        suggest.sort()

        return suggest
