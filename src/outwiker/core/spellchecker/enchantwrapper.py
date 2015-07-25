# -*- coding: UTF-8 -*-

import os.path

from enchant import Dict, DictWithPWL, Broker
import enchant.errors

from dictsfinder import DictsFinder


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
        self._customTag = '__custom'

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                try:
                    self._checkers.append (self._getDict (lang, path))
                except enchant.errors.Error:
                    pass

        if folders:
            try:
                self._checkers.append (self._getCustomDict (folders))
            except enchant.errors.Error:
                pass
            except IOError:
                pass


    def _getCustomDict (self, folders):
        customDictPath = os.path.join (folders[-1], self._customDictName)
        key = (self._customTag, customDictPath)

        if key not in self._dictCache:
            broker = Broker ()
            broker.set_param ('enchant.myspell.dictionary.path',
                              customDictPath)

            currentDict = DictWithPWL (None,
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
