# -*- coding: UTF-8 -*-

from outwiker.core.system import getSpellDirList
from dictsfinder import DictsFinder

from enchant import Dict, Broker


class EnchantWrapper (object):
    """
    Wrapper around pyenchant (http://pythonhosted.org/pyenchant/)
    """
    def __init__ (self, langlist):
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        dictsFinder = DictsFinder (getSpellDirList())
        self._checkers = []

        for lang in langlist:
            for path in dictsFinder.getFoldersForLang (lang):
                broker = Broker ()
                broker.set_param ('enchant.myspell.dictionary.path', path)
                self._checkers.append (Dict (lang, broker))


    def check (self, word):
        if not self._checkers:
            return True

        for checker in self._checkers:
            if checker.check (word):
                return True

        return False
