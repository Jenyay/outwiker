# -*- coding: UTF-8 -*-

import os.path

from enchant import Dict, DictWithPWL, Broker
import enchant.errors

from dictsfinder import DictsFinder
from defines import CUSTOM_DICT_LANG


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
        dictsFinder = DictsFinder (folders)
        self._checkers = []
        self._customDictName = u'custom.dic'

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                try:
                    self._checkers.append (self._getDict (lang, path))
                except enchant.errors.Error:
                    pass

        if folders:
            try:
                self._checkers.append (self._getCustomDict (folders[-1]))
            except enchant.errors.Error:
                pass
            except IOError:
                pass


    def _createCustomDict (self, pathToDict):
        # Create fake language for custom dictionary
        dicFile = os.path.join (pathToDict,
                                CUSTOM_DICT_LANG + u'.dic')

        affFile = os.path.join (pathToDict,
                                CUSTOM_DICT_LANG + u'.aff')

        if not os.path.exists (dicFile):
            with open (dicFile, 'w') as fp:
                fp.writelines ([u'1', u'test'])

        if not os.path.exists (affFile):
            with open (affFile, 'w'):
                pass


    def _getCustomDict (self, pathToDict):
        customDictPath = os.path.join (pathToDict, self._customDictName)
        self._createCustomDict (pathToDict)

        key = (CUSTOM_DICT_LANG, customDictPath)

        if key not in self._dictCache:
            broker = Broker ()
            broker.set_param ('enchant.myspell.dictionary.path',
                              pathToDict)

            currentDict = DictWithPWL (CUSTOM_DICT_LANG,
                                       customDictPath,
                                       broker=broker)
            self._dictCache[key] = currentDict
        else:
            currentDict = self._dictCache[key]

        return currentDict


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
        # One (last) is custom dictionary
        if len (self._checkers) < 2:
            return True

        for checker in self._checkers:
            if checker.check (word):
                return True

        return False
