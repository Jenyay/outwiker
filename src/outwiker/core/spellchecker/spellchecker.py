# -*- coding: UTF-8 -*-

from enchantwrapper import EnchantWrapper


class SpellChecker (object):
    """
    Class for checking a word with dictionaries
    """
    def __init__ (self, langlist, folders):
        """
        langlist - list of a languages for checking (for example ["ru_RU", "en_US"])
        folders - list of paths to dictionaries
        """
        self._realChecker = self._getSpellCheckerWrapper (langlist, folders)


    def check (self, word):
        """
        Return True if word is contained in the dictionaries and False otherwise
        """
        return self._realChecker.check (word)


    def _getSpellCheckerWrapper (self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return EnchantWrapper (langlist, folders)


    def addToCustomDict (self, word):
        self._realChecker.addToCustomDict (word)


    def getSuggest (self, word):
        return self._realChecker.getSuggest (word)
