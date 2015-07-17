# -*- coding: UTF-8 -*-

from enchantwrapper import EnchantWrapper


class SpellChecker (object):
    """
    Class for checking a word with dictionaries
    """
    def __init__ (self, config):
        self._config = config
        langlist = ["ru_RU"]
        self._realChecker = self._getSpellCheckerWrapper (langlist)


    def check (self, word):
        """
        Return True if word is contained in the dictionaries and False otherwise
        """
        return self._realChecker.check (word)


    def _getSpellCheckerWrapper (self, langlist):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return EnchantWrapper (langlist)
