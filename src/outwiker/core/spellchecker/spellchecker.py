# -*- coding: UTF-8 -*-

import re

from enchantwrapper import EnchantWrapper
from outwiker.core.events import SpellCheckingParams


class SpellChecker (object):
    """
    Class for checking a word with dictionaries
    """
    def __init__ (self, application, langlist, folders):
        """
        langlist - list of a languages for checking (for example ["ru_RU", "en_US"])
        folders - list of paths to dictionaries
        """
        self._application = application
        self._realChecker = self._getSpellCheckerWrapper (langlist, folders)

        self._wordRegex = re.compile (r'(?:(?:\w-\w)|\w)+', re.U)
        self._digitRegex = re.compile ('\d', re.U)

        self._skipWordsWithNumbers = True


    @property
    def skipWordsWithNumbers(self):
        return self._skipWordsWithNumbers


    @skipWordsWithNumbers.setter
    def skipWordsWithNumbers (self, value):
        self._skipWordsWithNumbers = value


    def check (self, word):
        """
        Return True if word is contained in the dictionaries and False otherwise
        """
        isValid = False

        if self._skipWordsWithNumbers:
            match = self._digitRegex.search (word)
            if match is not None:
                isValid = True

        if not isValid:
            isValid = self._realChecker.check (word)

        params = SpellCheckingParams (self, word, isValid)
        self._application.onSpellChecking (self._application.selectedPage, params)

        return params.isValid


    def _getSpellCheckerWrapper (self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return EnchantWrapper (langlist, folders)


    def addCustomDict (self, path):
        self._realChecker.addCustomDict (path)


    def addToCustomDict (self, dictIndex, word):
        self._realChecker.addToCustomDict (dictIndex, word)


    def getSuggest (self, word):
        return self._realChecker.getSuggest (word)


    def findErrors (self, text):
        """
        Return list of tuples with positions of invalid words: (word, error_start, error_end)
        """
        result = []

        words = self._wordRegex.finditer (text)
        for wordMatch in words:
            word = wordMatch.group(0)
            isValid = self.check (word)

            if not isValid:
                result.append ((word, wordMatch.start(), wordMatch.end()))

        return result
