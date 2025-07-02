# -*- coding: utf-8 -*-

import re
from outwiker.core.system import getOS


class SpellChecker:
    """
    Class for checking a word with dictionaries
    """

    def __init__(self, langlist, dict_folders):
        """
        langlist - list of a languages for checking
            (for example ["ru_RU", "en_US"])
        folders - list of paths to dictionaries
        """
        self._wordRegex = re.compile(r'(?:(?:\w-\w)|\w)+')
        self._digitRegex = re.compile(r'\d')
        self._skipWordsWithNumbers = True

        self._realChecker = getOS().getSpellChecker(dict_folders)
        for lang in langlist:
            self._realChecker.addLanguage(lang)

    @property
    def skipWordsWithNumbers(self):
        return self._skipWordsWithNumbers

    @skipWordsWithNumbers.setter
    def skipWordsWithNumbers(self, value):
        self._skipWordsWithNumbers = value

    def check(self, word):
        """
        Return True if word is contained in the dictionaries
            or False otherwise
        """
        isValid = False

        if self._skipWordsWithNumbers:
            match = self._digitRegex.search(word)
            if match is not None:
                isValid = True

        if not isValid:
            isValid = self._realChecker.check(word)

        return isValid

    def addCustomDict(self, path):
        self._realChecker.addCustomDict(path)

    def addToCustomDict(self, dictIndex, word):
        self._realChecker.addToCustomDict(dictIndex, word)

    def getSuggest(self, word):
        return self._realChecker.getSuggest(word)

    def findErrors(self, text):
        """
        Return list of tuples with positions of invalid words:
            (word, error_start, error_end)
        """
        result = []

        words = self._wordRegex.finditer(text)
        for wordMatch in words:
            word = wordMatch.group(0)
            isValid = self.check(word)

            if not isValid:
                result.append((word, wordMatch.start(), wordMatch.end()))

        return result
