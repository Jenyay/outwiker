# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple
import re
import logging

from .basespellcheckerwrapper import BaseSpellCheckerWrapper

logger = logging.getLogger("outwiker.core.spellchecker.spellchecker")


class SpellChecker:
    """
    Class for checking a word with dictionaries
    """

    def __init__(
        self,
        real_checkers: List[BaseSpellCheckerWrapper],
        custom_dict_checker: Optional[BaseSpellCheckerWrapper] = None,
    ) -> None:
        self._wordRegex = re.compile(r"(?:(?:\w-\w)|\w)+")
        self._digitRegex = re.compile(r"\d")
        self._skipWordsWithNumbers = True
        self._realCheckers = real_checkers
        self._customDictChecker = custom_dict_checker

    @property
    def skipWordsWithNumbers(self):
        return self._skipWordsWithNumbers

    @skipWordsWithNumbers.setter
    def skipWordsWithNumbers(self, value):
        self._skipWordsWithNumbers = value

    # Used for tests only
    @property
    def realCheckers(self) -> List[BaseSpellCheckerWrapper]:
        return self._realCheckers

    # Used for tests only
    @property
    def customDictChecker(self) -> Optional[BaseSpellCheckerWrapper]:
        return self._customDictChecker

    def check(self, word) -> bool:
        """
        Return True if word is contained in the dictionaries
            or False otherwise
        """
        if self._skipWordsWithNumbers:
            match = self._digitRegex.search(word)
            if match is not None:
                # Skip words with numbers
                return True

        checkers = self._realCheckers + (
            [self._customDictChecker] if self._customDictChecker else []
        )
        if not checkers:
            return True

        for checker in checkers:
            if checker.check(word):
                return True

        return False

    def addToCustomDict(self, word):
        if self._customDictChecker is None:
            logger.warning("Custom dictionary checker is not set")
            return

        self._customDictChecker.addToCustomDict(word)

    def getSuggest(self, word) -> List[str]:
        suggestions = []
        for checker in self._realCheckers:
            suggestions.extend(checker.getSuggest(word))

        return sorted(set(suggestions))

    def findErrors(self, text) -> List[Tuple[str, int, int]]:
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
