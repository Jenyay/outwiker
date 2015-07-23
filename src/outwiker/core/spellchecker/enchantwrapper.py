# -*- coding: UTF-8 -*-

from enchant import Dict, Broker

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

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                self._checkers.append (self._getDict (lang, path))


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
