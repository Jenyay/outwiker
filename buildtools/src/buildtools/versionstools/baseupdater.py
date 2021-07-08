# coding: utf-8

from abc import ABCMeta, abstractmethod
from typing import List, TextIO


class BaseUpdater(metaclass=ABCMeta):
    @abstractmethod
    def set_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        pass

    @abstractmethod
    def add_version(self, input_text: TextIO,
                    version: List[int],
                    status: str = '') -> str:
        pass
