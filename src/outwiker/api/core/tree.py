# coding: utf-8

from pathlib import Path
from typing import Union


from outwiker.core.tree import WikiDocument


def loadNotesTree(path: Union[str, Path], readonly: bool = False) -> WikiDocument:
    return WikiDocument.load(str(path), readonly)


def createNotesTree(path: Union[str, Path]) -> WikiDocument:
    return WikiDocument.create(str(path))
