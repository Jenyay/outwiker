from pathlib import Path
from typing import Union

from outwiker.core.tree import WikiDocument, WikiPage
from outwiker.core.factory import PageFactory

import outwiker.core.treetools as _treetools


def loadNotesTree(path: Union[str, Path], readonly: bool = False) -> WikiDocument:
    return _treetools.loadNotesTree(path, readonly)


def createNotesTree(path: Union[str, Path]) -> WikiDocument:
    return _treetools.createNotesTree(path)


def closeWiki(application) -> None:
    return _treetools.closeWiki(application)


def pageExists(page) -> bool:
    """
    Проверка на то, что страница была удалена сторонними средствами
    """
    return _treetools.pageExists(page)


def testreadonly(func):
    """
    Декоратор для отлавливания исключения
        outwiker.core.exceptions.ReadonlyException
    """
    return _treetools.testreadonly(func)


def generateLink(application, page) -> str:
    """
    Создать ссылку на страницу по UID
    """
    return _treetools.generateLink(application, page)


def findPage(application, page_id):
    """
    page_id - subpath of page or page UID
    """
    return _treetools.findPage(application, page_id)
