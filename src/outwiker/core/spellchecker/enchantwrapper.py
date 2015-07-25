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
        self._customDictPath = os.path.join (folders[-1], u'custom.dic')
        self._customTag = '__custom'

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                try:
                    self._checkers.append (self._getDict (lang, path))
                except enchant.errors.Error:
                    pass

        try:
            self._checkers.append (self._getCustomDict ())
        except enchant.errors.Error:
            pass
        except IOError:
            pass


    def _getCustomDict (self):
        key = (self._customTag, self._customDictPath)

        if key not in self._dictCache:
            broker = Broker ()
            broker.set_param ('enchant.myspell.dictionary.path',
                              self._customDictPath)

            currentDict = DictWithPWL (None,
                                       self._customDictPath,
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
        if not self._checkers:
            return True

        for checker in self._checkers:
            if checker.check (word):
                return True

        return False
