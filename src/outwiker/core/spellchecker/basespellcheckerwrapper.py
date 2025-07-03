
from abc import ABCMeta, abstractmethod
from typing import List


class BaseSpellCheckerWrapper (metaclass=ABCMeta):
    @abstractmethod
    def addLanguage(self, lang: str):
        pass

    @abstractmethod
    def addToCustomDict(self, word: str):
        pass

    @abstractmethod
    def setCustomDict(self, customDictPath: str):
        pass

    @abstractmethod
    def check(self, word: str) -> bool:
        pass

    @abstractmethod
    def getSuggest(self, word: str) -> List[str]:
        pass
