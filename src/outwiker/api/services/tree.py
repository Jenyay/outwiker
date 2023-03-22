from typing import Optional

import wx

import outwiker.app.services.tree as _tree
from outwiker.core.tree import WikiDocument, WikiPage


def removePage(page: WikiPage) -> None:
    return _tree.removePage(page)


def openWikiWithDialog(parent: wx.Window, readonly=False) -> Optional[WikiDocument]:
    """
    Показать диалог открытия вики и вернуть открытую wiki
    parent -- родительское окно
    """
    return _tree.openWikiWithDialog(parent, readonly)


def openWiki(path: str, readonly: bool = False) -> Optional[WikiDocument]:
    return _tree.openWiki(path, readonly)


def testPageTitle(title) -> bool:
    """
    Возвращает True, если можно создавать страницу с таким заголовком
    """
    return _tree.testPageTitle(title)


def renamePage(page, newtitle) -> None:
    return _tree.renamePage(page, newtitle)


def movePage(page, newParent) -> None:
    """
    Сделать страницу page ребенком newParent
    """
    return _tree.movePage(page, newParent)


def createNewWiki(parentwnd: wx.Window):
    """
    Создать новую вики
    parentwnd - окно-владелец диалога выбора файла
    """
    return _tree.createNewWiki(parentwnd)
