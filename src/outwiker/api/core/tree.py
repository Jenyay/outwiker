# coding: utf-8

import os.path

from pathlib import Path
from typing import Union


from outwiker.core.tree import WikiDocument


def loadNotesTree(path: Union[str, Path], readonly: bool = False) -> WikiDocument:
    return WikiDocument.load(str(path), readonly)


def createNotesTree(path: Union[str, Path]) -> WikiDocument:
    return WikiDocument.create(str(path))


def closeWiki(application):
    application.wikiroot = None


def pageExists(page) -> bool:
    """
    Проверка на то, что страница была удалена сторонними средствами
    """
    return page is not None and os.path.exists(page.path)
